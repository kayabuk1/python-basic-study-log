import time
import smbus2

# 1. インフラの準備：1番のI2C配管を開き、DHT20の内線番号（0x38）をロックオン
bus = smbus2.SMBus(1)
ADDR = 0x38

print("I2C直結でDHT20のハッキングを開始します...")
print("終了するには Ctrl+C を押してください。")

try:
    while True:
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
        humi = (humi_raw / 1048576.0) * 100.0
        temp = (temp_raw / 1048576.0) * 200.0 - 50.0
        
        # 取得した値を表示
        print(f"温度: {temp:.1f} ℃,  湿度: {humi:.1f} %")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\nハッキングを安全に終了しました。")
