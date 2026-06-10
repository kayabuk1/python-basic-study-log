import subprocess
import RPi.GPIO as GPIO
from time import sleep

SW_WH_PIN = 24
SW_BK_PIN = 22
SW_GR_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(SW_WH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW_BK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW_GR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
	while True:# メインループ（問題の出題サイクル）
		# ① UI表示：問題文はループの最初で「1回だけ」表示する
		print(
			F'''
			問題：おまえの両親はどれか当ててみな？
			
			白：右の豚
			黒：真ん中の豚
			緑：左の豚
			
			あなたの回答（ボタンを押してください！）
			'''
			)
		subprocess.run("~/share/aquestalkpi/AquesTalkPi -p '問題：おまえの両親はどれか当ててみな？。\
			\
			白、：右の豚、\
			黒、：真ん中の豚、\
			緑、：左の豚、\
			\
			あなたの回答、ボタンを押してください！' | aplay -D hw:2,0",shell=True)
		# ② 監視開始：フラグを作りボタンが押されるまでこの内部ループに閉じ込める
		is_answerd = False
		while is_answerd == False:
			if GPIO.input(SW_WH_PIN)==GPIO.HIGH:
				subprocess.run('mpg321 -a hw:2,0 ok.mp3',shell=True)
				subprocess.run('echo 大おおぅ当たぁありぃぃいい！',shell=True)
				subprocess.run("~/share/aquestalkpi/AquesTalkPi -p 'おおおぅあたぁぁありぃぃいい！' | aplay -D hw:2,0",shell=True)
				is_answerd = True
				#フラグを立てて内部ループを抜ける。
			elif GPIO.input(SW_BK_PIN) == GPIO.HIGH or GPIO.input(SW_GR_PIN) == GPIO.HIGH:
				subprocess.run('mpg321 -a hw:2,0 ng.mp3',shell=True)
				subprocess.run('echo 残念不正解だ',shell=True)
				subprocess.run("~/share/aquestalkpi/AquesTalkPi -p '残念不正解だ' | aplay -D hw:2,0", shell=True)
				is_answerd = True
				#フラグを立てて内部ループを脱出。
			else:
				#待機：ボタンが押されていない時CPUを休ませるためにわずかに待つ。
				sleep(0.1)
		sleep(10)
finally:
	GPIO.cleanup()
			