import requests
import json
import datetime
now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

key = ""
#現在の天気を取得する
with open("./openweather_key.txt") as file:
	for data in file:
		key = data.strip()
city = "Funabashi, JP"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&lang=ja&units=metric"
#↑このAPI用のURLはどこを調べたらわかるのだろうか？

jsondata = requests.get(url).json()
print(jsondata)

save_file = f"{now}_webapi_test.json"
with open (save_file, "w") as f:
	json.dump(jsondata, f)

'''
{'coord': {'lon': 139.9833, 'lat': 35.6931}, 'weather': [{'id': 800, 'main': 'Clear', 'description': '晴天', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 36.24, 'feels_like': 42.85, 'temp_min': 32.84, 'temp_max': 36.25, 'pressure': 1007, 'humidity': 48, 'sea_level': 1007, 'grnd_level': 1006}, 'visibility': 10000, 'wind': {'speed': 2.58, 'deg': 57, 'gust': 2.96}, 'clouds': {'all': 0}, 'dt': 1784768846, 'sys': {'type': 2, 'id': 60940, 'country': 'JP', 'sunrise': 1784749238, 'sunset': 1784800325}, 'timezone': 32400, 'id': 1863905, 'name': '船橋市', 'cod': 200}
'''
