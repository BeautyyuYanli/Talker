from manager import Manager
import os
import json


class ManagerPool:
    def __init__(self) -> None:
        self.pool = {}

    def get(self, key) -> Manager:
        if key not in self.pool:
            try:
                try:
                    with open(f"save/{key}/config.json") as f:
                        config = json.load(f)
                except FileNotFoundError:
                    config = {}

                self.pool[key] = Manager(prefix_msg_path=f"save/{key}/prefix.json", suffix_msg_path=f"save/{key}/suffix.json", save_msg_path=f"save/{key}/save.jsonl", config=config)
            except FileNotFoundError:
                self.pool[key] = Manager(prefix_msg_path=f"save/default/prefix.json", suffix_msg_path=f"save/default/suffix.json", save_msg_path=f"save/default/save.jsonl")
        return self.pool[key]

    def get_all(self):
        return self.pool.keys()
