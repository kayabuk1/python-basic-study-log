import ambient
import board
import adafruit_ahtx0
import time

am = ambient.Ambient(101418, "715d2714311951f3")
i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

while(True):
	temp = sensor.temperature
	humid = sensor.relative_humidity
	r = am.send({"d1":temp, "d2":humid})
	# 【追加】この1行で、システムの稼働状況をターミナルに吐き出させ       
	print(f"送信完了: 戻り値 {r.status_code} / 温度: {temp}度, 湿度: {humid}%")
	time.sleep(10)
