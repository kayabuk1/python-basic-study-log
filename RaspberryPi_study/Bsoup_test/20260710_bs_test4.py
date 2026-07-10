import requests
from bs4 import BeautifulSoup
import datetime
find_target = {"id": "tmp_contents"}

url = "https://www.pref.chiba.lg.jp/kg-funabashi/index.html"

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
for h2 in soup.find_all("h2"):
	print(h2.get_text())
find_tg_ls = soup.find_all(**find_target)
print(f"発見したfind_targetの数: {len(find_tg_ls)}")

with open(
f"scraped_data_[{url[8:20]}]_{now}.txt","w",encoding="utf-8")as file:
	for found_target in soup.find_all(**find_target):
		file.write(found_target.get_text() + "\n")
