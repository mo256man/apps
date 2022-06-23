import sqlite3
import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import dates as mdates

dt = datetime.datetime.now()
date = dt.strftime("%Y/%m/%d")

dbname = ".\\static\\co2.db"
conn = sqlite3.connect(dbname)

sql = f"SELECT * FROM sensor WHERE date='{date}';"
df = pd.read_sql(sql, conn)

conn.commit()
conn.close()

# df["datetime"] = (df["date"] + " " + df["time"]).strptime("%Y/%m/%d %H:%M")
df["datetime"] = df["date"] + " " + df["time"]
print(df)

fig ,ax = plt.subplots(3 , 1, sharex=True, figsize=(10 , 5))
ax[0].scatter(df["datetime"], df["co2"], marker='.', linestyle="-", color="red")
ax[1].scatter(df["datetime"], df["temperture"], marker='.', linestyle="-")
ax[2].scatter(df["datetime"], df["humidity"], marker='.', linestyle="-")
xfmt = matplotlib.dates.DateFormatter("%H:%M")
# ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

plt.show()
