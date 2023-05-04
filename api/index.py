from talker.talker import Talker
from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os


app = Flask(__name__, static_url_path="/dist")
CORS(app)
os.mkdir("data") if not os.path.exists("data") else None


def inspect_model(model: str) -> str:
    try:
        with open(f"models/{model}.json") as f:
            pass
    except FileNotFoundError:
        model = "default"
    return model


@app.route("/gen_msg", methods=["POST"])
def gen_msg():
    if os.getenv("TALKER_TOKEN") and request.headers.get("Authorization") != os.getenv(
        "TALKER_TOKEN"
    ):
        return "Unauthorized", 401
    msg = request.data.decode("utf-8")
    model = request.args.get("model", None)
    model = inspect_model(model)
    id = request.args.get("id", "default")
    id = f"{model}_{id}"
    return Talker(model, id).gen_msg({"role": "user", "content": msg})["content"]


@app.route("/")
def index():
    return send_from_directory("../frontend/dist", "index.html")


@app.route("/<path:path>", methods=["GET"])
def static_proxy(path):
    return send_from_directory("../frontend/dist", path)
