import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime
dt = datetime.datetime.now()
now = dt.date()

df = pd.read_csv("20260713_test_csv.csv")

#グラフを作って表示をする
df.plot()
plt.savefig(f"my_graph_{now}.png")
df.plot.bar()
plt.savefig(f"my_bargraph_{now}.png")
plt.show()