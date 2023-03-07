import openai
import os


class Manager:
    def __init__(self, api_key: str, prefix_msg: list, summary_msg: dict | None = None) -> None:
        openai.api_key = api_key
        self.prefix_msg = prefix_msg
        self.summary_msg = summary_msg
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
        full_msg = ([self.summary_msg] if self.summary_msg else []) + \
            self.prefix_msg + self.msg
        return full_msg

# public:

    def gen_summary(self) -> dict:
        msg = {
            "role": "system",
            "content": "以第一人称总结以上对话"
        }
        self.msg.append(msg)
        completion = self.gen_completion()
        self.msg.pop()
        return completion.choices[0].message

    # check token usage, if overflow, trim and return True
    def self_check(self) -> bool:
        if self.last_completion is None:
            return False
        if self.last_completion.usage.total_tokens > self.max_token:
            self.summary_msg = self.gen_summary()
            self.msg = []
            return True

    def self_check_dry(self) -> bool:
        if self.last_completion is None:
            return False
        if self.last_completion.usage.total_tokens > self.max_token:
            return True

    def gen_msg(self, msg: dict) -> dict:
        check = self.self_check()
        if check:
            print(2, "Made summary")
        self.msg.append(msg)
        completion = self.gen_completion()
        msg = completion.choices[0].message
        self.msg.append(msg)
        return msg

    def get_msg(self) -> list:
        return self.msg

    def get_summary(self) -> dict:
        return self.summary_msg
