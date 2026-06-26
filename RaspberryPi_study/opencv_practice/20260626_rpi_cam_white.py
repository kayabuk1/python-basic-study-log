# 物体検出プログラムのサンプルコード

from picamera2 import Picamera2
import cv2, numpy as np, time


def main():
    # カメラを初期化「.configure」※640x480でプレビュー
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(main={"size": (640, 480)}))
    cam.start()
    time.sleep(0.2)  # 起動安定待ちの為

    # デジタルズームを解除(ｶﾒﾗｾﾝｻの物理的な最大解像度を取得)
    try:
        sw, sh = cam.camera_properties["PixelArraySize"]
        cam.set_controls({"ScalerCrop": (0, 0, int(sw), int(sh))})
    except Exception:
        cam.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})

    min_area = 300  # 小さ過ぎる輪郭は無視
    max_area = 30000  # 外枠など大き過ぎる輪郭を除外

    while True:
        # 撮影したカメラ画像RGBをBGRに並び替え
        frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)
        # グレースケール変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ぼかし（ノイズ低減）
        blur = cv2.GaussianBlur(gray, (5, 5), 1.0)

        binary = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 0
        )

        # 小さなノイズを除去（開演算）
        opened = cv2.morphologyEx(
            binary, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1
        )

        # 最外輪のみ抽出
        contours, _ = cv2.findContours(
            opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        vis = frame.copy()
        count = 0

        # 面積でフィルタし、対象のみ描画
        for c in contours:
            area = cv2.contourArea(c)
            if area < min_area or area > max_area:
                continue
            count += 1
            cv2.drawContours(vis, [c], -1, (0, 0, 255), 2)  # 輪郭を赤に
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 1)  # 矩形を緑に

        # 個数表示
        cv2.putText(
            vis,
            f"Count:{count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 0),
            2,
        )

        # 結果表示
        cv2.imshow("Binary", opened)
        cv2.imshow("Countours", vis)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 終了処理opencvで表示した全ウインドを閉じてメモリを解放
    cv2.destroyAllWindows()
    cam.stop()


if __name__ == "__main__":
    main()
