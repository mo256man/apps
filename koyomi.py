import ephem
import datetime
import pytz

sun = ephem.Sun()                       # 太陽
moon = ephem.Moon()                     # 月

class Ephem():
    def __init__(self):
        self.lat = 35.1667                              # 北緯
        self.lon = 136.9167                             # 東経
        elev = 0                                        # 標高
        self.name = "名古屋"                            # 地名
        self.timedelta = datetime.timedelta(hours=9)    # utcと日本時間の時差
        self.location = ephem.Observer()

        dt_local = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))   # 日本の日時
        self.date = dt_local.date()                     # 日本の日付
        
        dt_utc = dt_local - self.timedelta              # UTC時間での日時
        self.dt0 = self.get0hour(dt_utc)                # 今日の0時0分0秒を登録
        self.location.date = self.get0hour(self.dt0)          
        self.location.lat = str(self.lat)
        self.location.lon = str(self.lon)
        self.location.elev = elev

        self.getResult()
        
    def get0hour(self, dt):
        # 現在時刻ではなく今日の0時を基準とするために時差で日付を修正する
        if dt.hour < 15:                                # 15時以前ならば
            dt = dt + datetime.timedelta(days=1)        # -1日する
        return dt

    def getResult(self):
        self.today_rising = self.dt2str(self.location.next_rising(sun))
        self.today_setting = self.dt2str(self.location.next_setting(sun))
        self.moon_phase = round(self.location.date - ephem.previous_new_moon(self.location.date),2)

        self.moon_emoji = "🌓"
        moons = ["🌑🌑🌒🌒🌒🌓🌓🌓🌔🌔🌔🌔🌕🌖🌗🌘"]

        self.location.date= self.dt0 + datetime.timedelta(days=1)      # 翌日に注目
        self.tomorrow_rising = self.dt2str(self.location.next_rising(sun))
        self.tomorrow_setting = self.dt2str(self.location.next_setting(sun))

    def dt2str(self, dt):
        return (ephem.localtime(dt).strftime("%H:%M"))

    def change_date(self, k):
        if k==0:
            self.date = datetime.datetime.now().date()
        else:
            self.date = self.date + datetime.timedelta(days=k)
        self.location.date = self.date
        self.getResult()


def main():
    ep = Ephem()
    
    ep.getResult()

    pass

if __name__=="__main__":
    main()