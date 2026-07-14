import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime
now = datetime.datetime.now()

df = pd.read_csv("20260713_test_csv.csv",index_col=0)

#グラフを作って表示をする
df.plot()
plt.savefig(f"my_graph_{now}.png")

df.plot.bar()
plt.savefig(f"my_bargraph_{now}.png")

df.plot.barh()
plt.legend(loc="lower left")
plt.savefig(f"my_barhgraph_{now}.png")

df.plot.bar(stacked=True)
plt.legend(loc="lower right")
plt.savefig(f"my_barstackgraph_{now}.png")

df.plot.box()
plt.savefig(f"my_boxgraph_{now}.png")

df.plot.area()
plt.legend(loc="lower right")
plt.savefig(f"my_areagraph_{now}.png")

plt.show()