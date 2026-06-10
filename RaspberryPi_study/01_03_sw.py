import RPi.GPIO as GPIO
from time import sleep

LED_PIN = 25
SW_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SW_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(SW_PIN) == GPIO.HIGH:
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
        sleep(0.01)

finally:
    print("終了処理を実行し、ピンを解放します")
    GPIO.cleanup()