from manager import Manager
import os
import argparse


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


argparser = argparse.ArgumentParser()
argparser.add_argument("--model", type=str, default="default")
manager = ManagerPool().get(argparser.parse_args().model)

while True:
    msg = input(">> ")
    if msg == "q":
        break
    if msg == "sq":
        manager.save()
        break
    else:
        print(manager.gen_msg({"role": "user", "content": msg})["content"])
