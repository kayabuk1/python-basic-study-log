import subprocess
import RPi.GPIO as GPIO
from time import sleep

SW_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(SW_PIN, GPIO.IN)

try:
	while True:
		if GPIO.input(SW_PIN)==GPIO.HIGH:
			subprocess.run(['rpicam-still','-o','pic1.jpg'])
		else:
			print("SW ON!!")
		sleep(1)
finally:
	GPIO.cleanup()
