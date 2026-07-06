import time
from datetime import datetime
import smbus2
from grove.adc import ADC
import RPi.GPIO as GPIO
import csv
import os
#↑ﾌｧｲﾙ関連、logﾌｧｲﾙ存在確認などの関数を使う為に追加。

LIGHT_SENSOR_PIN = 2 
#↑光センサA2
MOI_SENSOR_PIN = 0
#↑水分センサーA0
WATER_SENSOR_PIN = 16
#↑水センサーD16
WATER_PUMP_PIN = 6
#↑水ポンプD5※5番センサーpinは不使用。

adc = ADC()
GPIO.setmode(GPIO.BCM)
GPIO.setup(WATER_SENSOR_PIN, GPIO.IN)
#↑水センサから信号を受け取る。HIGHで水無Lowで短絡水在り
GPIO.setup(WATER_PUMP_PIN, GPIO.OUT)
#↑入出力の01信号をポンプに出すのでOUT

bus = smbus2.SMBus(1)
DHT20_ADDR = 0x38

log_columns = (f'"年-月-日 時:分:秒","光ｾﾝｻｰ値","温度(℃)","湿度(%)",\
"土中水分ｾﾝｻｰ値","水ﾀﾝｸ内水有無","水ポンプ起動有無","水ポンプ作動時間"')

#↓光センサー実行関数
def get_light_sensor():
    light_value = adc.read(LIGHT_SENSOR_PIN)
    return light_value
#↓温度湿度センサー実行関数
def get_dht20_sensor():
    bus.write_i2c_block_data(DHT20_ADDR, 0xAC, [0x33, 0x00])
    time.sleep(0.1)
    data = bus.read_i2c_block_data(DHT20_ADDR, 0x71, 7)
    #print(data)
    humi_raw = ((data[ 1 ] << 12) | (data[ 2 ] << 4) | (data[ 3 ] >> 4))
    temp_raw = (((data[ 3 ] & 0x0F) << 16) | (data[ 4 ] << 8) | data[ 5 ])
    #print(humi_raw)
    #print(temp_raw)
    humi = round((humi_raw / 1048576.0) * 100.0, 2)
    temp = round((temp_raw / 1048576.0) * 200.0 - 50.0, 2)
    return temp,humi
#↓土中水分センサー実行関数
def get_moi_sensor():
    moisture_value = adc.read(MOI_SENSOR_PIN)
    return moisture_value
#↓水センサー実行関数
def check_water_sensor():
    is_water_exist = False
    sensor_state = GPIO.input(WATER_SENSOR_PIN)
    if sensor_state == GPIO.LOW:
        return True
    else:
        return False
#↓水ポンプ起動関数
def control_waterpump(is_water_exist=False):
    if is_water_exist:
        print('水ポンプを3秒間起動します...')
        GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
        time.sleep(3)
        #ポンプは空回しし過ぎると痛む為3秒で終了。
    else:
        print('水が無いためポンプを動かせません。')        
        GPIO.output(WATER_PUMP_PIN, GPIO.LOW)

#↓センサー測定値記録関数
def write_sensors_values(*datum):
	now_values = list(datum)
	#↑可変長引数タプルをリスト関数を使いリストに変換
	now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#↑Excelで扱いやすい形で時刻を取得
	now_values.insert(0, now)
	# ↑時刻をリストの先頭（0番目）に追加※listにすればinsertメソッドが使える
	# ↓"a"モードで追記。
	with open ("./sensor_log/sensor_log.csv", "a", newline='', encoding='UTF-8'
	) as file:
		writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
		#↑csvﾌｧｲﾙに書き込む為にwriterｵﾌﾞｼﾞｪｸﾄを生成。
		#ﾃﾞﾌｫﾙﾄ引数(ﾊﾟﾗﾒｰﾀ)quotingにcsv.QUOTE_NONNUMERIC※非数値ﾌｨｰﾙﾄﾞだけを
		#ダブルクォート""で囲う様に記述。
		writer.writerow(now_values)
		#↑各データ書き込みは1ループ1行なのでrowsではなくrowで。
		
		if not os.exists(./sensor_log/sensor_log.csv):
			global log_columns
			writer.wirterow(log_columns)
	

	

