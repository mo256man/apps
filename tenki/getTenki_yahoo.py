import requests
import json
import pandas as pd
import pprint

latitude, longitude = 35.027686, 137.034037

# Yahoo! 気象情報API
# https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/weather.html
app_id = "dj00aiZpPXo5cG9DYkh6Qm93byZzPWNvbnN1bWVyc2VjcmV0Jng9YTY-"
url = "https://map.yahooapis.jp/weather/V1/place"
param = f"?coordinates={longitude},{latitude}&appid={app_id}&output=json&past=1"

response = requests.get(url + param)
jsonData = response.json()
weathers = jsonData["Feature"][0]["Property"]["WeatherList"]["Weather"]

for weather in weathers:
    print(weather)
