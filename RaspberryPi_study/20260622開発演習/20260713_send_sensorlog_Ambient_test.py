import time
from datetime import datetime
import smbus2
from grove.adc import ADC
import RPi.GPIO as GPIO
import csv
import os
#↑ﾌｧｲﾙ関連、logﾌｧｲﾙ存在確認などの関数を使う為に追加。
import json
import ambient
with open("./ambientID_writeKEY.json") as file:
    data = json.load(file)
    amibientID = data["ambientID"]
    ambientW_KEY = data["ambientW_KEY"]
am_writer = ambient.Ambient(ambientID, ambientW_KEY)

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

log_columns = ["年-月-日 時:分:秒","光ｾﾝｻｰ値","温度(℃)","湿度(%)",\
"土中水分ｾﾝｻｰ値","水ﾀﾝｸ内水有無","水ポンプ起動有無","水ポンプ作動時間"]

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
        starttime = time.time()
        GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
        time.sleep(3)
        endtime = time.time()
        totaltime = endtime - starttime
        wpump_ifstart = "水ポンプ起動"
        return wpump_ifstart, totaltime
        #ポンプは空回しし過ぎると痛む為3秒で終了。
    else:
        print('水が無いためポンプを動かせません。')        
        GPIO.output(WATER_PUMP_PIN, GPIO.LOW)
        wpump_ifstart = "水ポンプ不起動"
        totaltime = None
        return wpump_ifstart,totaltime

#↓センサー測定値記録関数
def write_sensors_values(*datum):
    now_values = list(datum)
    #↑可変長引数タプルをリスト関数を使いリストに変換
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #↑Excelで扱いやすい形で時刻を取得
    now_values.insert(0, now)
    # ↑時刻をリストの先頭（0番目）に追加※listにすればinsertメソッドが使える
    # ↓"a"モードで追記。
    
    filename = "./sensor_log/sensor_log.csv"
    file_exists = os.path.exists(filename)
    #↑ﾌｧｲﾙを開く前に存在確認をする。TrueかFalseが返って来る。
    
    with open ("./sensor_log/sensor_log.csv", "a", newline='', encoding='UTF-8'
    ) as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        #↑csvﾌｧｲﾙに書き込む為にwriterｵﾌﾞｼﾞｪｸﾄを生成。
        #ﾃﾞﾌｫﾙﾄ引数(ﾊﾟﾗﾒｰﾀ)quotingにcsv.QUOTE_NONNUMERIC※非数値ﾌｨｰﾙﾄﾞだけを
        #ダブルクォート""で囲う様に記述。
        
        #↓一番最初に書き込みする時=logﾌｧｲﾙが存在しない時、項目名を書き込み。
        if not file_exists:
            writer.writerow(log_columns)
            #↑グローバル変数は参照するだけならglobalは要らない。
        
        writer.writerow(now_values)
        #↑各データ書き込みは1ループ1行なのでrowsではなくrowで。
    

    

print("各センサーの監視を開始します（Ctrl+Cで終了）...")

try:
    while True:
        start_time = time.time()
        
        # 1. データの収集（確実に順番に取得する）
        light_val = get_light_sensor()
        temp_val, humi_val = get_dht20_sensor()
        moi_val = get_moi_sensor()
        water_status = check_water_sensor()
        if water_status:
            w_st_forhuman = "タンク内水有"
        else:
            w_st_forhuman = "タンク内水無" 
        
        # ポンプの自律制御 記録書き込み前にreturnを受け取る為に位置を変更
        # ※本来は「土壌が乾いた時」かつ「タンクに水がある時」に動かしますが、
        # 今回は統合テストのため、タンクに水があれば毎回3秒動かす仕様にしています。
        wpump_ifstart,totaltime = control_waterpump(water_status)
        
        # 2. ターミナルへのログ出力（今後のCSV記録のベース）
        print("-" * 50)
        print(f"光: {light_val} | 温度: {temp_val}℃ | 湿度: {humi_val}% | 土壌水分: {moi_val}")
        # 3. ★CSVファイルへの記録（関数を呼び出し！）
        # 引数として、取得したセンサー値と水位ステータスを順番に渡す
        sensor_values = (
            light_val, temp_val, humi_val, moi_val, w_st_forhuman, wpump_ifstart,
            round(totaltime, 2))
        write_sensors_values(sensor_values)
        print("【記録】sensor_log.csv にデータを追記しました。")
        
        #Ambientにデータを送信する。辞書型に直す必要がある。
        ambient_data = {}
        for k,v in zip(log_columns, sensor_values):
            ambient_data[k] = v
        print(ambient_data) #デバック用
        
        if water_status:
            print("タンク水位: 【正常】水あり")
        else:
            print("タンク水位: 【異常】水切れ！！")
            

        
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

