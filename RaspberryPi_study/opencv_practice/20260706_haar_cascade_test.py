from picamera2 import Picamera2
import cv2, time
# Haar Cascade（学習済み分類器）のパス
cascade_path =
 "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
#↑人間の正面顔の光と影のパターンを数値化した辞書（XMLファイル）の物理的な保存場所
#（パス）を変数に代入。
#●そういえば何故画像の明暗の数値のファイルが、csvやjsonなどではなく、
#  xmlファイルなのでしょうか？
#A.Haar Cascadeのアルゴリズムが発表されたのは2001年。
#  当時は複雑な階層構造（木構造）を持ったデータを保存するための
#  標準的なフォーマットは「XML」しか無かった。
#  複雑な条件分岐のツリー構造を、タグ（<node>〜</node>のような形式）で
#  厳格に入れ子にして記述できるXMLは、機械学習のモデルデータを保存するのに
#  非常に都合が良かった。
face_cascade = cv2.CascadeClassifier(cascade_path)
#cv2.CascadeClassifier()※cv2と言う画像処理ｴﾝｼﾞﾝﾊﾟｯｹｰｼﾞのCascadeClassifierクラス
#※先頭が大文字なのはpythonでのクラス命名規則、を使い、
#その辞書データをOpenCVのシステムに引数として読み込ませてインスタンス化。
#これにより、face_cascade という変数は
#「顔のパターンを完全に記憶した分類機としてインスタンス化（実体化）される。
#●cascadeという言葉が使われているのは何故？
#A.「Cascade」とは英語で「連なった小さな滝」や「数珠つなぎ（連結）」。
#  顔の判定には本来、約6000個もの膨大な特徴量（明暗のパターン）を計算する必要。
#  しかしこれではシステムがパンクしてしまう。
#  そこで、6000個の特徴を「38個のグループ（関門）」に分けられた。
#  第1関門：「とりあえずここ、顔っぽい明暗ある？」➡ 「無い」と判断されたら、
#  即座にその領域の計算を打ち切り（棄却し）、二度と処理しません。
#  第1関門を突破した領域だけが、第2関門、第3関門へと進み、より厳しい
#  チェックを受けます。
#  この次々と関門を抜け、ダメなら即座に下に落とす（処理を捨てる）という流れが、
#  段々に落ちる滝（カスケード）のようであるため、
# 「Cascade of Classifiers（分類器の連結）」と名付けられた。

#↓お決まりの安全なカメラ起動処理
cam = Picamera2()
#↑Raspberry Pi公式のカメラ制御用ライブラリをインスタンス化
cam.configure(cam.create_preview_configuration(main={"size": (640, 360)}))
#↑カメラ設定を顔認識の処理にちょうど良い軽さである「640×360」の解像度に
#設定して構築。
cam.start(); time.sleep(0.2)
try:
	sw, sh = cam.camera_properties["PixelArraySize"]
	#PixelArraySize：カメラセンサーが物理的に持っている「本当の最大ピクセル数」を
	#システムから取り込んで分割代入。w=width,h=heightだけれど、sは？
	cam.set_controls({"ScalerCrop": (0, 0, int(sw), int(sh))})
	#ScalerCrop：通常、カメラは映像の端を少し切り取って（クロップして）
	#デジタルズームをかけた状態で出力しようとする。しかし顔検出では視界（画角）が
	#広い方が有利なため、吸い上げた最大サイズ (0, 0, int(sw), int(sh)) を
	#切り取り範囲として強制指定し、デジタルズームを解除して視野を最大化している。
except:
	cam.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})
	#PixelArraySizeの取得に失敗したら、Raspberry Pi Camera V2の
	#標準的な最大サイズである『2592×1944』を強制適用。

while True:
	frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)
	#●↑cvtとは何の略？→convertの略。cvtColor()は色変換専用メソッド。
	#●arrayと配列になっているのは、画像はrgbの数値配列ということ？
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#↑Haar Cascadesは明暗のｺﾝﾄﾗｽﾄでのみ顔を判断するｱﾙｺﾞﾘｽﾞﾑなので色は不要。
	
	# 顔検出（複数OK）
	faces = face_cascade.detectMultiScale(
	#↑１０行目で作った顔分類用のインスタンスに現在の画像grayを渡して顔を探して
	#変数facesに格納。
		gray,
		scaleFactor=1.2, # 小さいほど精度↑/計算↑
		#●↑scaleFactorは翻訳するとどんな意味？
		minNeighbors=5, # 誤検出を抑える（大きいほど厳しい）
		#●↑なぜNeighborsが誤検出に意味なの？
		minSize=(30, 30) # 最小サイズ（遠くの顔→小さく）
	)
	
	# 顔の枠を描画
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
		#↑見つかった顔の情報が、[x座標,y座標,幅,高さ]というリスト配列の形で
		#格納される。誰もいなければ空のリストになる。
		#●なぜ座標情報も必要なの？
	cv2.imshow("Face Detection", frame)
	# q で終了
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows(); cam.stop()

'''
◆なぜ顔が上下逆さまだと認識されないのか？
Haar Cascade分類器が「顔の物理的な形ではなく、
『光と影の配置パターン（白黒のコントラスト）』を暗記しているだけだから」です。
Haar特徴量： Haar Cascadeは、「人間の目はくぼんでいるから頬よりも暗い」
「目は眉間よりも暗い」といった、顔特有の明暗の配置
（白黒の長方形パターンの組み合わせ）を数千個も計算して「顔っぽさ」を判断しています
。
逆さまによるパターンの崩壊： 顔が上下逆さまになると、
「上が暗くて（目）、下が明るい（頬）」という光のパターンが完全に
ひっくり返ってしまいます。
システムは「学習した正面顔の明暗パターンと一致しないから、
これは顔ではない！」と冷徹に足切りしてしまうのです
。これが、古典的な機械学習モデルの限界（トレードオフ）です。
'''