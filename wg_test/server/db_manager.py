import sqlite3
import json

class DatabaseManager:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('users.db')
        self.init_database()

    def init_database(self):
        c = self.conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS users (nickname TEXT, credits INTEGER, resources TEXT)")
        self.conn.commit()

    def create_user(self, nickname):
        c = self.conn.cursor()
        c.execute("INSERT INTO users (nickname, credits, resources) VALUES (?, ?, ?)", (nickname, 0, json.dumps([])))
        self.conn.commit()

        c.close()

    def load_user(self, nickname):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE nickname=?", (nickname,))
        result_from_db = c.fetchone()

        result = None
        if result_from_db != None:
            result = {'nickname' : result_from_db[0], 'credits' : result_from_db[1], 'resources' : result_from_db[2]}
        c.close()

        return result
    def update_credits(self, nickname, new_credits):
        c = self.conn.cursor()
        c.execute("UPDATE users SET credits = ? WHERE nickname = ?", (new_credits, nickname))
        self.conn.commit()

        c.close()

    def update_resources(self, nickname, new_resources):
        c = self.conn.cursor()
        c.execute("UPDATE users SET resources = ? WHERE nickname = ?", (json.dumps(new_resources), nickname))
        self.conn.commit()

        c.close()