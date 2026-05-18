# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:07:07 2026

@author: iot01
"""

#%% 7.2.4途中から タブ区切りテキストを出力する csv.write関数
import csv
data = [
        [101,'山田太郎','090-1111-2222',],
        [102,'鈴木次郎','080-3333-4444',],
        [103,'佐藤花子','070-5555-6666',],
        ]
with open ("menber.tsv","w",newline='',encoding='UTF-8')\
as file:
    writer = csv.writer(file,delimiter='\t',quoting=csv.QUOTE_ALL)
    writer.writerow(data)
    #%runfile 'D:/python/20260518_7.2.4_file_csv_write~.py' --wdir
    #"[101, '山田太郎', '090-1111-2222']"	"[102, '鈴木次郎', '080-3333-4444']"	"[103, '佐藤花子', '070-5555-6666']"
'''
newline='': これは 「csv モジュールを使ってファイルに書き込むときの『鉄の掟（公式ルール）』」 です。
WindowsなどのOSは、ファイルに書き込む際に「改行コード（行の終わり）」を勝手に変換しようとするおせっかいな機能を持っています。
しかし、csv.writer も自分で改行をコントロールしようとするため、二重に改行処理が行われてしまい、「1行ごとに空行が挟まる（1行空きになる）バグ」が起きることがあります。
それを防ぐために、システムに対して「OS側での改行の自動変換は一切やめろ（newline=''）」と指示を出しているのです。
'''

#%% 7.2.5 オブジェクトのシリアライズとは？
class Book:
    def __init__(self,isbn,title,price):
        self.isbn = isbn
        self.title = title
        self.price = price
#上のコードをbook.pyで保存しておく必要がある。

import pickle
import book
b = book.Book('978-4-7981-5382-7','独習C# 新版',3600)
with open('book.bin','wb')as file:
    pickle.dump(b,file)

#引数protocolとは？？？？
#デシリアライズする。 loadメソッド
import pickle
with open('book.bin','rb')as file:
    b = pickle.load(file)
    print(b.title)

#%%# 7.3 ファイルシステムの操作
# 7.3.1 フォルダーは以下のファイル情報を取得する listdir関数 
import datetime
import os
PATH = './python'
for f in os.listdir(PATH):
    p = os.path.join(PATH, f)
    #「モジュール名」.「サブモジュール名」.「関数名()」 という構造
    print(p)
    print('フォルダー' if os.path.isdir(p) else 'ファイル')
    print(datetime.datetime.fromtimestamp(os.path.getatime(p)))
    print(os.path.getsize(p),'byte')
    print('-----')
'''
python\新規 テキスト ドキュメント.txt
ファイル
2026-05-18 14:19:42.440461
0 byte
-----
python\練習問題2横須賀.py
ファイル
2026-05-18 14:19:42.473842
1224 byte
-----
'''
'''
【1ループ目の報告：新規テキストドキュメント】
python\新規 テキスト ドキュメント.txt
➔ print(p) の結果です。os.path.join 工場が、ターゲットのフォルダとファイル名を
Windows専用の区切り文字 \ で安全に合体させてくれました。
    #osモジュールについて分かりやすく解説してください。
    os.path.join関数の動作について分かりやすく解説してください。
ファイル
➔ 三項演算子の結果です。対象がフォルダではないため、OSは False を返し、
見事に右側の「ファイル」という文字が選ばれて出力されました。
2026-05-18 14:19:42.440461
➔ os.path.getatime がOSから引っぱり出した「機械用の暗号
（1970年からの経過秒数）」を、外側の datetime.datetime.fromtimestamp
工場が「人間が読める日時」へと翻訳した結果です。ミリ秒（.440461）まで正確に出ていますね。
    #.getatimeと.datetime.fromtimestampの動作について分かりやすく解説してください。
0 byte
➔ os.path.getsize が容量を計測した結果です。作ったばかりで中身が
空っぽのテキストファイルであることが、数字から正確に読み取れます。
【2ループ目の報告：過去の練習問題】
python\練習問題2横須賀.py
➔ ループの2周目で、昌敏さんが過去に書いたPythonスクリプトを発見しました。
1224 byte
➔ このファイルには1224バイト分（約1.2キロバイト、半角文字なら1224文字分）のコードが
ぎっしり書かれていることがわかります。

'''
#%% 7.3.2 ファイル情報の取得2　scandir関数
import datetime
import os
PATH = './python'
for f in os.scandir(PATH):
    print(f.path)
    print('フォルダー' if f.is_dir() else 'ファイル')
    st =f.stat()
    print(datetime.datetime.fromtimestamp(st.st_atime))
    print(st.st_size,'byte')
    print('-----')
'''
./python\新規 テキスト ドキュメント.txt
ファイル
2026-05-18 14:19:42.440461
0 byte
-----
./python\練習問題2横須賀.py
ファイル
2026-05-18 14:19:42.473842
1224 byte
-----
'''

#%%　7.3.3　フォルダ/ファイルを再帰的に取得する walk関数
import os
for path,dirs,files in os.walk('./python'):
    print(path)
    print(dirs)
    print(files)
    print('-----------')
'''
./python
[]
['新規 テキスト ドキュメント.txt', '練習問題2横須賀.py', '練習問題3横須賀.py', '練習問題4途中横須賀.py', '練習問題１.pptx', '練習問題２.pptx', '練習問題３.pptx', '練習問題４.pptx']
-----------
'''

#拡張子が .txt のファイルをすべて列挙する
import os
for path,dirs,files in os.walk('./python'):
    for f in files:
        if f.endswith('.txt'):
            print(os.path.join(path,f))
#./python\新規 テキスト ドキュメント.txt

#%% 7.3.4 フォルダ作成/リネーム/削除　mkdir,rename,rmdir関数
import os
os.mkdir('./python/sub',mode=0o666)
input('Hit any key...')
os.rename('./python/sub','./python/copy')
input('Hit any key...')
os.rmdir('./python/copy')
#Hit any key...
#Hit any key...

#%% 7.3.5　複数階層でフォルダを作成/リネーム/削除する
import os
os.makedirs('./python/sub/gsub')
input('Hit any key...')
os.renames('./python/sub/gsub','./python/copy/gchild')
input('Hit any key...')
os.removedirs('./python/copy/gchild')

#%% 7.3.6 フォルダと配下のフォルダ/ファイルをまとめてコピーする copytree関数
import shutil
shutil.copytree(
    './python/doc', './python/data',
    dirs_exist_ok=True
    )

#%%# 7.4 HTTP経由でコンテンツを取得する
# 7.4.1 requestsモジュールの基本
import requests
print(dir(requests))
res = requests.request('get', 'https://codezine.jp', )
print(res.text)

#%% 7.4.2 HTTP POSTによる通信
import requests
res = requests.post('https://wings.msn.to/tmp/post.php', 
                    data={'name':'佐々木新之助'})
print(res.text)
    #こんにちは、佐々木新之助さん！











