from flask import Flask, Response, jsonify, request, render_template
from flask_cors import CORS
import json, os

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


@app.route("/compile", methods=["POST"])
def compile():
    # print(f"compiling {request.data}")
    # Set CORS headers for the main request
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    try:
        body = json.loads(request.data, strict=False)
        body = body["body"]
    except:
        return Response("Bad Request in body", status=400)
    try:
        compiled_source = compile_pyteal.raw_compile(body)
        return Response(
            f"Compilation successful: {compiled_source}", status=200, headers=headers
        )
    except Exception as e:
        return Response(
            "Bad Approval program; could not compile PyTeal",
            status=400,
            headers=headers,
        )


@app.route("/compile-file", methods=["POST"])
def compile_file():
    file = request.files["file"]
    body = file.read()
    try:
        compiled_source = compile_pyteal.raw_compile(body)
        return Response(f"Compilation successful: {compiled_source}", status=200)
    except Exception as e:
        return Response("Bad Approval program; could not compile PyTeal", status=400)


@app.route("/deploy", methods=["POST"])
def deploy_app():
    global current_account

    file = request.files["file"]
    body = file.read()

    client = sandbox_utils.create_algod_client()
    current_account.generate_transient_account(client)
    compiled_source = compile_pyteal.raw_compile(body)

    resp = sandbox_utils.deploy_app(
        client, compiled_source, current_account.sk, current_account.pk
    )

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0")
