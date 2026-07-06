from picamera2 import Picamera2
import cv2, time
# Haar Cascade（学習済み分類器）のパス
cascade_path = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

cam = Picamera2()
cam.configure(cam.create_preview_configuration(main={"size": (640, 360)}))
cam.start(); time.sleep(0.2)
try:
	sw, sh = cam.camera_properties["PixelArraySize"]
	cam.set_controls({"ScalerCrop": (0, 0, int(sw), int(sh))})
except:
	cam.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})

while True:
	frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# 顔検出（複数OK）
	faces = face_cascade.detectMultiScale(
		gray,
		scaleFactor=1.2, # 小さいほど精度↑/計算↑
		minNeighbors=5, # 誤検出を抑える（大きいほど厳しい）minSize=(30, 30) # 最小サイズ（遠くの顔→小さく）
	)
	
	# 顔の枠を描画
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
	cv2.imshow("Face Detection", frame)
	# q で終了
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows(); cam.stop()