#次は画像を全て取得し、新たにフォルダを作成してそこに保存する
import requests
from bs4 import BeautifulSoup
import datetime
import re
import urllib
import time
from pathlib import Path

find_target1 = "img"
find_target2 = "src"

url = "https://ja.wikipedia.org/wiki/NASA"

#通信の身分証明書（一般的なブラウザのふりをする）
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

#状況を可視化する（デバッグ用）
print(f"通信ステータス: {response.status_code}")
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.content, 'lxml')
#↑BSを用い構文解析する。
#print(soup) ←取得データ確認デバック用

#画像保存先のﾌｫﾙﾀﾞを作成
save_folder = Path("download_all")
#Pathクラスからﾌｫﾙﾀﾞ名を指定してオブジェクトをコンストラクトする。
save_folder.mkdir(exist_ok=True)

#時刻の作成
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

for element in soup.find_all(find_target1):
	src =element.get(find_target2)
	#HTML内の属性URLの取り出しは.get(属性名href)を使うとのこと。
	
	if src:
		image_url = urllib.parse.urljoin(url, src)
		img_filename = image_url.split("/")[-1]
		#↑絶対パスから画像ファイル名を取得
		
		imgdata = requests.get(image_url, headers=headers)
		#↑image_url絶対パスを作り,requests.getメソッドを使い画像を取得
		
		print(image_url,">>",img_filename)
		
		new_filename = f"scraped_img_{domain}_{now}_{img_filename}"
		#保存用の取得サイト、日時、ファイル名合わせた保存用ファイル名だけ先に作成
		
		save_path =save_folder.joinpath(new_filename)
		
		with open(save_path, mode="wb")as file:
			file.write(imgdata.content)
	time.sleep(1)

