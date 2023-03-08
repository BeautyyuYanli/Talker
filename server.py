from flask import send_from_directory
from manager import Manager
from flask import Flask, request
from flask_cors import CORS
import os

manager = Manager(os.getenv("OPENAI_API_KEY"),
                  prefix_msg_path="save/meow/prefix.json", summary_msg_path="save/meow/summary.json", save_msg_path="save/meow/save.jsonl")

app = Flask(__name__, static_url_path="/dist")
CORS(app)


@app.route("/gen_msg", methods=["POST"])
def gen_msg():
    msg = request.data.decode("utf-8")
    return manager.gen_msg({"role": "user", "content": msg}).content


@app.route("/save_with_summary", methods=["POST"])
def save_with_summary():
    manager.set_summary(manager.gen_summary())
    manager.save()
    return "OK"


@app.route("/save", methods=["POST"])
def save():
    manager.save()
    return "OK"


@app.route("/echo", methods=["POST"])
def echo():
    msg = request.data
    return msg


@app.route("/")
def index():
    return send_from_directory("frontend/dist", "index.html")


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('frontend/dist', path)
