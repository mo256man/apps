from gpiozero import LED, Button
import time

led = LED(18)
switch = Button(23)

while True:
    if switch.value:
        led.on()
    else:
        led.off()
