import requests
from bs4 import BeautifulSoup
import datetime
import re

find_target1 = {"class_": "title"} #"h2", class="title"みたいにまとめて渡すには？
find_target2 = {"class_": "author"}
find_target3 = {"class_": "main_text"}

url = "https://www.aozora.gr.jp/cards/000879/files/92_14545.html"
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
soup = BeautifulSoup(response.content, 'lxml-xml')
#print(soup)
print(type(soup))
#print(dir(soup))
now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

for ft in soup.find_all(find_target1):
	print(ft.get_text())
find_tg_ls = soup.find_all(**find_target1)
print(f"発見したfind_targetの数: {len(find_tg_ls)}")
for ft in soup.find_all(find_target2):
	print(ft.get_text())
find_tg_ls = soup.find_all(**find_target2)
print(f"発見したfind_targetの数: {len(find_tg_ls)}")
for ft in soup.find_all(find_target3):
	print(ft.get_text())
find_tg_ls = soup.find_all(**find_target3)
print(f"発見したfind_targetの数: {len(find_tg_ls)}")

with open(
f"scraped_data_[{domain}]_{now}.txt","w",encoding="utf-8")as file:
	for found_target in soup.find_all(**find_target1):
		file.write(found_target.get_text() + "\n")
	for found_target in soup.find_all(**find_target2):
		file.write(found_target.get_text() + "\n")
	for found_target in soup.find_all(**find_target3):
		file.write(found_target.get_text() + "\n")
