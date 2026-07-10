import requests
from bs4 import BeautifulSoup
import datetime
import re
import urllib
#次は画像を取得しようとのことです。

find_target1 = "img"
find_target2 = "src"

url = "https://www.pref.chiba.lg.jp/kg-funabashi/"

# 【追加】通信の身分証明書（一般的なブラウザのふりをする防弾装甲）
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
# 【追加】状況を可視化するレーダー（デバッグ用）
print(f"通信ステータス: {response.status_code}")
#print(response.text)
response.encoding = response.apparent_encoding
#print(response.text)
soup = BeautifulSoup(response.content, 'lxml')
#print(soup)
print(type(soup))
#print(dir(soup))
now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# //の直後から、次の / までの文字を取り出す。
match = re.search(r'//([^/]+)', url)
if match:
    domain = match.group(1)
    print(f"抽出ドメイン: {domain}") # 出力: www.aozora.gr.jp
'''
リスト（match）ではないのか？：
 re.search は、ただ文字を見つけるだけでなく、「どこからどこまで見つかったか（位置情報）」などのメタデータも一緒に持ち帰ってきます。そのため、ただのリストではなく「Matchオブジェクト」という高機能な箱に詰め込まれます。 そこから「() で囲んでキャプチャ（確保）した1番目のグループだけを取り出せ」と指示するために、match.group(1) というメソッド通信を使っているのです。
'''

#ほしい画像名は絶対パスの一番最後の部分splitメソッドで返ってくるデータ型はリスト
#なので、[-1]を指定してやれば最後のみ取り出すことができるとのことです。

with open(
f"scraped_data_[{domain}]_{now}_imglist.txt","w",encoding="utf-8")as file:
	for element in soup.find_all(find_target1):
		src =element.get("src")
		#HTML内の属性URLの取り出しは.get(属性名href)を使うとのこと。
		image_url = urllib.parse.urljoin(url, src)
		filename = image_url.split("/")[-1]
		print(image_url,">>",filename)
		file.write(image_url+">>"+filename + "\n")
