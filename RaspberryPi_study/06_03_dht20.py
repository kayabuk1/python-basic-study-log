import time
import seeed_dht

# 初期化：DHT20センサーにアクセスする
# ※ライブラリのバグ（ピン番号を要求される）を回避するため、
# ダミーのピン番号として「I2Cのバス番号である 1」を渡してシステムを騙す！
sensor = seeed_dht.DHT("20", 1)

print("温湿度データの取得を開始します。")
print("終了するには Ctrl+C を押してください。")

# 無限ループと防弾装甲（強制終了時の安全対策）の型
try:
    while True:
        # センサーから湿度(humi)と温度(temp)を読み取る
        humi, temp = sensor.read()
        
        # 取得したデータを分かりやすくターミナルに表示する
        print('温度: {} ℃, 湿度: {} %'.format(temp, humi))
        
        # 連続で問い合わせてシステムがパニックにならないよう、1秒待機
        time.sleep(1)

except KeyboardInterrupt:
    # Ctrl+C が押されたら、ここを通過して安全にプログラムを終了する
    print("\nシステムを安全に終了しました。")
