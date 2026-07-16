import pandas as pd

#CSVファイルをpandasのデータフレームとして読み込む。
df = pd.read_csv("FEH_00200524_260716103239.csv", index_col="全国・都道府県", encoding="shift-JIS")
#index_colは読み込み時に指定した列をindexとして使うという指定。

print(len(df))
print(df.columns.values)
'''
pi@raspberrypi ~/s/pandas_practice [1]> python3 20260716_opendata4_e-St
at.py
288
<StringArray>
[   '表章項目',     '男女別',      '人口', '/時間軸（年）',   '2005年',   '2010年',   '2015年',
   '2020年',   '2021年',   '2022年',   '2023年',   '2024年']
Length: 12, dtype: str
'''
