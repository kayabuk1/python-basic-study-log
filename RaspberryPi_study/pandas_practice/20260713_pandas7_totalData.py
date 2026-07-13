import pandas as pd

df = pd.read_csv("20260713_test_csv.csv")

#集計、最大値、最小値、平均値、中央値、合計
print("数学の最高点=", df["数学"].max())
print("数学の最低点=", df["数学"].min())
print("数学の平均点=", round(df["数学"].mean(),2))
print("数学の平均点=", df["数学"].mean().round(2))
print("数学の中央値=", df["数学"].median())
print("数学の合計  =", df["数学"].sum())

'''
数学の最高点= 93
数学の最低点= 62
数学の平均点= 82 2
数学の中央値= 86.5
数学の合計  = 493
'''