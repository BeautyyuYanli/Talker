from managerpool import ManagerPool
from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os


app = Flask(__name__, static_url_path="/dist")
CORS(app)
pool = ManagerPool()


@app.route("/gen_msg", methods=["POST"])
def gen_msg():
    msg = request.data.decode("utf-8")
    model = request.args.get("model")
    return pool.get(model).gen_msg({"role": "user", "content": msg})["content"]


@app.route("/")
def index():
    return send_from_directory("frontend/dist", "index.html")


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('frontend/dist', path)
