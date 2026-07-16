import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#CSVファイルをpandasのデータフレームとして読み込む。
df = pd.read_csv("FEH_00200524_260716110527.csv", index_col="全国・都道府県", encoding="UTF-8", thousands=',')
#index_colは読み込み時に指定した列をindexとして使うという指定。

print(df["2022年"])
df["2022年"].plot.bar()
plt.savefig(f"s-stat_test_{now}.jpg")
'''
全国・都道府県
全国      124,947
北海道       5,140
青森県       1,204
岩手県       1,181
宮城県       2,280
         ...
熊本県         894
大分県         573
宮崎県         551
鹿児島県        817
沖縄県         736
Name: 2022年, Length: 288, dtype: str
Traceback (most recent call last):
  File "/home/pi/share/pandas_practice/20260716_opendata5_e-Stat.py", line 13, in <module>
    df["2022年"].plot.bar()
    ~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/pi/.local/lib/python3.13/site-packages/pandas/plotting/_core.py", line 1432, in bar
    return self(kind="bar", x=x, y=y, **kwargs)
  File "/home/pi/.local/lib/python3.13/site-packages/pandas/plotting/_core.py", line 1185, in __call__
    return plot_backend.plot(data, kind=kind, **kwargs)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/pi/.local/lib/python3.13/site-packages/pandas/plotting/_matplotlib/__init__.py", line 71, in plot
    plot_obj.generate()
    ~~~~~~~~~~~~~~~~~^^
  File "/home/pi/.local/lib/python3.13/site-packages/pandas/plotting/_matplotlib/core.py", line 516, in generate
    self._compute_plot_data()
    ~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/pi/.local/lib/python3.13/site-packages/pandas/plotting/_matplotlib/core.py", line 716, in _compute_plot_data
    raise TypeError("no numeric data to plot")
TypeError: no numeric data to plot

全国・都道府県
全国      124947
北海道       5140
青森県       1204
岩手県       1181
宮城県       2280
         ...
熊本県        894
大分県        573
宮崎県        551
鹿児島県       817
沖縄県        736
Name: 2022年, Length: 288, dtype: int64
'''
