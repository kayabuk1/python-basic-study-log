import requests
from bs4 import BeautifulSoup
import datetime
import re
#取り出したURLのうち、相対URLを絶対URLに変換する。
import urllib

find_target1 = "a"
find_target2 = "href"

url = "https://www.pref.chiba.lg.jp/kg-funabashi/index.html"
# //の直後から、次の / までの文字をえぐり出すレーザーメス
match = re.search(r'//([^/]+)', url)
if match:
    domain = match.group(1)
    print(f"抽出ドメイン: {domain}") # 出力: www.aozora.gr.jp
'''
リスト（match）ではないのか？：
 re.search は、ただ文字を見つけるだけでなく、「どこからどこまで見つかったか（位置情報）」などのメタデータも一緒に持ち帰ってきます。そのため、ただのリストではなく「Matchオブジェクト」という高機能な箱に詰め込まれます。 そこから「() で囲んでキャプチャ（確保）した1番目のグループだけを取り出せ」と指示するために、match.group(1) というメソッド通信を使っているのです。
'''

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

for ft in soup.find_all(find_target1):
	print(ft.get_text())
	link = ft.get(find_target2)
	print(link)
	ab_url = urllib.parse.urljoin(url,link)
	print(ab_url)
find_tg_ls = soup.find_all(find_target1)
print(f"発見したfind_targetの数: {len(find_tg_ls)}")

with open(
f"scraped_data_[{domain}]_{now}_linklist.txt","w",encoding="utf-8")as file:
	for found_target in soup.find_all(find_target1):
		file.write(found_target.get_text() + "\n")
		#found_targetはBSオブジェクトなので.get_text()メソッドが使えた。
		link = found_target.get(find_target2)
		if link:
			#取り出した link はすでにただの文字列なので.get_textメソッドは使えない。
			ab_url = urllib.parse.urljoin(url, link)
			#↑urljoin(基準となるURL, 変更したいURL)を引数として渡すだけ。
			file.write(ab_url + "\n")
print("URLの抽出と保存が完了しました！")
