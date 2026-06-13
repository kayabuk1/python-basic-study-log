from flask import Flask
from flask import render_template
from flask import redirect
import subprocess
import time
import smbus2
import RPi.GPIO as GPIO
from datetime import datetime

bus = smbus2.SMBus(1)
ADDR = 0x38
LED25_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED25_PIN, GPIO.OUT)
start = 0.0

app = Flask(__name__)

@app.route("/")
def hello_world():
	# 2. トリガー：測定開始コマンド（0xAC, 0x33, 0x00）を送信
	bus.write_i2c_block_data(ADDR, 0xAC, [ 0x33, 0x00 ])
	# 測定完了を待つ
	time.sleep(0.1)
	# 3. データの吸い上げ：生データ（7バイト）を読み出す
	data = bus.read_i2c_block_data(ADDR, 0x71, 7)
	# 4. 翻訳（ビット演算）
	# ※システムの表示バグを回避するため、括弧の中にスペースを入れています
	# 湿度は 1番, 2番, 3番の上半分 に格納されている
	humi_raw = ((data[ 1 ] << 12) | (data[ 2 ] << 4) | (data[ 3 ] >> 4))
	# 温度は 3番の下半分, 4番, 5番 に格納されている
	temp_raw = (((data[ 3 ] & 0x0F) << 16) | (data[ 4 ] << 8) | data[ 5 ])
	# 復元した数値を、人間が読める「％」と「℃」に計算し直す
	humi = round((humi_raw / 1048576.0) * 100.0, 2)
	temp = round((temp_raw / 1048576.0) * 200.0 - 50.0, 2)
	outputs = {"temp":temp, "humi":humi}
	end = time.time()
	if end-start > 1:
		GPIO.output(LED25_PIN, GPIO.LOW)
	return render_template("04_02_scamera.php",values=outputs)
@app.route("/scamera/off")
def scamera_off():
	cmd_off = "killall mjpg_streamer"
	subprocess.run(cmd_off, shell=True)
	return redirect("/")
@app.route("/scamera/on")
def scamera_on():
	cmd_on = "cd /home/pi/mjpg-streamer/mjpg-streamer-experimental && ./mjpg_streamer -o './output_http.so -w ./www -p 8080' -i './input_uvc.so -d /dev/video1 -r 1920x1080 -fps 30 -q 10' > /dev/null 2>&1 &"
	subprocess.run(cmd_on, shell=True)
	return redirect("/")
@app.route("/alert/on")
def alert_on():
	global start
	start = time.time()
	GPIO.output(LED25_PIN, GPIO.HIGH)
	subprocess.run("cd /home/pi/share/aquestalkpi && ./AquesTalkPi -p '監視カメラ映像録画中です。近づかず立ち去ってください。' | aplay -D hw:2,0",shell=True)
	return redirect("/")
@app.route("/snap/on")
def snap_on():
	# 1. Pythonで現在時刻を取得し、「20260613_153000」のような文字列を作る
	now = datetime.now().strftime('%Y%m%d_%H%M%S')
	# 2. wgetコマンドを使って、mjpg_streamerから画像をダウンロードし、名前を付けて保存
	cmd_snap = f"wget http://127.0.0.1:8080/?action=snapshot -O /home/pi/share/scamera_pic/pic_{now}.jpg"
	# 3. サブプロセスで実行
	subprocess.run(cmd_snap, shell=True)
	print('画像を撮影しました')
	return redirect("/")
if __name__=="__main__":
	app.debug=True
	app.run(host="0.0.0.0", port=8000)