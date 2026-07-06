from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


DB_PATH = Path(__file__).parent / "rss.db"


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

    def execute(self, query: str, params: tuple = ()):

        cur = self.conn.cursor()

        cur.execute(query, params)

        self.conn.commit()

        return cur

    def fetchone(self, query: str, params: tuple = ()):

        cur = self.conn.cursor()

        cur.execute(query, params)

        row = cur.fetchone()

        return dict(row) if row else None

    def fetchall(self, query: str, params: tuple = ()):

        cur = self.conn.cursor()

        cur.execute(query, params)

        rows = cur.fetchall()

        return [dict(r) for r in rows]

    def insert(self, table: str, data: dict):

        keys = ",".join(data.keys())

        placeholders = ",".join(["?"] * len(data))

        values = tuple(data.values())

        sql = f"""
        INSERT INTO {table}
        ({keys})
        VALUES
        ({placeholders})
        """

        cur = self.execute(sql, values)

        return cur.lastrowid

    def update(
        self,
        table: str,
        data: dict,
        where: str,
        params: tuple,
    ):

        sets = ",".join(
            f"{k}=?" for k in data.keys()
        )

        values = tuple(data.values()) + params

        sql = f"""
        UPDATE {table}

        SET {sets}

        WHERE {where}
        """

        self.execute(sql, values)

    def delete(
        self,
        table: str,
        where: str,
        params: tuple,
    ):

        sql = f"""
        DELETE FROM {table}

        WHERE {where}
        """

        self.execute(sql, params)


db = Database()
