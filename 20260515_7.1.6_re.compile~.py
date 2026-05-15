# -*- coding: utf-8 -*-
"""
Created on Fri May 15 09:04:58 2026

@author: iot01
"""

#%% 7.1.6 正規表現途中から
# 名前付きキャプチャーグループの例
import re
print(dir(re))
msg = '仕事用はwings@exmple.comです。'
ptn = re.compile(
    r'(?i)(?P<localName>[a-z0-9.!#$%&\'*+/=?^\{|}~-]+)'
    r'@(?P<domain>[a-z0-9-]+(?:\.[a-z0-9-]+)*)'
    )
#そもそも re についても re.compile についても解っていないな。
#途中で改行するときの書き方も思い出せていない…
print(ptn.sub(r'\g<domain>の\g<localName>',msg))

#%% 7.1.7 正規表現で文字列を分割する splitメソッド
import re
msg = 'にわに３わうらにわに51わにわとりがいる'
ptn = re.compile(r'\d{1,}わ')
result = ptn.split(msg)
print(result)
    #['にわに', 'うらにわに', 'にわとりがいる']
    #そもそもPatternクラスとは？？？
    
#%%# 7.2ファイル操作
# 7.2.1 テキストファイルへの書き込み
import datetime
#print(dir(open))
#help(open)
file = open('access.log','a', encoding='UTF-8')
    #ファイルはデフォルトでどこに作られることになっている？？
file.write(f'{datetime.datetime.now()}\n')
    #datetime.datetime.now()というのはどういう文法構造になっている？？
file.close()
print('現在時刻をファイルに保存しました。')

# 自動クローズ with命令
'''
f が「条件分岐」、for が「繰り返し」を制御するのに対し、
with 文は 「コードの塊（ブロック）の前後で、 初期化（前処理）と
終了処理（後処理） を確実に実行させること」 を制御するために存在します
'''

#%% 7.2.2 テキストファイルを読み込む
with open('access.log','r',encoding='UTF-8')as file:
    data = file.read()
print(data)

#行単位にファイルを取得する readlinesメソッド
with open('access.log','r',encoding='UTF-8')as file:
    data = file.readlines()
for line in data:
    print(line,end='')
print(dir(file))
print(dir(file.read))
print(dir(file.readlines))

# fileオブジェクトをforでループする
with open('access.log','r',encoding='UTF-8') as file:
    #なぜopenに引き渡すパラメータは1、2文字なのに''で囲う？
    for line in file:
        print(line,end='')

#　シーク位置を変更する seekメソッド
#seekは実務的にはどんな所で役に立つのだろうか？
with open('access.log','r',encoding='UTF-8',
          newline='\n') as file:
    file.seek(6)
    for line in file:
        print(line,end='')

#%% 7.2.3 バイナリファイルの読み書き
with open("D:\python\input.png",'rb')as reader,\
     open('D:\python\input.png','wb')as writer:
         #ああ、readereとwirterを変数名としてデータ型指定して宣言していないのが、今更違和感を感じてくる。
         #\どんな意味だったけ汗？
         while d := reader.read(1):
             writer.write(d)

#%% 7.2.4 タブ区切り形式のテキストを読み書きする csv
# 1. テスト用のタブ区切りファイル（sample.tsv）を自動作成する
with open('sample.tsv', 'w', encoding='UTF-8') as f:
    f.write("ホスト名\tIPアドレス\t機種\n")
    f.write("Router-A\t192.168.1.1\tCisco\n")
    f.write("Switch-B\t192.168.1.2\tYamaha\n")
import csv
print(dir(csv))
help(csv)
with open ('sample.tsv',encoding='UTF-8')as f:
    for row in csv.reader(f,delimiter='\t'):
        for cell in row:
            print(cell)
        print('--------')
'''
ホスト名
IPアドレス
機種
--------
Router-A
192.168.1.1
Cisco
--------
Switch-B
192.168.1.2
Yamaha
--------
'''
