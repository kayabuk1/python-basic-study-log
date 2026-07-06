from picamera2 import Picamera2
import cv2,time
import numpy as np

def show_small(winname, img, width=640):
	#↓等比で縮小表示
	h,w = img.shape[:2]
	scale = width/w
	cv2.imshow(winname, cv2.resize(img, (width, int(h*scale))))
	
def classify_shape(cnt):
	#輪郭から図形名と近似多角形を返す(小ノイズは除外)
	area = cv2.contourArea(cnt)
	#↓小さい面積を除外する事でノイズを除外
	if area<80: return None, None
	peri = cv2.arcLength(cnt, True)
	approx = cv2.approxPolyDP(cnt, 0.02*peri, True) #←近似精度=周長の2%
	v = len(approx)
	if v==3:
		name = "Triangle"
	elif v==4:
		x,y,w,h = cv2.boundingRect(approx)
		aspect = w/float(h)
		name = "Square" if 0.90<=aspect<=1.10 else "Rectangle"
	else:
		circ = (4.0*np.pi*area/(peri*peri)) if peri>0 else 0 #1に近い程円
		name = "Circle" if circ >0.80 else "Polygon"
	return name, approx
	
def main():
	cam = Picamera2()
	cam.configure(cam.create_preview_configuration(main={"size":(640, 360)}))
	cam.start()
	time.sleep(0.2) #←起動安定の為少しだけ時間を待つ
	
	try:
		sw, sh = cam.camera_properties["PixelArraySize"]
		cam.set_controls({"ScalerCrop":(0, 0, int(sw), int(sh))})	
	except:
		cam.set_controls({"ScalerCrop":(0, 0, 2592, 1944)})
		
	while True:
		#↓フレーム取得→RGB→BGR→GRAY
		frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray, (3, 3), 0.8)
		_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
		
		#↓二値化（黒物体を白にする為に Otsu+INVを使用）
		_, binary = cv2.threshold(
			gray, 0, 255, 
			cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
		)
		#↓最外輪郭のみ抽出
		contours,_ = cv2.findContours(
			binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
		)
		#↓図形分類と描画
		counts = {"Triangle":0, "Square":0, "Rectangle":0, "Circle":0, "Polygon":0}
		vis = frame.copy()
		cv2.drawContours(vis, contours, -1, (0,0,255), 2)
		cv2.putText(
			vis, f'Contours:{len(contours)}',(10, 28), 
			cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2
		)
		for c in contours:
			name, approx = classify_shape(c)
			if not name:continue
			counts[name] = counts.get(name, 0) + 1
			cv2.drawContours(vis, [approx], -1, (0,0,255), 2) #赤：輪郭
			x,y,w,h = cv2.boundingRect(approx)
			cv2.putText(vis, name, (x,y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,50,255), 2)
		
		#集計表示
		summary = f"Tri:{counts['Triangle']} Sq:{counts['Square']} Rect:{counts['Rectangle']}\
		Cir:{counts['Circle']} Poly:{counts['Polygon']}" 
		cv2.putText(vis, summary, (10,28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 180,255), 2)
		
		#縮小表示（見やすさのため）
		show_small("Binary(INV+Otsu)", binary, 480)
		show_small("Detected Contours", vis, 640)
		show_small("Shape Detection (Live)", vis, 640)
		
		# s:保存 / q:終了
		key = cv2.waitKey(1)&0xFF
		if key == ord('s'):
			cv2.imwrite("contours_frame.jpg", vis)
			print("Saved: contours_frame.jpg")
		if key == ord('q'):
			brak
	
	cv2.destoryALLWindows()
	cam.stop()
	
if __name__=="__main__"	:
	main()
	