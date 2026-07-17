import pandas as pd

#CSVファイルを各データフレームに読み込む
df1 = pd.read_csv("Preview_20260717091920.csv", index_col="時点", skiprows=1)
df2 = pd.read_csv("Preview_20260717092140.csv", index_col="時点", skiprows=1)
df3 = pd.read_csv("Preview_20260717092126.csv", index_col="時点", skiprows=1)

print(df1.columns.values)
print(df2.columns.values)
print(df3.columns.values)