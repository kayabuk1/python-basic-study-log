import pandas as pd
import folium
#↑なぜfoliumは同じ階層にファイルを置かなくても実行出来てしまうのだろうか？
import datetime

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

df = pd.read_csv("898.csv", encoding="utf-8")

print(len(df))
print(df.columns.values)

#消火栓のある地点※緯度経度 をリスト化する
stores = df[["緯度","経度","店舗名(日本語)"]].values
print(len(stores))
print(stores)

#foliumを使って地図を書き出す。
map = folium.Map(location=[35.942957, 136.198863], zoom_start=16)
#↑この行はどんな意味だろうか？
for store in stores:
	print(store)
	folium.Marker([store[0], store[1]],tooltip=store[2]).add_to(map)
map.save(F"{now}_sabaestore.html")




'''

'''