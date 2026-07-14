import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime
now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

df = pd.read_csv("20260713_test_csv.csv")

#ソート、高い順
kokugo = df.sort_values("国語", ascending=False) #value's'なのを忘れるな！

#1つのExcelファイルに複数シートで出力する
with pd.ExcelWriter(F"csv_to excel_{now}.xlsx") as writer:
	df.to_excel(writer, index=False, sheet_name="元のデータ")
	kokugo.to_excel(writer, index=False, sheet_name="国語でソート")


