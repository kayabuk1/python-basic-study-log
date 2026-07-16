import pandas as pd

#CSVファイルをpandasのデータフレームとして読み込む。
df = pd.read_csv("12CHIBA.CSV", header=None, encoding="shift_JIS", dtype=str)

#[2]の列が[2730014]の住所を抽出して表示
results = df[df[2]=="2730014"]
print(results[[2,6,7,8]])

'''
  2    6    7    8
506  2730014  千葉県  船橋市  高瀬町
'''
