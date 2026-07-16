import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#CSVファイルをpandasのデータフレームとして読み込む。
df = pd.read_csv("FEH_00200524_260716110527.csv", index_col="全国・都道府県", encoding="UTF-8", thousands=',', dtype=str)
#index_colは読み込み時に指定した列をindexとして使うという指定。

#2022円の列データで棒グラフを作って表示する
df = df.drop("全国",axis=0) 
#↑全国のデータは大き過ぎてグラフにした時にほかのデータが小さくなりすぎてしまうので削除。

df["2022年"] = pd.to_numeric(df["2022年"].str.replace(",",""))
df["2022年"].plot.bar(figsize=(10,6))
plt.savefig(f"s-stat_test2_{now}.jpg")
'''

'''
