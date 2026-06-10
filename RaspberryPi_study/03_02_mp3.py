import subprocess
import RPi.GPIO as GPIO
from time import sleep

SW_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(SW_PIN, GPIO.IN)

try:
	while True:
		if GPIO.input(SW_PIN)==GPIO.HIGH:
			subprocess.run("/home/pi/share/aquestalkpi/AquesTalkPi -p 'あーマイクテストテスト' | aplay", shell=True)
		else:
			print('SW_ON!!')
		sleep(1)
finally:
	GPIO.cleanup()
