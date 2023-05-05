import requests
import json
import os
from talker.db.redis import RedisDB
from threading import Lock
from typing import Dict 

locks: Dict[str, Lock] = dict({})


class Talker:
    def __init__(self, model: str, id: str) -> None:
        try:
            with open(f"models/{model}.json") as f:
                config = json.load(f)
        except FileNotFoundError:
            model = "default"
            with open(f"models/{model}.json") as f:
                config = json.load(f)
        self.prefix_msg = config["prefix"]
        self.suffix_msg = config["suffix"]
        self.config = config.get("api_config", {})
        self.id = id
        self.history_token = 3072
        self.db = RedisDB(id)
        if locks.get(id) is None:
            locks[id] = Lock()

    def update_msg(self):
        msg = self.db.get_msg(self.history_token)
        self.msg = [{"role": r["role"], "content": r["content"]} for r in msg]
        self.total_tokens = sum([r["token"] for r in msg])

    def gen_completion(self, user_msg: dict) -> dict:
        j = {
            "model": "gpt-3.5-turbo",
            "messages": self.prefix_msg + self.msg + self.suffix_msg + [user_msg],
            # "stream": False
        }
        j.update(self.config)
        resp = requests.post(
            url=f"https://{os.getenv('OPENAI_API_BASE') if os.getenv('OPENAI_API_BASE') else 'api.openai.com'}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json",
            },
            json=j,
        )
        try:
            completion = resp.json()
        except json.decoder.JSONDecodeError:
            print("json decode error")
            completion = {
                "error": "json decode error",
                "content": resp.content.decode("utf-8"),
            }
        completion.update({"status_code": resp.status_code})
        return completion

    # public:

    def gen_msg(self, user_msg: dict) -> dict:
        locks[self.id].acquire()
        self.update_msg()
        try:
            completion = self.gen_completion(user_msg)
            user_msg.update(
                {"token": completion["usage"]["prompt_tokens"] - self.total_tokens}
            )
            comp_msg = completion["choices"][0]["message"]
            comp_msg.update({"token": completion["usage"]["completion_tokens"]})
            self.db.add(user_msg, comp_msg)
        except KeyError:
            comp_msg = {
                "role": "program",
                "content": json.dumps(completion, ensure_ascii=False),
            }
        except Exception as e:
            print("Error: ", e)
            comp_msg = {"role": "program", "content": "Error: " + str(e)}
        locks[self.id].release()
        return comp_msg
