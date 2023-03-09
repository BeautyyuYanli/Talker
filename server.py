from flask import send_from_directory
from manager import Manager
from flask import Flask, request
from flask_cors import CORS
import os


class ManagerPool:
    def __init__(self) -> None:
        self.pool = {}

    def get(self, key):
        if key not in self.pool:
            try:
                self.pool[key] = Manager(os.getenv("OPENAI_API_KEY"),
                                         prefix_msg_path=f"save/{key}/prefix.json", suffix_msg_path=f"save/{key}/suffix.json", summary_msg_path=f"save/{key}/summary.json", save_msg_path=f"save/{key}/save.jsonl")
            except FileNotFoundError:
                self.pool[key] = Manager(os.getenv("OPENAI_API_KEY"),
                                         prefix_msg_path=f"save/default/prefix.json", suffix_msg_path=f"save/default/suffix.json", summary_msg_path=f"save/default/summary.json", save_msg_path=f"save/default/save.jsonl")
        return self.pool[key]

    def get_all(self):
        return self.pool.keys()


app = Flask(__name__, static_url_path="/dist")
CORS(app)
pool = ManagerPool()


@app.route("/gen_msg", methods=["POST"])
def gen_msg():
    msg = request.data.decode("utf-8")
    model = request.args.get("model")
    return pool.get(model).gen_msg({"role": "user", "content": msg}).content


@app.route("/save_with_summary", methods=["POST"])
def save_with_summary():
    manager = pool.get(request.args.get("model"))
    manager.set_summary(manager.gen_summary())
    manager.save()
    return "OK"


@app.route("/save", methods=["POST"])
def save():
    manager = pool.get(request.args.get("model"))
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
