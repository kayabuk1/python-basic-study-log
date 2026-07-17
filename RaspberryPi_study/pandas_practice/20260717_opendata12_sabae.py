import pandas as pd

df = pd.read_csv("200.csv", encoding="shift-jis")
#↑どこを見ればDLしたCSVファイルがshift-jisかutf-8か確認できるのだっけ？

print(len(df))
print(df.columns.values)
'''
2568
<StringArray>
[      '消火栓名',   '消火栓名(英語)',      '消火栓分類',        '消 防団',       '管理番号',
      '都道府県名',      '市区町村名',       '行政区名',         '住 所', '対象範囲の直径(m)',
  '配水管口径(mm)',     '貯水量(t)',         '緯度',         '経度',   '分離器（有、無）',
    '標準地域コード']
Length: 16, dtype: str
↑そう言えばなぜcolumnの長さ※データ個数とデータ型まで教えてくれるの？
'''