import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 17
instance = dht11.DHT11(pin=17)

date_file = datetime.datetime.now()
with open("./temp_{0:%Y%m%d%H%M%S}.csv".format(date_file),"a") as f:

    try:
        while True:
            result = instance.read()
            restemp = str(datetime.datetime.now()) + ' ,  %-3.1f' % result.temperature + ' , %-3.1f' % result.humidity
            
            if result.is_valid():
                print(restemp)
                print(restemp,file=f)
                f.flush()  # 常時書き込み

            time.sleep(1)

    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()

