import cv2
import numpy as np
import os

IMG_SIZE = 32 # 学習用に縮小（32×32が軽くて速い）

labels = {"circle": 0, "square": 1, "triangle": 2}

train_data = []
train_labels = []

for name, label in labels.items():
	folder = f"./dataset/{name}"
	print("Loading:", folder)
	for filename in os.listdir(folder):
		path = os.path.join(folder, filename)

		# 画像を読み込む
		img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

		# 読み込めない場合はスキップ
		if img is None:
			continue
		# サイズを揃える（学習のため）
		img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
		# 1次元の特徴ベクトルに変換
		vec = img.flatten().astype(np.float32)
		train_data.append(vec)
		train_labels.append(label)
	print("画像読み込み完了")
	
# 配列に変換
train_data = np.array(train_data)
train_labels = np.array(train_labels)

# k-NN モデルを作成して学習
knn = cv2.ml.KNearest_create()
knn.train(train_data, cv2.ml.ROW_SAMPLE, train_labels)

# 学習結果を保存
knn.save("shape_knn_model.yml")
print("学習完了 → shape_knn_model.yml に保存されました！")