print("各センサーの監視を開始します（Ctrl+Cで終了）...")

try:
    while True:
        start_time = time.time()
        
        # 1. データの収集（確実に順番に取得する）
        light_val = get_light_sensor()
        temp_val, humi_val = get_dht20_sensor()
        moi_val = get_moi_sensor()
        water_status = check_water_sensor()
        
        # 2. ターミナルへのログ出力（今後のCSV記録のベース）
        print("-" * 50)
        print(f"光: {light_val} | 温度: {temp_val}℃ | 湿度: {humi_val}% | 土壌水分: {moi_val}")
        # 3. ★CSVファイルへの記録（関数を呼び出し！）
        # 引数として、取得したセンサー値と水位ステータスを順番に渡す
        write_sensors_values(light_val, temp_val, humi_val, moi_val, water_status)
        print("【記録】sensor_log.csv にデータを追記しました。")
        if water_status:
            print("タンク水位: 【正常】水あり")
        else:
            print("タンク水位: 【異常】水切れ！！")
            
        # 3. ポンプの自律制御
        # ※本来は「土壌が乾いた時」かつ「タンクに水がある時」に動かしますが、
        # 今回は統合テストのため、タンクに水があれば毎回3秒動かす仕様にしています。
        control_waterpump(water_status)
        
        end_time = time.time()
        print(f"処理時間: {round(end_time - start_time, 3)}秒")
        print("-" * 50)
        
        # 次の監視まで待機
        time.sleep(1)
        
except KeyboardInterrupt:
    print("各センサー監視とポンプの起動を終了します。")

finally:
    print("ピンの占有を解放します。")
    GPIO.cleanup()

'''実行結果：2026年6月23日16時17分記録
pi@raspberrypi:~/share/development20260622~ $ python3 20260623_write_sensor_log_test.py
各センサーの監視を開始します（Ctrl+Cで終了）...
--------------------------------------------------
光: 16 | 温度: 27.1℃ | 湿度: 40.95% | 土壌水分: 0
【記録】sensor_log.csv にデータを追記しました。
タンク水位: 【異常】水切れ！！
水が無いためポンプを動かせません。
処理時間: 0.104秒
--------------------------------------------------
--------------------------------------------------
光: 16 | 温度: 27.1℃ | 湿度: 40.89% | 土壌水分: 0
【記録】sensor_log.csv にデータを追記しました。
タンク水位: 【異常】水切れ！！
水が無いためポンプを動かせません。
処理時間: 0.104秒
--------------------------------------------------
--------------------------------------------------
光: 15 | 温度: 27.09℃ | 湿度: 40.83% | 土壌水分: 0
【記録】sensor_log.csv にデータを追記しました。
タンク水位: 【異常】水切れ！！
水が無いためポンプを動かせません。
処理時間: 0.104秒
--------------------------------------------------
--------------------------------------------------
光: 16 | 温度: 27.1℃ | 湿度: 40.76% | 土壌水分: 0
【記録】sensor_log.csv にデータを追記しました。
タンク水位: 【異常】水切れ！！
水が無いためポンプを動かせません。
処理時間: 0.104秒
--------------------------------------------------
--------------------------------------------------
光: 17 | 温度: 27.09℃ | 湿度: 40.71% | 土壌水分: 0
【記録】sensor_log.csv にデータを追記しました。
タンク水位: 【異常】水切れ！！
水が無いためポンプを動かせません。
処理時間: 0.104秒
--------------------------------------------------
--------------------------------------------------
光: 16 | 温度: 27.06℃ | 湿度: 40.68% | 土壌水分: 0
【記録】sensor_log.csv にデータを追記しました。
タンク水位: 【異常】水切れ！！
水が無いためポンプを動かせません。
処理時間: 0.109秒
--------------------------------------------------
--------------------------------------------------
光: 17 | 温度: 27.11℃ | 湿度: 40.63% | 土壌水分: 0
【記録】sensor_log.csv にデータを追記しました。
タンク水位: 【異常】水切れ！！
水が無いためポンプを動かせません。
処理時間: 0.109秒
--------------------------------------------------
^C各センサー監視とポンプの起動を終了します。
ピンの占有を解放します。
'''
