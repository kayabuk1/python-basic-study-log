import requests
import json
from pprint import pprint

from datetime import datetime, timedelta, timezone

#APIキーをハードコーディングしないで読み込む。
key = ""
with open("./openweather_key.txt") as file:
	for data in file:
		key = data.strip()

#●UTC（協定世界時）をJST（日本標準時）に変換
timestamp = 1709964000 #2024年3月9日？のタイムスタンプ
tz = timezone(timedelta(), 'UTC')
print(tz)
utc = datetime.fromtimestamp(timestamp, tz)
print(utc)

tz = timezone(timedelta(hours=+9), 'JST')
print(tz)
jst = datetime.fromtimestamp(timestamp, tz)
print(jst)
print(str(jst)[:-9])
#UTC
#1975-06-03 03:00:00+00:00
#JST
#1975-06-03 12:00:00+09:00
#1975-06-03 12:00

#●5日間の時刻（3時間ごと）の天気を取得する：東京
city = "Tokyo,JP"
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&lang=ja&units=metric"
jsondata = requests.get(url).json()
pprint(jsondata)
tz = timezone(timedelta(hours=+9),'JST')
for dat in jsondata["list"]:
	jst = str(datetime.fromtimestamp(dat["dt"],tz))[:-9]
	weather = dat["weather"][0]["description"]
	temp = dat["main"]["temp"]
	print("UTC={utc},JST={jst}".format(utc=dat["dt_txt"],jst=jst))
	print("日時:{jst}, 天気:{w}, 気温:{t}度".format(jst=jst, w=weather, t=temp))
	#●dt,datはどんな意味？


now = datetime.now().strftime("%Y%m%d_%H%M%S")

'''

#現在の船橋の天気を取得する
city = "Funabashi, JP"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&lang=ja&units=metric"

#●5日間（3時間ごと）の天気を取得する：東京
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&lang=ja&units=metric"
jsondata5 = requests.get(url).json()
pprint(jsondata5)
print("\n")
#●取得したJSONデータをjsonファイルとして書き込み
save_file = f"{now}_webapi_5days_test.json"
with open (save_file, "w", encoding="utf-8") as f:
	json.dump(jsondata5, f, indent=4, ensure_ascii=False)


#●郵便番号で天気を取得する●zipcordで郵便番号という意味になるの？
zipcode = "10001,US"
z_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode}&appid={key}&lang=ja&units=metric"
jsondata4 = requests.get(z_url).json()
print(jsondata4)
print("\n")
pprint(jsondata4)
print("\n")
#print("都市名 = ",jsondata4["name"])
#print("気温 = ",jsondata4["main"]["temp"])
#print("天気 = ",jsondata4["weather"][0]["main"])
#print("天気詳細 =", jsondata4["weather"][0]["description"])
print("\n")

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


'''
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

