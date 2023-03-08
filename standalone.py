from manager import Manager
import os
import json

# with open("prefix.json", "r") as f:
#     prefix_msg = json.load(f)
# with open("summary.json", "r") as f:
#     summary_msg = json.load(f)
manager = Manager(os.getenv("OPENAI_API_KEY"),
                  prefix_msg_path="save/meow/prefix.json", summary_msg_path="save/meow/summary.json", save_msg_path="save/meow/save.jsonl")


while True:
    msg = input(">> ")
    if msg == "q":
        break
    if msg == "sq":
        manager.save()
        break
    else:
        print(manager.gen_msg({"role": "user", "content": msg}).content)
