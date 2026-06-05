import time
import smbus2
'''
SMBusはSystem Management Busの略。1995年にintel社によって提唱。
Q.も少しsmbus2について詳しく解説して欲しい。
'''
import subprocess
import RPi.GPIO as GPIO

LED_PIN = 25

GPIO.setmode(GPIO.BCM)
#BroadCom社制のCPUチップが使われているので、その仕様でPINを制御するように命令。
GPIO.setup(LED_PIN, GPIO.OUT)

# 1. インフラの準備：1番のI2C配管を開き、DHT20の内線番号（0x38）
#をロックオン
bus = smbus2.SMBus(1)
'''
ラズパイから物理的に生えている「1番のI2C配管（SDA1/SCL1ピン）」のバルブを開き、通信の準備をします

'''
ADDR = 0x38
ADDR2 = 0x19

print("I2C直結でDHT20の使用を開始します...")
print("終了するには Ctrl+C を押してください。")
print("3軸加速度センサーの監視を開始します...")

# 1. 前回の状態を記憶しておくための箱（ソフトウェア・フリップフロップ）を用意
prev_x, prev_y, prev_z = 0, 0, 0
THRESHOLD = 1.0  # これ以上数値が変化したら「動いた」とみなす閾値（感度）
try:
    while True:
        # 2. トリガー：測定開始コマンド（0xAC, 0x33, 0x00）を送信
        bus.write_i2c_block_data(ADDR, 0xAC, [ 0x33, 0x00 ])
        # 2. センサーから現在の X, Y, Z の加速度を取得する
        curr_x, curr_y, curr_z = get_acceleration()  # ※実際の取得関数に置き換えます
        
        # 測定完了を待つ
        time.sleep(0.1)
        
        # 3. データの吸い上げ：生データ（7バイト）を読み出す
        data = bus.read_i2c_block_data(ADDR, 0x71, 7)
        # 3. 「現在の値」と「前回の値」の差（絶対値）を計算する
        diff_x = abs(curr_x - prev_x)
        diff_y = abs(curr_y - prev_y)
        diff_z = abs(curr_z - prev_z)
        
        # 4. 翻訳（ビット演算）
        # ※システムの表示バグを回避するため、括弧の中にスペースを入れています
        # 湿度は 1番, 2番, 3番の上半分 に格納されている
        humi_raw = ((data[ 1 ] << 12) | (data[ 2 ] << 4) | (data[ 3 ] >> 4))
        
        # 温度は 3番の下半分, 4番, 5番 に格納されている
        temp_raw = (((data[ 3 ] & 0x0F) << 16) | (data[ 4 ] << 8) | data[ 5 ])
        
        # 復元した数値を、人間が読める「％」と「℃」に計算し直す
        humi = (humi_raw / 1048576.0) * 100.0
        temp = (temp_raw / 1048576.0) * 200.0 - 50.0
        
        # 取得した値を表示
        print(f"温度: {temp:.1f} ℃,  湿度: {humi:.1f} %")
        
        if temp >= 25:
        	GPIO.output(LED_PIN, GPIO.HIGH)
        	subprocess.run(F"/home/pi/share/aquestalkpi/AquesTalkPi -p '現在の温度は{temp:.1f}度だよ！湿度は{humi:.1f}だよ！' | aplay -D plughw:2,0", shell=True)
        elif temp < 25:
        	GPIO.output(LED_PIN, GPIO.LOW)
                # 4. 変化量の合計が閾値を超えたら「動いた！」と判定
        if (diff_x + diff_y + diff_z) > THRESHOLD:
            print("警告：センサーの動きを検知しました！")
            
            # AquesTalkPi ＋ aplay (plughw) の安全配管で喋らせる！
            cmd = "/home/pi/share/aquestalkpi/AquesTalkPi -p '動いています' | aplay -D plughw:2,0"
            subprocess.run(cmd, shell=True)
            
            # 連続で喋りすぎてシステムがパニックにならないよう、3秒ほど待機
            time.sleep(3)
        # 5. 次のループのために、現在の値を「前回の値」として記憶（上書き）させる
        prev_x = curr_x
        prev_y = curr_y
        prev_z = curr_z
        
        time.sleep(10)

except KeyboardInterrupt:
	GPIO.cleanup()
	print("\n安全に終了しました。")
