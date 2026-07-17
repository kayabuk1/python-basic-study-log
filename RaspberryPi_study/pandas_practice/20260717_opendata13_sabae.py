import pandas as pd

df = pd.read_csv("200.csv", encoding="shift-jis")
#↑どこを見ればDLしたCSVファイルがshift-jisかutf-8か確認できるのだっけ？

print(len(df))
print(df.columns.values)

#消火栓のある地点※緯度経度 をリスト化する
hydrant = df[["緯度","経度"]].values
print(len(hydrant))
print(hydrant)


'''

'''