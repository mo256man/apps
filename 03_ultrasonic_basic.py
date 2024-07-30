from gpiozero import DigitalInputDevice, DigitalOutputDevice, LED, Buzzer
import time

trig = DigitalOutputDevice(19)              # GPIO出力
echo = DigitalInputDevice(26)               # GPIO入力
led = LED(18)
buzzer = Buzzer(21)
buzzer.off()

def read_dist():
    # 距離を測定する関数
    trig.on()                               # トリガーをオンにする
    time.sleep(0.00001)                     # 一瞬だけ待つ
    trig.off()                              # トリガーをオフにする

    sig_off = time.time()                   # 時間
    while not echo.is_active:               # エコーがオフの
        sig_off = time.time()               # 時間

    while echo.is_active:                   # エコーがオンになった
        sig_on = time.time()                # 時間

    duration = sig_on - sig_off             # 超音波を出してから届くまでの時間（往復）
    distance = duration * 34000 / 2         # 距離＝往復時間＊音速÷２（単位：cm）
    return distance


while True:                                 # 無限ループ
    dis = read_dist()                       # 距離を測定する
    if dis < 10:                            # 10cm未満ならば
        print(f"too close! {dis:.2f}cm")    # 警告を発する 
        led.on()                            # LED点灯
        buzzer.beep()
    else:
        print(f"distance   {dis:.2f}cm")    # 距離を表示する
        led.off()                           # LEDを消灯する
        buzzer.off()

    time.sleep(0.1)
