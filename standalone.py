from manager import Manager
import os
import json

with open("prefix.json", "r") as f:
    prefix_msg = json.load(f)
with open("summary.json", "r") as f:
    summary_msg = json.load(f)
manager = Manager(os.getenv("OPENAI_API_KEY"),
                  prefix_msg, summary_msg=summary_msg)


def save():
    with open("save.jsonl", "a") as f:
        for msg in manager.get_msg():
            f.write(json.dumps(msg) + "\n")
    with open("summary.json", "w") as f:
        print(type(manager.get_summary()))
        f.write(json.dumps(manager.get_summary()))
    print("saved.")


while True:
    msg = input(">> ")
    if msg == "q":
        save()
        break
    if msg == "sq":
        manager.summary_msg = manager.gen_summary()
        save()
        break
    else:
        print(manager.gen_msg({"role": "user", "content": msg}).content)
        if manager.self_check_dry():
            save()
