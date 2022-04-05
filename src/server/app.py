from flask import Flask, Response, jsonify, request
from flask_cors import CORS

import compile_pyteal

app = Flask(__name__)
CORS(app, resources=r"/*")
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/hello")
def hello():
    return jsonify({"body": "Hello, from Cadenza!"})


@app.route("/compile", methods=["POST"])
def compile():
    file = request.files["file"]
    body = file.read()
    try:
        compiled_source = compile_pyteal.raw_compile(body)
        return Response(f"Compilation successful: {compiled_source}", status=200)
    except Exception as e:
        return Response("Bad Approval program; could not compile PyTeal", status=400)


@app.route("/deploy", methods=["POST"])
def deploy_app():
    file = request.files["file"]
    body = file.read()
    resp = compile_pyteal.raw_compile(body)

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0")
