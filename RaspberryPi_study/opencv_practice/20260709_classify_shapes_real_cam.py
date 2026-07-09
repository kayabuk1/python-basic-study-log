from picamera2 import Picamera2
import cv2
import numpy as np
import time

IMG_SIZE = 32
labels = {0: "circle", 1: "square", 2: "triangle"}

# 作成した学習済みモデルを読み込む
knn = cv2.ml.KNearest_load("shape_knn_model.yml")

picam2 = Picamera2()
picam2.configure(
	picam2.create_preview_configuration(
		main={"size": (640, 360)}
	)
)

picam2.start()
time.sleep(0.3)

try:
	sw, sh = picam2.camera_properties["PixelArraySize"]
	picam2.set_controls({"ScalerCrop": (0, 0, int(sw), int(sh))})
except:
	picam2.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})
	
print("推論開始（qで終了）")

while True:
	frame = picam2.capture_array()
	bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
	gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

	# 中央部分だけ使う（撮影時と同じ領域）
	h, w = gray.shape[:2]
	x1, y1 = w//4, h//4
	x2, y2 = w*3//4, h*3//4
	roi = gray[y1:y2, x1:x2]
	
	# 推論用にリサイズ＆ベクトル化
	resized = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))
	vec = resized.flatten().astype(np.float32).reshape(1, -1)
	
	# 推論（k=3 の多数決）
	ret, results, neighbours, dist = knn.findNearest(vec, k=3)
	label_id = int(results[0][0])
	name = labels[label_id]
	
	# 結果表示
	cv2.rectangle(bgr, (x1,y1), (x2,y2), (0,255,255), 2)
	cv2.putText(bgr, f"Detected: {name}", (20,50),
		cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255), 2)
	cv2.imshow("Shape Classification (Real Camera)", bgr)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
cv2.destroyAllWindows()
picam2.stop()