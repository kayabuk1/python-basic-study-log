import RPi.GPIO as GPIO
import time

WATER_PUMP_PIN = 6
#↑GroveHatのD5は物理？5番ピンと6番ピンがセットになっている。
#  背面シール確認した所PUMPは6番になる。INで1でポンプON、0でポンプOFF
#  5番がOUTでセンサー

GPIO.setmode(GPIO.BCM)
GPIO.setup(WATER_PUMP_PIN, GPIO.OUT)
#↑入出力の01信号をポンプに出すのでOUT

try:
	print('水ポンプを起動します...')
	GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
	time.sleep(3)
	#ポンプは空回しし過ぎると痛む為3秒で終了。
	GPIO.output(WATER_PUMP_PIN, GPIO.LOW)
finally:
	print('水ポンプテストを終了し、ピンを解放します。')
	GPIO.cleanup()
'''2026年6月22日15時56分
水ポンプを起動します...
水ポンプテストを終了し、ピンを解放します。
無事ポンプの起動に成功。
'''

