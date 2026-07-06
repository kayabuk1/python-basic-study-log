from picamera2 import Picamera2
import cv2, time
# Haar Cascade（学習済み分類器）のパス
cascade_path =\
 "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
#↑人間の正面顔の光と影のパターンを数値化した辞書（XMLファイル）の物理的な保存場所
#（パス）を変数に代入。
#●そういえば何故画像の明暗の数値のファイルが、csvやjsonなどではなく、
#xmlファイルなのでしょうか？
face_cascade = cv2.CascadeClassifier(cascade_path)
#cv2.CascadeClassifier()※cv2と言う画像処理ｴﾝｼﾞﾝﾊﾟｯｹｰｼﾞのCascadeClassifierクラス
#※先頭が大文字なのはpythonでのクラス命名規則、を使い、
#その辞書データをOpenCVのシステムに引数として読み込ませてインスタンス化。
#これにより、face_cascade という変数は
#「顔のパターンを完全に記憶した分類機としてインスタンス化（実体化）される。
#●cascadeという言葉が使われているのは何故？

#↓お決まりの安全なカメラ起動処理
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
	#●↑cvtとは何の略？
	#●arrayと配列になっているのは、画像はrgbの数値配列ということ？
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#↑Haar Cascadesは明暗のｺﾝﾄﾗｽﾄでのみ顔を判断するｱﾙｺﾞﾘｽﾞﾑなので色は不要。
	
	# 顔検出（複数OK）
	faces = face_cascade.detectMultiScale(
	#↑１０行目で作った顔分類用のインスタンスに現在の画像grayを渡して顔を探す
		gray,
		scaleFactor=1.2, # 小さいほど精度↑/計算↑
		minNeighbors=5, # 誤検出を抑える（大きいほど厳しい）
		minSize=(30, 30) # 最小サイズ（遠くの顔→小さく）
	)
	
	# 顔に番号ラベルを描画 ＊＊ここから＊＊
	for i, (x, y, w, h) in enumerate(faces, start=1):
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2) # 顔枠cv2.putText(frame, f“Face {i}”, (x, max(0, y-8)), # 番号cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
	# 総数を表示
	cv2.putText(frame, f"Detected: {len(faces)}",
		(10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
	cv2.imshow("Face Numbering", frame)
	# qで終了 ＊＊ここ以降は同じ＊＊
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows(); cam.stop()

'''

'''