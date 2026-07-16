import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#CSVファイルをpandasのデータフレームとして読み込む。
df = pd.read_csv("FEH_00200524_260716110527.csv", index_col="全国・都道府県", encoding="UTF-8", thousands=",")
#index_colは読み込み時に指定した列をindexとして使うという指定。

#2022円の列データで棒グラフを作って表示する
df = df.drop("全国",axis=0) 
#↑全国のデータは大き過ぎてグラフにした時にほかのデータが小さくなりすぎてしまうので削除。
print(df.head(10))

#df["2021年"] = pd.to_numeric(df["2021年"].str.replace(",",""))
#df["2022年"] = pd.to_numeric(df["2022年"].str.replace(",",""))

df["2021年"] = df[df[["男女別"]=-="男女計"&&["人口"]=="総人口"]]]
df["2022年"] = df[df[["男女別"]=-="男女計"&&["人口"]=="総人口"]]]
df["人口増減"] = df["2021年"] - df["2022年"]
df = df.sort_values("人口増減", ascending=False)
df["人口増減"].plot.barh(figsize=(15,6))
plt.tight_layout()  # ← 追加：システムに余白の自動計算を命令！
#plt.savefig(f"s-stat_test2_{now}.jpg")
'''

'''
