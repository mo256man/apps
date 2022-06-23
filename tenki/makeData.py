import sqlite3
import datetime
import random

dt = datetime.datetime.now()
date = dt.strftime("%Y/%m/%d")
time = dt.strftime("%H:%M")

dbname = ".\\static\\co2.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

co2 = random.randint(600, 900)
temperture = random.randint(25, 30)
humidity = random.randint(40, 80)

sql = f"INSERT INTO sensor VALUES ('{date}', '{time}', {co2}, {temperture}, {humidity});"

cur.execute(sql)
conn.commit()
cur.close()
conn.close()