import pandas as pd
import folium
#↑なぜfoliumは同じ階層にファイルを置かなくても実行出来てしまうのだろうか？
import datetime

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

df = pd.read_csv("200.csv", encoding="shift-jis")

print(len(df))
print(df.columns.values)

#消火栓のある地点※緯度経度 をリスト化する
hydrant = df[["緯度","経度"]].values
print(len(hydrant))
print(hydrant)

#foliumを使って地図を書き出す。
map = folium.Map(location=[35.942957, 136.198863], zoom_start=16)
#↑この行はどんな意味だろうか？
for data in hydrant:
	folium.Marker([data[0], data[1]]).add_to(map)
map.save(F"{now}_sabae.html")




'''

'''