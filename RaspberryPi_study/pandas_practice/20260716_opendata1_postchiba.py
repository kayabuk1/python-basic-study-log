import pandas as pd

#CSVファイルをpandasのデータフレームとして読み込む。
df = pd.read_csv("12CHIBA.CSV", header=None, encoding="shift_JIS", dtype=str)

print(len(df))
print(df.columns.values)