'''実行結果：2026年7月13日14時40分分記録
各センサーの監視を開始します（Ctrl+Cで終了）...
水ポンプを3秒間起動します...
--------------------------------------------------
光: 0 | 温度: 25.61℃ | 湿度: 49.86% | 土壌水分: 0
【記録】sensor_log.csv にデータを追記しました。
タンク水位: 【正常】水あり
処理時間: 3.104秒
--------------------------------------------------
水ポンプを3秒間起動します...
--------------------------------------------------
光: 0 | 温度: 25.63℃ | 湿度: 49.62% | 土壌水分: 0
【記録】sensor_log.csv にデータを追記しました。
タンク水位: 【正常】水あり
処理時間: 3.106秒
--------------------------------------------------
水ポンプを3秒間起動します...
^C各センサー監視とポンプの起動を終了します。
ピンの占有を解放します。

"年-月-日 時:分:秒","光ｾﾝｻｰ値","温度(℃)","湿度(%)","土中水分ｾﾝｻｰ値","水ﾀﾝｸ内水有無","水ポンプ起動有無","水ポンプ作動時間"
"2026-07-06 16:04:27",9,27.09,37.72,0,False
"2026-07-06 16:04:28",9,27.1,37.72,0,False
"2026-07-06 16:04:29",9,27.05,37.72,0,False
"2026-07-13 13:49:57",8,24.94,54.45,0,"タンク内水無"
"2026-07-13 13:49:58",10,24.94,54.46,0,"タンク内水無"
"2026-07-13 13:49:59",7,24.96,54.47,0,"タンク内水無"
"2026-07-13 13:50:00",9,24.97,54.46,0,"タンク内水無"
"2026-07-13 14:34:32",5,25.49,52.33,0,"タンク内水無","水ポンプ不起動",""
"2026-07-13 14:34:33",3,25.48,52.42,0,"タンク内水無","水ポンプ不起動",""
"2026-07-13 14:34:34",4,25.5,52.43,0,"タンク内水無","水ポンプ不起動",""
"2026-07-13 14:34:35",3,25.49,52.57,0,"タンク内水無","水ポンプ不起動",""
"2026-07-13 14:37:05",0,25.53,52.31,0,"タンク内水無","水ポンプ不起動",""
"2026-07-13 14:37:06",0,25.54,52.17,0,"タンク内水無","水ポンプ不起動",""
"2026-07-13 14:37:07",0,25.53,52.03,0,"タンク内水無","水ポンプ不起動",""
"2026-07-13 14:37:26",0,25.58,50.73,0,"タンク内水無","水ポンプ不起動",""
"2026-07-13 14:37:27",0,25.6,50.79,0,"タンク内水無","水ポンプ不起動",""
"2026-07-13 14:39:24",0,25.61,49.86,0,"タンク内水有","水ポンプ起動",-3.0000839233398438
"2026-07-13 14:39:28",0,25.63,49.62,0,"タンク内水有","水ポンプ起動",-3.000122547149658
【修正】
"2026-07-13 14:48:59",0,25.33,45.43,0,"タンク内水有","水ポンプ起動",3.0
"2026-07-13 14:49:03",0,25.35,45.57,0,"タンク内水有","水ポンプ起動",3.0
"2026-07-13 14:49:07",0,25.35,45.43,0,"タンク内水有","水ポンプ起動",3.0
'''
