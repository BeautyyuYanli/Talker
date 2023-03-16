import openai
import os
import json
import time


class Manager:
    def __init__(self, api_key: str, prefix_msg_path: str, suffix_msg_path: str, summary_msg_path: str, save_msg_path: str) -> None:
        openai.api_key = api_key
        with open(prefix_msg_path, "r") as f:
            self.prefix_msg = json.load(f)
        with open(suffix_msg_path, "r") as f:
            self.suffix_msg = json.load(f)
        self.summary_msg_path = summary_msg_path
        try:
            with open(summary_msg_path, "r") as f:
                self.summary_msg = json.load(f)
        except FileNotFoundError:
            self.summary_msg = None
        self.save_msg_path = save_msg_path
        self.msg = []
        self.last_completion = None
        self.max_token = 3072

    def gen_completion(self) -> dict:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.get_full_msg()
        )
        self.last_completion = completion
        return completion

    def get_full_msg(self) -> dict:
        full_msg = self.prefix_msg + \
            ([self.summary_msg] if self.summary_msg else []) + \
            self.msg + self.suffix_msg
        return full_msg

# public:

    def gen_summary(self) -> dict:
        msg = {
            "role": "system",
            "content": "以第一人称总结以上内容"
        }
        self.msg.append(msg)
        while True:
            try:
                completion = self.gen_completion()
                break
            except:
                time.sleep(3)
                continue

        self.msg.pop()
        return completion.choices[0].message

    def set_summary(self, summary_msg: dict):
        self.summary_msg = summary_msg
        self.summary_msg["role"] = "system"
        self.summary_msg["content"] = "你刚才所做的总结：" + self.summary_msg["content"]

    # check token usage, if overflow, trim and return True
    def self_check(self) -> bool:
        if self.last_completion is None:
            return False
        print(self.last_completion.usage.total_tokens)
        if self.last_completion.usage.total_tokens > self.max_token:

            return True
        else:
            return False

    def save(self):
        with open(self.save_msg_path, "a", encoding="utf-8") as f:
            for msg in self.get_msg():
                f.write(json.dumps(msg, ensure_ascii=False) + "\n")
        with open(self.summary_msg_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.get_summary(), ensure_ascii=False))

    def gen_msg(self, msg: dict) -> dict:
        check = self.self_check()
        if check:
            self.set_summary(self.gen_summary())
            self.save()
            self.msg = []
            print(2, "Made summary")
        self.msg.append(msg)
        try:
            completion = self.gen_completion()
            msg = completion.choices[0].message
            self.msg.append(msg)
        except Exception as e:
            msg = {"role": "program", "content": e}
        return msg

    def get_msg(self) -> list:
        return self.msg

    def get_summary(self) -> dict:
        return self.summary_msg
