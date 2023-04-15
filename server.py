from talker.pool import Pool
from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os


app = Flask(__name__, static_url_path="/dist")
CORS(app)
pool = Pool()
os.mkdir("data") if not os.path.exists("data") else None


@app.route("/new", methods=["GET"])
def new():
    model = request.args.get("model", None)
    return pool.new(model)


@app.route("/gen_msg", methods=["POST"])
def gen_msg():
    msg = request.data.decode("utf-8")
    model = request.args.get("model", None)
    id = request.args.get("id", None)
    return pool.get(id, model=model).gen_msg({"role": "user", "content": msg})["content"]


@app.route("/")
def index():
    return send_from_directory("frontend/dist", "index.html")


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('frontend/dist', path)
