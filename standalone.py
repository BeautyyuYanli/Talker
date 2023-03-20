from managerpool import ManagerPool
import argparse


argparser = argparse.ArgumentParser()
argparser.add_argument("--model", type=str, default="default")
manager = ManagerPool().get(argparser.parse_args().model)

while True:
    msg = input(">> ")
    if msg == "q":
        break
    else:
        print(manager.gen_msg({"role": "user", "content": msg})["content"])
