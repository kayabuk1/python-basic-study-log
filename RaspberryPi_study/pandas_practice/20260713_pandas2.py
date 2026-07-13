import pandas as pd

df = pd.read_csv("20260713_test_csv.csv")

#表データの情報
print("データの件数=", len(df))
print("項目名      =", df.columns.values)
print("インデックス=", df.index.values)