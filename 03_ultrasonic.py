from gpiozero import DistanceSensor, LED, Buzzer
import time

sensor = DistanceSensor(trigger=19, echo=26)
led = LED(18)
buzzer = Buzzer(21)

while True:
    dis = sensor.distance * 100				# 100倍するとcmになる

    if dis < 10:                            # 10cm未満ならば
        print(f"too close! {dis:.2f}cm")    # 警告を発する 
        led.on()                            # LED点灯
        buzzer.beep()
    elif dis < 100:                         # 100cm未満ならば
        print(f"distance   {dis:.2f}cm")    # 距離を表示する
        led.off()                           # LEDを消灯する
        buzzer.off()
                                            # （それ以上ならば特に何もしない）
    time.sleep(0.5)

