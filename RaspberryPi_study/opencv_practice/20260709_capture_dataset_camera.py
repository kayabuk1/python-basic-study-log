from picamera2 import Picamera2
import cv2
import time
import os

#保存するディレクトリ名
label = “circle” 
#↑ circle / square / triangle の３つを書き換えて実行

base_dir = "dataset"
save_dir = os.path.join(base_dir, label)
os.makedirs(save_dir, exist_ok=True)

# PiCamera2 初期化（640×360）
picam2 = Picamera2()
picam2.configure(
	picam2.create_preview_configuration(
		main={"size": (640, 360)}
	)
)
picam2.start()
time.sleep(0.2)

#デジタルズーム防止
try:
	sensor_w, sensor_h = picam2.camera_properties["PixelArraySize"]
	picam2.set_controls({"ScalerCrop": (0, 0, int(sensor_w), int(sensor_h))})
except:
	picam2.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})
time.sleep(0.2)

print(f"学習データ撮影開始: label={label}")
print(" [s] 保存 / [q] 終了")

count = len(os.listdir(save_dir))

while True:
	# 生のカメラ画像（保存用）
	rgb = picam2.capture_array()
	raw_bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
	
	# 表示用画像（ガイド表示に使う）
	disp = raw_bgr.copy()
	h, w = disp.shape[:2]

	# ガイド枠の座標（フレーム中央の四角形）
	x1, y1 = w // 4, h // 4
	x2, y2 = w * 3 // 4, h * 3 // 4
	
	# ガイド枠描画（画面表示のみ）
	cv2.rectangle(disp, (x1, y1), (x2, y2), (0,255,255), 2)
	cv2.putText(disp, f"Label: {label} Count: {count}",
		(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
	cv2.putText(disp, "[s]=save [q]=quit",
		(10, h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

	# 表示
	cv2.imshow("Capture Dataset (Crop inside guide)", disp)
	key = cv2.waitKey(1) & 0xFF

	# sキー → ガイド枠の「内側のみ」を保存
	if key == ord('s'):
		cropped = raw_bgr[y1:y2, x1:x2] # ← ここが重要！
		
		filename = os.path.join(save_dir, f"{label}_{count:03d}.jpg")
		cv2.imwrite(filename, cropped)
		print("Saved:", filename)
		count += 1
		
	elif key == ord('q'):
		break
		
cv2.destroyAllWindows()
picam2.stop()