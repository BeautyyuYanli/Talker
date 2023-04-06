# import openai
import requests
import json
import os


class Manager:
    def __init__(self, prefix_msg_path: str, suffix_msg_path: str, save_msg_path: str, config: dict = {}) -> None:
        with open(prefix_msg_path, "r") as f:
            self.prefix_msg = json.load(f)
        with open(suffix_msg_path, "r") as f:
            self.suffix_msg = json.load(f)
        self.save_msg_path = save_msg_path
        self.msg = []
        self.total_tokens = 0
        self.balance_token = 3072
        self.config = config
        self.check_count = 0

    def gen_completion(self) -> dict:
        j = {
            "model": "gpt-3.5-turbo",
            "messages": self.get_full_msg(),
            # "stream": False
        }
        j.update(self.config)
        resp = requests.post(
            url=f"https://{os.getenv('OPENAI_API_BASE')}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}" ,
                "Content-Type": "application/json"
            },
            json=j
        )
        try:
            completion = resp.json()
        except json.decoder.JSONDecodeError:
            print("json decode error")
            completion = {"error": "json decode error",
                          "content": resp.content.decode("utf-8")}
        try:
            self.total_tokens = completion["usage"]["total_tokens"]
        except KeyError:
            pass
        completion.update({"status_code": resp.status_code})
        return completion

    def get_full_msg(self) -> dict:
        full_msg = self.prefix_msg + \
            self.msg[:-1] + self.suffix_msg + self.msg[-1:]
        return full_msg

# public:

    # check token usage, if overflow, trim and return True
    def self_check(self) -> bool:
        print(self.total_tokens)
        if self.total_tokens > self.balance_token:
            try:
                for _ in range(2*(self.check_count+1)):
                    self.msg.pop(0)
            except IndexError:
                print("no msg to trim")
            self.check_count += 1
            return True
        else:
            self.check_count = 0
            return False

    def save_all(self):
        with open(self.save_msg_path, "a", encoding="utf-8") as f:
            for msg in self.get_msg():
                f.write(json.dumps(msg, ensure_ascii=False) + "\n")

    def gen_msg(self, msg: dict) -> dict:
        self.self_check()
        self.msg.append(msg)
        try:
            completion = self.gen_completion()
            msg = completion["choices"][0]["message"]
            self.msg.append(msg)
            with open(self.save_msg_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(self.msg[-2], ensure_ascii=False) + "\n")
                f.write(json.dumps(self.msg[-1], ensure_ascii=False) + "\n")
        except KeyError:
            self.msg.pop(-1)
            msg = {"role": "program", "content": json.dumps(
                completion, ensure_ascii=False)}
        return msg

    def get_msg(self) -> list:
        return self.msg
