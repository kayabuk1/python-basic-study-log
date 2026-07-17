import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#CSVファイルを各データフレームに読み込む
df1 = pd.read_csv("Preview_20260717091920.csv", index_col="時点", skiprows=1)
df2 = pd.read_csv("Preview_20260717092140.csv", index_col="時点", skiprows=1)
df3 = pd.read_csv("Preview_20260717092126.csv", index_col="時点", skiprows=1)

print(df1.columns.values)
print(df2.columns.values)
print(df3.columns.values)

# 0行目, 0列目の値（例：1975年の年平均気温）を抽出して変数に格納
#target_val = df1.iloc[-1, 0] 
# 行のインデックスが「2022年」、列名が「年平均気温【℃】」の値を抽出
target_val = df1.loc["2022年", "年平均気温【℃】"]

#平均気温で折れ線グラフを表示
df1["年平均気温【℃】"].plot()
plt.ylim(-10,40) #←これ初めて見る関数だな。動作：Y軸の最小値を -10 に、最大値を 40 に固定してグラフを描画します。
#インフラ的メリット：Pandasは賢いので、放っておくと「データの最大値・最小値に合わせてグラフのメモリを自動調整」してしまいます。しかし、最高気温・最低気温・平均気温など複数のグラフを見比べる場合、Y軸のスケール（物差し）が固定されていないと、データの比較が正しくできなくなるため、この重機を使ってシステムに表示範囲を絶対指定しているのです。
# 抽出した値（target_val）を f-string でファイル名に組み込む
plt.savefig(f"temp_data_{target_val}_{now}.jpg")

'''
3. 【真相解明】：特定のセル（行・列）の値をぶち抜き、ファイル名にする方法
「データフレームの特定のマス目（セル）のデータだけをピンポイントで抽出する」には、Pandasの最強のピンポイント抽出ツールである iloc（アイロック：Index Location） または loc（ロック：Location） を使います。
■ ルートA：iloc （行番号・列番号の「数字」でぶち抜く） コンピュータの配列インデックスと同じく「0」から数えます。 例えば、**「一番上の行（0行目）の、一番左の列（0列目）」**の値を抽出したい場合はこう書きます。
# 0行目, 0列目の値（例：1975年の年平均気温）を抽出して変数に格納
target_val = df1.iloc
■ ルートB：loc （行の名前・列の「名前」でぶち抜く） 昌敏さんが以前使った行抽出の応用です。「何行目」か分からない場合でも、名指しで抽出できます。
# 行のインデックスが「2022年」、列名が「年平均気温【℃】」の値を抽出
target_val = df1.loc["2022年", "年平均気温【℃】"]
'''