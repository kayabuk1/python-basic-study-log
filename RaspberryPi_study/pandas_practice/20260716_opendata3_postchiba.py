import pandas as pd

#CSVファイルをpandasのデータフレームとして読み込む。
df = pd.read_csv("12CHIBA.CSV", header=None, encoding="shift_JIS", dtype=str)

#[8]の列が[2730014]の住所を抽出して表示
results = df[df[8]=="今井"]
print(results[[2,6,7,8]])

#[8]の列に[今井]の文字が含まれる住所を抽出して表示
results = df[df[8].str.contains("今井")]
print(results[[2,6,7,8]])

'''
pi@raspberrypi ~/s/pandas_practice> python3 20260716_opendata3_postchib
a.py
            2    6       7   8
7     2600834  千葉県  千葉市中央区  今井
2428  2990264  千葉県    袖ケ浦市  今井
2606  2701401  千葉県     白井市  今井
            2    6       7    8
7     2600834  千葉県  千葉市中央区   今井
8     2600815  千葉県  千葉市中央区  今井町
2428  2990264  千葉県    袖ケ浦市   今井
2606  2701401  千葉県     白井市   今井
'''
