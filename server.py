from flask import send_from_directory
from manager import Manager
from flask import Flask, request
from flask_cors import CORS
import os
import json

with open("prefix.json", "r") as f:
    prefix_msg = json.load(f)
with open("summary.json", "r") as f:
    summary_msg = json.load(f)
manager = Manager(os.getenv("OPENAI_API_KEY"),
                  prefix_msg, summary_msg=summary_msg)


def save():
    with open("save.jsonl", "a") as f:
        for msg in manager.get_msg():
            f.write(json.dumps(msg) + "\n")
    with open("summary.json", "w") as f:
        print(type(manager.get_summary()))
        f.write(json.dumps(manager.get_summary()))
    print("saved.")


app = Flask(__name__, static_url_path="/dist")
CORS(app)


@app.route("/gen_msg", methods=["POST"])
def gen_msg():
    msg = request.data.decode("utf-8")
    return manager.gen_msg({"role": "user", "content": msg}).content


@app.route("/gen_summary", methods=["POST"])
def gen_summary():
    manager.summary_msg = manager.gen_summary()
    save()
    return "OK"


@app.route("/save", methods=["POST"])
def save_():
    save()
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
