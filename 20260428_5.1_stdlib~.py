# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 08:17:31 2026

@author: iot01
"""
import datetime
# datetimeオブジェクトの裏側（名前空間の辞書）に隠されているすべての
#属性とメソッドを暴く
print(dir(datetime))
'''
%runfile D:/python/20260428_.py --wdir
['MAXYEAR', 'MINYEAR', 'UTC', '__all__', '__builtins__',
 '__cached__', '__doc__', '__file__', '__loader__', 
 '__name__', '__package__', '__spec__', 'date', 
 'datetime', 'datetime_CAPI', 'sys', 'time', 
 'timedelta', 'timezone', 'tzinfo']
'''
today = datetime.date(2020,11,10)
print(today)
    #2020-11-10
print(today.year)
    #2020
a = print
a(today)
    #2020-11-10
current = datetime.date.today()
a(current)
    #2026-04-28
'''
1. 通常ルート（人間が手作業で組み立てる場合）
人間がOSのカレンダーや時計を見て、今日が「2026年、4月、28日」であることを自力で調べる。
その調べた材料を使って、
    today_obj = datetime.date(2026, 4, 28) 
と手作業で引数を渡し、インスタンスを作る。 ※もし明日コードを実行するなら、人間が
毎日コードの引数（数字）を手動で書き換えなければなりません。
2. today() ルート（全自動の工場に任せる場合）
人間は 
    today_obj = datetime.date.today() 
と、「今日の日付の完成品をくれ！」とクラス（工場長）に発注するだけ。
クラス（工場長）が裏側で勝手にOSの時計を調べに行き
、「2026, 4, 28」という材料を自動でかき集める。
システムが裏側でゼロからインスタンス（箱）を生成し、
人間の手元に完成品としてポーンと返してくれる。
'''

#%%# 5.2 文字列の操作
#5.2.1 文字列の長さを取得する。
title = 'WINGSプロジェクト'
print(len(title))
    #11
#↓半角1文字、全角2文字換算にしたい場合（1文字ずつしか判定できない）
import unicodedata
count = 0
for ch in title:
    if unicodedata.east_asian_width(ch) in 'FWA':
        count +=2
    else:
        count +=1
print(F'{title}は{count!r}文字です！')
    #WINGSプロジェクト17文字です！

#%% 5.2.2 文字列を大文字 ⇔ 小文字で変換
print(dir(str))
'''
['__add__', '__class__', '__contains__', '__delattr__',
 '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
 '__getattribute__', '__getitem__', '__getnewargs__', 
 '__getstate__', '__gt__', '__hash__', '__init__', 
 '__init_subclass__', '__iter__', '__le__', '__len__', 
 '__lt__', '__mod__', '__mul__', '__ne__', '__new__', 
 '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', 
 '__rmul__', '__setattr__', '__sizeof__', '__str__', 
 '__subclasshook__', 'capitalize', 'casefold', 'center', 
 'count', 'encode', 'endswith', 'expandtabs', 'find', 
 'format', 'format_map', 'index', 'isalnum', 'isalpha', 
 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 
 'islower', 'isnumeric', 'isprintable', 'isspace', 
 'istitle', 'isupper', 'join', 'ljust', 'lower', 
 'lstrip', 'maketrans', 'partition', 'removeprefix', 
 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust', 
 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 
 'startswith', 'strip', 'swapcase', 'title', 'translate', 
 'upper', 'zfill']
'''
data1 = 'Touhou Project'
data2 = 'self learn python'
data3 = 'Großer Zappenheim'
ip_data4 = '192.168.1.254'
data5 = ' up\n'
data6 = 'ERROR：エラーでなくて警告という意味にしよう！'
    #ß（エスツェット）はAlt＋0223(テンキー限定)で表示可能
print(data1.lower())#touhou project
print(data1.upper())#TOUHOU PROJECT
print(data1.swapcase())#tOUHOU pROJECT
print(data2.capitalize())#Self learn python
print(data2.title())#Self Learn Python
'''
英語には 「Title Case（タイトルケース）」 という厳格な文法ルールがあります。 
新聞の見出し、本の題名、映画のタイトルなどを書くときは、**「一番最初の単語と、
前置詞（inやon）などを除くすべての主要な単語の先頭を大文字にしなければ
ならない」**という絶対的なルールがあります。 
（例：名作映画『Back to the Future』など。
'''
print(data3.lower())#großer zappenheim
print(data3.casefold())#grosser zappenheim
    #fold（折りたたむ・平らにする）。 lower() よりも強力
print(ip_data4.split('.'))#['192', '168', '1', '254']
print(*ip_data4.split('.'))#192 168 1 254
print(data5.strip())#up
print(data6.replace("ERROR", "WARNING"))
    #WARNING：エラーでなくて警告という意味にしよう！
print(data6.startswith("Error:"))#False
    #if line.startswith("Error:"):のように使う
print(data6.startswith("ERROR："))#True
'''
1. 「関数（引数渡し）」と「メソッド（ドット呼び出し）」の区別のつけ方
【【結論】
関数（ 関数名(データ) ） ＝ どんな型（箱）にも使える 「外にある汎用的な
                      メジャーやハカリ」 です。
メソッド（ データ.メソッド名() ） ＝ その型（今回は文字列）の箱の中にだけ
                       組み込まれている 「専用の操作ボタン」 です。
【なぜ引数に渡さなくていいのか？（違和感の解消）】 
C言語であれば、文字列を小文字にするには
 lower(data1) のように引数として渡すのが当然です。 
 しかし、先ほど「 self（自分自身）の暗黙の差し込み」で学んだことを思い出してください。
data1.lower() とドットで呼び出した瞬間、システムは裏側で
 str.lower(data1) と自動変換して実行しています。 
 つまり、「主語（ data1 ）自身がすでに第一引数として裏側で渡されているから、
 カッコの中は空っぽで良い（渡す必要がない）」 のです。
 【区別のつけ方（メンタルモデル）】
「文字列の長さを測る」など、リストや辞書など他のデータ型にも共通して使えそうな処理は、
汎用関数（例： len(data1) ）として用意されています。
「大文字・小文字を変換する」など、文字列というデータ型にしか絶対にあり得ない処理は、
文字列専用のメソッド（例： data1.lower() ）として用意されています。
'''
#%% 5．2.3 部分文字列を取得する（インデックス/スライス構文）
print(dir(slice))
'''
['__class__', '__delattr__', '__dir__', '__doc__', 
 '__eq__', '__format__', '__ge__', '__getattribute__', 
 '__getstate__', '__gt__', '__hash__', '__init__', 
 '__init_subclass__', '__le__', '__lt__', '__ne__', 
 '__new__', '__reduce__', '__reduce_ex__', '__repr__', 
 '__setattr__', '__sizeof__', '__str__', 
 '__subclasshook__', 'indices', 'start', 'step', 'stop']
'''
title = '123456789ⅹ'
print(title[2])#3
print(title[2:5])#345
print(title[2:])#3456789ⅹ
print(title[:5])#12345
print(title[:])#123456789ⅹ
print(title[-7:])#456789ⅹ
print(title[-7:-5])#45
print(title[::2])#13579
print(title[1::2])#2468ⅹ
print(title[::-1])#ⅹ987654321














