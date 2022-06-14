from asyncio.windows_events import NULL
from numbers import Real
from pickle import NONE
import random
import sqlite3
from pprint import pprint

db_file = "database.db"

def init():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    #Create Table "times"
    cur.execute('''
                CREATE TABLE IF NOT EXISTS times (
                    id INTEGER PRIMARY KEY,
                    lane_1 REAL NOT NULL DEFAULT 0.00,
                    lane_2 REAL NOT NULL DEFAULT 0.00,
                    lane_3 REAL NOT NULL DEFAULT 0.00,
                    img_path TEXT,
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            ''')

    con.commit()
    con.close()


def get_times():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    list = []
    result = cur.execute('SELECT * FROM times ORDER BY timestamp desc')
    for row in result:
        list.append({
            "id": row[0],
            "lane_1": row[1],
            "lane_2": row[2],
            "lane_3": row[3],
            "img_path": row[4],
            "timestamp": row[5],
        })

    con.close()
    return list


def add_times(lane_1 : float, lane_2 : float, lane_3 : float, img_path : str = None):
    """Add times to Database"""
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute("INSERT INTO times(lane_1, lane_2, lane_3, img_path) VALUES (?,?,?,?)", (lane_1, lane_2, lane_3, img_path))

    con.commit()
    con.close()


if __name__ == "__main__":
        init()
        add_times(
            round(random.uniform(70.0, 90.0),2),
            round(random.uniform(70.0, 90.0),2),
            round(random.uniform(70.0, 90.0),2),
        )