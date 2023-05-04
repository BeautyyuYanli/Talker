import redis
import os
import json

kv_url = os.environ.get("KV_URL")
if os.environ.get("VERCEL"):
    kv_url = kv_url.replace("redis://", "rediss://")
conn = redis.Redis.from_url(kv_url)


class DB:
    def __init__(self, name: str) -> None:
        self.name = name

    def add(self, user_msg: dict, comp_msg: dict) -> None:
        conn.rpush(self.name, json.dumps(user_msg), json.dumps(comp_msg))

    def get_msg(self, token: int, trim: bool = False) -> list:
        l = conn.lrange(self.name, 0, -1)
        l = [json.loads(i) for i in l]
        # trim
        trim_b = False
        total_token = 0
        for i in range(len(l) - 1, -1, -1):
            total_token += l[i]["token"]
            if total_token > token:
                trim_b = True
                break
        if trim_b:
            l = l[i + 1 :]
            if trim:
                conn.ltrim(self.name, i + 1, -1)
        return l


if __name__ == "__main__":
    db = DB("test_1")
    # db.add({"a": 1, "token": 100}, {"b": 2, "token": 200})
    # db.add({"a": 3, "token": 300}, {"b": 4, "token": 400})
    print(db.get_msg(1000))
