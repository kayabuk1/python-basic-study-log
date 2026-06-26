from picamera2 import Picamera2
import cv2


def nothing(x):
    pass


def main():
    # カメラを初期化「.configure」※640x480でプレビュー
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(main={"size": (640, 480)}))
    cam.start()

    # デジタルズームを解除(ｶﾒﾗｾﾝｻの物理的な最大解像度を取得)
    try:
        sw, sh = cam.camera_properties["PixelArraySize"]
        cam.set_controls({"ScalerCrop": (0, 0, int(sw), int(sh))})
    except Exception:
        cam.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})

    #Cannyパラメータ設定用スライダー
    cv2.namedWindow("Controls")
    cv2.createTrackbar("Low", "Controls", 50, 255, nothing)
    cv2.createTrackbar("High", "Controls", 150, 255, nothing)

    while True:
        # 撮影したカメラ画像RGBをBGRに並び替え
        frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)
        # グレースケール変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #ぼかし（ノイズ低減）
        blur = cv2.GaussianBlur(gray, (5,5), 1.0)
        
        #Trackbarの値を取得
        low = cv2.getTrackbarPos("Low", "Controls")
        high = cv2.getTrackbarPos("High", "Controls")
        high = max(high, low+1) #Highはlowより大きく

        #Cannyエッジ検出
        edges = cv2.Canny(blur, low, high)

        # 表示
        cv2.imshow("Original", frame)
        cv2.imshow("Blurred", blur)
        cv2.imshow("Edges", edges)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # 終了処理opencvで表示した全ウインドを閉じてメモリを解放
    cv2.destroyAllWindows()
    cam.stop()


if __name__ == "__main__":
    main()
