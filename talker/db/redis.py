from talker.db.base import DB
import redis
import os
import json
from typing import Dict, List, Optional, Union, Any

kv_url = os.environ.get("KV_URL")
conn = redis.Redis.from_url(kv_url)


class RedisDB(DB):
    def add(self, user_msg: Dict[str, Any], comp_msg: Dict[str, Any]) -> None:
        conn.rpush(self.id, json.dumps(user_msg, ensure_ascii=False), json.dumps(comp_msg, ensure_ascii=False))

    def get_msg(self, token: int, trim: bool = True) -> List[Dict[str, Any]]:
        l = conn.lrange(self.id, 0, -1)
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
                conn.ltrim(self.id, i + 1, -1)
        return l


if __name__ == "__main__":
    db = RedisDB("test_1")
    # db.add({"a": 1, "token": 100}, {"b": 2, "token": 200})
    # db.add({"a": 3, "token": 300}, {"b": 4, "token": 400})
    print(db.get_msg(1000))
