import RPi.GPIO as GPIO
from time import sleep
LED_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        sleep(0.5)

finally:
    print("終了処理を実行し、ピンを解放します")
    GPIO.cleanup()