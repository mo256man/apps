import requests
import json
import pprint
import sqlite3
import datetime


# Open Weather
# https://openweathermap.org/
# https://qiita.com/noritakaIzumi/items/34f16e383f59f9c5d8cf

def get_tenki():
    latitude, longitude = 35.027686, 137.034037
    api_key = "3b241d7361b50161806f04c7b40d3452"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": str(latitude),
        "lon": str(longitude),
        "appid": api_key,
        "units": "metric",
        "lang": "ja",
    }

    response = requests.get(url, params=params)
    json_data = json.loads(response.text)
    return json_data

def json2db():
    dt = datetime.datetime.now()
    json_data = get_tenki()
    date = dt.strftime("%Y/%m/%d")
    time = dt.strftime("%H:%M")
    weather = json_data["weather"][0]["description"]
    temp = json_data["main"]["temp"]
    humidity = json_data["main"]["humidity"]
    wind_speed = json_data["wind"]["speed"]
    icon = json_data["weather"][0]["icon"]

    dbpath = ".\\static\\"
    dbname = "co2.sqlite"
    conn = sqlite3.connect(dbpath + dbname)
    cur = conn.cursor()
    sql = f"INSERT INTO weather VALUES('{date}','{time}','{weather}', {temp}, {humidity}, {wind_speed}, '{icon}');" 
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return (date, time, weather, temp, humidity, wind_speed, icon)

if __name__ == "__main__":
    json2db()