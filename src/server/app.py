from flask import Flask, jsonify, request
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
    resp = compile_pyteal.raw_compile(body)

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0")
