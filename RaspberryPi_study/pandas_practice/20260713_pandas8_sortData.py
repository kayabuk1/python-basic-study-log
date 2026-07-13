import pandas as pd

df = pd.read_csv("20260713_test_csv.csv")

#ソートして表示
kokugo = df.sort_values("国語", ascending=False)
print("国語の点数 高い順でソート\n", kokugo)

'''
pi@raspberrypi ~/s/pandas_practice> python3 20260713_pandas8_sortData.
py
Traceback (most recent call last):
  File "/home/pi/share/pandas_practice/20260713_pandas8_sortData.py", line 6, in <module>
    kokugo = df.sort_value("国語", ascending=False)
             ^^^^^^^^^^^^^
  File "/home/pi/.local/lib/python3.13/site-packages/pandas/core/generic.py", line 6206, in __getattr__
    return object.__getattribute__(self, name)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AttributeError: 'DataFrame' object has no attribute 'sort_value'. Did you mean: 'sort_values'?
pi@raspberrypi ~/s/pandas_practice [1]> python3 20260713_pandas8_sortD
ata.py
国語の点数 高い順でソート    名前   国語  数学  英語  理科  社会
2  C子  100  84  96  82  94
5  F菜   96  92  94  92  90
4  E美   92  62  84  80  78
0  A太   83  89  76  97  76
1  B介   66  93  75  88  76
3  D郎   60  73  63  52  70

手痛いエラーを食らった。
indexは一塊のindexとして渡すということだが、
valuesも値を一塊で扱っているのではないのだろうか？

pandasにもソートが用意されているけれど、sorted関数とlist.sortメソッドとの違いを比較しながら
解説してほしい。
2. ソート機能の比較解剖（sort / sorted / sort_values）
PythonとPandasの世界には、似た名前でも役割（アーキテクチャ）が全く異なる3つのソート機能が存在します。
① list.sort() （Pythonのリスト専用メソッド）
対象: 
 のようなPythonの標準リスト。
挙動（破壊的）: 元のリストそのものを直接書き換えて並べ替えます。
戻り値: なし（None）。
実務での立ち位置: メモリを節約しながら、単なる配列をその場でサッと並べ替えたい場合に使用する「軽量な配管」です。
② sorted() （Pythonの組み込み関数）
対象: リスト、タプル、辞書など、複数の要素を持つデータ全般。
挙動（非破壊的）: 元のデータには一切触れず、並べ替え済みの**「新しいリスト」を生成して返します**。
実務での立ち位置: 元のデータを壊さずに保護したまま、並べ替えた結果を別の変数で受け取りたい場合に使用する「安全装置」です。
③ df.sort_values() （Pandas専用メソッド）
対象: PandasのDataFrame（2次元の表）やSeries（1次元の列）。
挙動（非破壊的）: sorted() と同様に元の表は変更せず、並べ替えた「新しい表」を作って返します。
実務での立ち位置: 単なる1列の数字を並べるのではなく、**「『国語』の点数を基準にして、その人の『名前』や『数学』の点数も一緒に（行を維持したまま）丸ごと並べ替える」**ための、強力なデータベース型ソートエンジンです。 （※今回の実行結果でも、A太やC子といった行全体のデータが崩れることなく国語の点数順に並び替わっていることが確認できます）
■ まとめ
Python標準の sort() や sorted() は「1次元の単純なデータの列」を整列させるための機能ですが、Pandasの sort_values() は「2次元の表データを、指定した列をキー（基準）として行ごと入れ替える」という、SQLの ORDER BY に相当する高度な処理を行っています。
'''