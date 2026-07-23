import requests
import json
from pprint import pprint

import datetime
now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#jsonファイルを開く練習 
#●※jsonファイルの一番外側に[]が使われているものとそうでないもの違いは？
with open('./test.json', mode="r") as f:
#mode="r"とデフォルト引数に指定する形でも良いのは知らなかった。
	jsondata = json.loads(f.read())
	#●f.readが必要なのはなぜだろうか？
	f.seek(0)
	jsondata2 = json.load(f)
	pprint(jsondata)
	print("\n")
	pprint(jsondata2)
	print("\n")
	print("1つ目のオブジェクト = ",jsondata[0])
	print("都市名 = ",jsondata[0]["name"])
	print("緯度 = ",jsondata[0]["coord"]["lat"])
	print("経度 = ",jsondata[0]["coord"]["lon"])
	print("\n")
	#●↑この辺りのデータの指定の仕方がよくわからない。、、、。

key = ""
#現在の天気を取得する
with open("./openweather_key.txt") as file:
	for data in file:
		key = data.strip()
city = "Funabashi, JP"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&lang=ja&units=metric"
#↑このAPI用のURLはどこを調べたらわかるのだろうか？

#船橋の天気を取得して表示
jsondata3 = requests.get(url).json()
print(jsondata3)
print("\n")
pprint(jsondata3)
print("\n")
print("都市名 = ",jsondata3["name"])
print("気温 = ",jsondata3["main"]["temp"])
print("天気 = ",jsondata3["weather"][0]["main"])
print("天気詳細 =", jsondata3["weather"][0]["description"])
print("\n")
#●↑このほしいデータのキーを割り出す為に、一度pprintで出力するとのこと。

save_file = f"{now}_webapi_test.json"
with open (save_file, "w", encoding="utf-8") as f:
	json.dump(jsondata3, f, indent=4, ensure_ascii=False)

'''
[{'coord': {'lat': 35.69, 'lon': 139.69}, 'name': 'Tokyo'},
 {'coord': {'lat': 35.02, 'lon': 135.75}, 'name': 'Kyoto'}]


[{'coord': {'lat': 35.69, 'lon': 139.69}, 'name': 'Tokyo'},
 {'coord': {'lat': 35.02, 'lon': 135.75}, 'name': 'Kyoto'}]


1つ目のオブジェクト =  {'name': 'Tokyo', 'coord': {'lat': 35.69, 'lon': 139.69}}
都市名 =  Tokyo
緯度 =  35.69
経度 =  139.69


{'coord': {'lon': 139.9833, 'lat': 35.6931}, 'weather': [{'id': 800, 'main': 'Clear', 'description': '晴天', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 35.7, 'feels_like': 42.38, 'temp_min': 35.7, 'temp_max': 36.78, 'pressure': 1006, 'humidity': 50, 'sea_level': 1006, 'grnd_level': 1006}, 'visibility': 10000, 'wind': {'speed': 2.51, 'deg': 68, 'gust': 3}, 'clouds': {'all': 0}, 'dt': 1784773084, 'sys': {'type': 2, 'id': 60940, 'country': 'JP', 'sunrise': 1784749238, 'sunset': 1784800325}, 'timezone': 32400, 'id': 1863905, 'name': '船橋市', 'cod': 200}


{'base': 'stations',
 'clouds': {'all': 0},
 'cod': 200,
 'coord': {'lat': 35.6931, 'lon': 139.9833},
 'dt': 1784773084,
 'id': 1863905,
 'main': {'feels_like': 42.38,
          'grnd_level': 1006,
          'humidity': 50,
          'pressure': 1006,
          'sea_level': 1006,
          'temp': 35.7,
          'temp_max': 36.78,
          'temp_min': 35.7},
 'name': '船橋市',
 'sys': {'country': 'JP',
         'id': 60940,
         'sunrise': 1784749238,
         'sunset': 1784800325,
         'type': 2},
 'timezone': 32400,
 'visibility': 10000,
 'weather': [{'description': '晴天', 'icon': '01d', 'id': 800, 'main': 'Clear'}],
 'wind': {'deg': 68, 'gust': 3, 'speed': 2.51}}


都市名 =  船橋市
気温 =  35.7
天気 =  Clear
天気詳細 = 晴天
'''
