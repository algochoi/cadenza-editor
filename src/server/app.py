import base64
import json

from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS

import application_call
import compile_pyteal
import sandbox_utils

app = Flask(__name__)
CORS(app, resources=r"/*")
app.config["CORS_HEADERS"] = "Content-Type"


class Account:
    def __init__(self) -> None:
        self.sandbox_account = sandbox_utils.SandboxAccount()
        self.pk = ""
        self.sk = ""

    def generate_transient_account(self, client):
        self.sk, self.pk = self.sandbox_account.get_funded_transient(client)


# Generate new transient account pairs for every app deployment
current_account = Account()


@app.route("/")
def render_main():
    return render_template("index.html")


@app.route("/hello")
def hello():
    return jsonify({"body": "Hello, from Cadenza!"})


def json_result(compiled: str, teal: str) -> str:
    return json.dumps({"result": compiled, "teal": teal})


@app.route("/compile", methods=["POST"])
def compile():
    # Parse the incoming request.
    # The PyTeal code is sent as text in the body field.
    try:
        body = json.loads(request.data, strict=False)
        body = body["body"]
    except:
        return Response("Bad Request in body", status=400)

    # Try to compile the PyTeal code, and if it fails, return the error.
    try:
        teal_source, compiled_source = compile_pyteal.compile_pyteal(body)
        b64encoded = base64.b64encode(compiled_source).decode("utf8")
        compiled_source = f"Compilation successful: {b64encoded}"
        return Response(json_result(compiled_source, teal_source), status=200)
    except Exception as e:
        return Response(
            json_result(f"Could not compile PyTeal: {e}", ""),
            status=400,
        )


@app.route("/compile-file", methods=["POST"])
def compile_file():
    file = request.files["file"]
    body = file.read()
    try:
        teal_source, compiled_source = compile_pyteal.compile_pyteal(body)
        compiled_source = f"Compilation successful: {compiled_source}"
        return Response(json_result(compiled_source, teal_source), status=200)
    except Exception as e:
        return Response("Bad Approval program; could not compile PyTeal", status=400)


@app.route("/deploy", methods=["POST"])
def deploy_app():
    global current_account

    try:
        body = json.loads(request.data, strict=False)
        body = body["body"]
    except:
        return Response("Bad Request in body", status=400)

    try:
        client = sandbox_utils.create_algod_client()
        current_account.generate_transient_account(client)
        _, compiled_source = compile_pyteal.compile_pyteal(body)

        resp = application_call.deploy_app(
            client, compiled_source, current_account.sk, current_account.pk
        )
        return resp
    except Exception as e:
        return Response(
            json_result(f"Could not deploy PyTeal: {e}", ""),
            status=400,
        )


@app.route("/deploy-file", methods=["POST"])
def deploy_app_from_file():
    global current_account

    file = request.files["file"]
    body = file.read()

    client = sandbox_utils.create_algod_client()
    current_account.generate_transient_account(client)
    _, compiled_source = compile_pyteal.compile_pyteal(body)

    resp = application_call.deploy_app(
        client, compiled_source, current_account.sk, current_account.pk
    )

    return Response(resp, status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
