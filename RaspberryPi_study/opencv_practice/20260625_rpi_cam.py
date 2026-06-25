from picamera2 import Picamera2
import cv2


def main():
    # カメラを初期化「.configure」※640x480でプレビュー
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(main={"size": (640, 480)}))
    cam.start()

    # デジタルズームを解除(ｶﾒﾗｾﾝｻの物理的な最大解像度を取得)
    try:
        sw, sh = cam.camera_properties["PixelArraySize"]
        cam.set_controls({"ScalerCrop": (0, 0, init(sw), init(sh))})
    except Exception:
        cam.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})

    while True:
        # 撮影したカメラ画像RGBをBGRに並び替え
        frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)

        # "Camera"という名前のウインドウにBGRに変換したフレームを表示
        cv2.imshow("Cmaera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            cv2.imwrite("frame.jpg", frame)
            print("Saved:frame.jpg")
        elif key == ord("q"):
            break

    # 終了処理opencvで表示した全ウインドを閉じてメモリを解放
    cv2.destroyAllWindows()
    cam.stop()


if __name__ == "__main__":
    main()
