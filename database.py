import os
import sqlite3
import json
from typing import Union

class Database:
    def __init__(self, filename: Union[str, os.PathLike]):
        self.__db = sqlite3.connect(filename)
        self.__db.row_factory = self.dict_factory
        self.__cursor = self.__db.cursor()
        self.create_table()

    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL, password TEXT NOT NULL)"
        self.__db.execute(query)
        self.__db.commit()

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_user(self, **options):
        query = "SELECT * FROM users WHERE "
        if not options:
            return
        args = []
        args_str = []
        for key, val in options.items():
            args.append(val)
            args_str.append(f"{key} = ?")

        query += " AND ".join(args_str)
        self.__cursor.execute(query, args)
        return self.__cursor.fetchone()

    def add_user(self, **options):
        if "login" in options and self.get_user(login=options["login"]):
            raise Exception("User has been already registered!")

        query = "INSERT INTO users ({}) VALUES ({})"
        if not options:
            return
        args_str = []
        args = []

        for key, val in options.items():
            args_str.append(key)
            args.append(val)
        query = query.format(", ".join(args_str), ", ".join(list("?"*len(args_str))))
        self.__cursor.execute(query, args)
        self.__db.commit()
        return self.__cursor.lastrowid

    def update_user(self, id: int, **options):
        query = 'UPDATE users SET {} WHERE id = ?'
        if not options:
            return

        args_str = []
        args = []

        for key, val in options.items():
            args_str.append(f"{key} = ?")
            args.append(val)

        args.append(id)
        query = query.format(", ".join(args_str))
        self.__cursor.execute(query, args)
        return self.__db.commit()
