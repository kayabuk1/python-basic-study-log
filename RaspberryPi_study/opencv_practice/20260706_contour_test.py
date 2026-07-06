from picamera2 import Picamera2
import cv2,time

def show_small(winname, img, width=640):
	h,w = img.shape[:2]
	scale = width/w
	cv2.imshow(winname, cv2.resize(img, (width, int(h*scale))))
	
def main():
	cam = Picamera2()
	cam.configure(cma.create_preview_configuration(main={"size":(640, 360)}))
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
		gray = cv2.cvtColor(flame, cv2.COLOR_BGR2GRAY)
		
		#↓二値化（黒物体を白にする為に Otsu+INVを使用）
		_, binary = cv2.threshold(
			gray, 0, 255, 
			cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
		)
		#↓最外輪郭のみ抽出
		contours,_ = cv2.findContours(
			binary, cv2.RETR_EXTERNAL, cv2CHAIN_APPROX_SIMPLE
		)
		#↓輪郭描画
		vis = frame.copy()
		cv2.drawContours(vis, contours, -1, (0,0,255), 2)
		cv2.putText(
			vis, f'Contours:{len(contours)}',(10, 28), 
			cv2.FONT_HIRSHY_SIMPLEX, 0.8, (0, 200, 255), 2
		)
		
		#縮小表示（見やすさのため）
		show_small()
	