import sqlite3


class DB:
    def __init__(self, name: str) -> None:
        self.con = sqlite3.connect(f"data/{name}.db", check_same_thread=False)
        self.cur = self.con.cursor()
        res = self.cur.execute("SELECT name FROM sqlite_master").fetchone()
        if res is None:
            self.cur.execute("""
CREATE TABLE history (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   role TEXT,
   content TEXT,
   token INTEGER
);
"""
                             )

    def add(self, user_msg: dict, comp_msg: dict) -> None:
        self.cur.execute(
            "INSERT INTO history (role, content, token) VALUES (?, ?, ?)", (user_msg["role"], user_msg["content"], user_msg["token"]))
        self.cur.execute(
            "INSERT INTO history (role, content, token) VALUES (?, ?, ?)", (comp_msg["role"], comp_msg["content"], comp_msg["token"]))
        self.con.commit()

    def get_msg(self, token: int) -> list:
        res = self.cur.execute(
            f"""
SELECT *
FROM 
(SELECT *
 FROM history 
 ORDER BY id DESC
) t
WHERE 
(SELECT SUM(token) 
 FROM history 
 WHERE id >= t.id
) <= {token};
        """
        ).fetchall()
        res.reverse()
        return [
            {
                "role": r[1],
                "content": r[2],
                "token": r[3]
            }
            for r in res
        ]


if __name__ == "__main__":
    db = DB("test")
    db.add("user", "hello", 1000)
    db.add("user", "你好", 1000)
    db.add("user", "hola", 1000)
    print(db.get_msg(4000))
