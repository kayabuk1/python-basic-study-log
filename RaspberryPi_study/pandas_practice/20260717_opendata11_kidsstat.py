import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#CSVファイルを各データフレームに読み込む
df1 = pd.read_csv("Preview_20260717091920.csv", index_col="時点", skiprows=1)
df2 = pd.read_csv("Preview_20260717092140.csv", index_col="時点", skiprows=1)
df3 = pd.read_csv("Preview_20260717092126.csv", index_col="時点", skiprows=1)

#df2とdf3の2行1列目の値が東京になっているので、わかりやすい名前にリネームする
df2 = df2.rename(columns={"東京都":"最高気温"})
df3 = df3.rename(columns={"東京都":"最低気温"})

print(df1.columns.values)
print(df2.columns.values)
print(df3.columns.values)

# ★修正ポイント：columns配列の [ 0 ] 番目を指定して、純粋な文字列だけを取り出して結合する
# ※システムの自動変換を防ぐため、念のため括弧の中にスペースを入れていますが、実際のコードでは df1.columns と詰めて書いても大丈夫です。
datalabel = f"{df1.columns[ 0 ]}_{df2.columns[ 0 ]}_{df3.columns[ 0 ]}"
print("生成されたラベル:", datalabel)

# 0行目, 0列目の値（例：1975年の年平均気温）を抽出して変数に格納
#target_val = df1.iloc[-1, 0] 
# 行のインデックスが「2022年」、列名が「年平均気温【℃】」の値を抽出
target_val = df1.loc["2022年", "年平均気温【℃】"]
print(target_val)

#3つのグラフを重ねて表示
df1["年平均気温【℃】"].plot()
df2["最高気温"].plot()
df3["最低気温"].plot()

#print(df1["年平均気温【℃】"].plot())
#print(df2["最高気温"].plot())
#print(df3["最低気温"].plot())

plt.ylim(-10,40) 
# 抽出した値（target_val）を f-string でファイル名に組み込む

plt.legend(loc="lower right")
plt.savefig(f"temp_data_{datalabel}_{now}.jpg")

'''
<StringArray>
['年平均気温【℃】']
Length: 1, dtype: str
<StringArray>
['最高気温']
Length: 1, dtype: str
<StringArray>
['最低気温']
Length: 1, dtype: str
16.4
Axes(0.125,0.11;0.775x0.77)
Axes(0.125,0.11;0.775x0.77)
Axes(0.125,0.11;0.775x0.77)
'''