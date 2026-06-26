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

    cv2.namedWindow("Controls")
    cv2.createTrackbar("Manual TH", "Controls", 128, 255, nothing)

    while True:
        # 撮影したカメラ画像RGBをBGRに並び替え
        frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)
        # グレースケール変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 手動閾値設定
        th = cv2.getTrackbarPos("Manual TH", "Controls")
        _, bin_manual = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)

        # Otus(二値化＋自動しきい値)
        _, bin_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 適応二値化（局所的に判定）
        bin_adp = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # "Camera"という名前のウインドウにBGRに変換したフレームを表示
        cv2.imshow("Original", frame)
        cv2.imshow("Gray", gray)
        # 表示
        cv2.imshow("Manual", bin_manual)
        cv2.imshow("Otsu", bin_otsu)
        cv2.imshow("Adaptive", bin_adp)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            cv2.imwrite("bin_manual.jpg", bin_manual)
            cv2.imwrite("bin_otsu.jpg", bin_otsu)
            cv2.imwrite("bin_adaptive.jpg", bin_active)
            print("Saved:frame.jpg")
        elif key == ord("q"):
            break

    # 終了処理opencvで表示した全ウインドを閉じてメモリを解放
    cv2.destroyAllWindows()
    cam.stop()


if __name__ == "__main__":
    main()
