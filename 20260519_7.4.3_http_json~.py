# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:48:51 2026

@author: iot01
"""
#%% 7.4.3 JSONデータを取得する
import requests
res = requests.get('http://wings.msn.to/tmp/books.json')
#requestsモジュールの部屋から get という通信用の道具（関数）を取り出し、URLを渡して実行します。
#この関数は、Webサーバーと通信を行い、返ってきた結果
#（ステータスコード、生のテキスト、通信ヘッダーなど）を全て1つのカプセルに詰め込んだ
#**「Responseオブジェクト（実体）」**を生成しします。それに res という名札を付けます。
bs = res.json()
#res オブジェクトが持っている json() という機能（メソッド）を実行しています。
#Webから送られてくるJSONデータは、システムにとってはただの「単なる文字列（テキスト）」
#にすぎません。json() メソッドは、この文字列を構文解析し、Pythonが扱いやすい
#**「辞書（ディクショナリ）とリストの組み合わせ」へと自動的に変換（デシリアライズ）**してくれます
#変換後の辞書オブジェクトに bs という名札を付けています。
#⇒pythonには型、クラスが無数に存在するから、wgetしたデータがresponesオブジェクトで、
#  .json()メソッドを持っているし、使わないとな。という風に使える様になるにはどうしたら良い？
#  たとえ、resoponseオブジェクトの処理のテンプレは覚えても他のクラスやメソッドはどう型に嵌めて
#  覚えたら良いのだろうか？
'''
1.「お前は誰だ？」と尋ねる ➔ print(type(res)) 
    「なるほど、お前は <class 'requests.models.Response'> というクラスから生まれた実体だな」と特定。
2.「お前は何ができるんだ？」と尋ねる ➔ print(dir(res)) 
    「おっ、レントゲンスキャンしたら .json や .text、.status_code なんていう機能（メソッドや属性）
    を持っているじゃないか」と使える武器を一覧化します。
3.「どうやって使うんだ？」と尋ねる ➔ help(res.json) （対話モードなどで）
    help() 関数に放り込んで、そのメソッドの公式な説明書（docstring）を直接読み込みます。
この「type(), dir(), help()」の3種の神器を使えば、どんな未知のライブラリの、
どんな未知のクラスが返ってきても、その場で使い方を解読できるようになります。
'''
print(bs)
#%runfile 'D:/python/20260519_7.4.3_http_json~.py' --wdir
#辞書型に変換されたデータの中身全体を画面に出力します。
#⇒runfile＝実行ファイル？、--wdirとは？
#%runfile ＝ 「今から指定するパスのPythonファイルを、まるごと実行しろ！」
#というIPython専用の命令（% で始まるのはマジックコマンドと呼ばれます）。
#--wdir ＝ 「Working Directory（作業ディレクトリ）」の略です。
#「実行する時のカレントディレクトリ（現在位置）を、ファイルの場所と同じに設定してね」というオプション。
print(bs['books'][0]['title'])
#独習Java 新版
#変換された辞書・リストから、ピンポイントでデータを抽出しています。
#① bs['books'] ➔ 辞書の中から books というキーで「リスト」を取り出す。
#② `` ➔ そのリストの「0番目（最初）の要素（これも辞書）」を取り出す。
#③ ['title'] ➔ その辞書の中から `title` というキーの値を取り出す。 
#結果として、 `'独習Java 新版'` という文字列が抽出され、出力されます。
#⇒これリストが[[[]]]三重になっているのか？なぜそんな面倒くさい構造に？
#「世界中のどんな複雑なデータも、たった2つの型（辞書とリスト）の組み合わせだけで表現する」
#というJSONのアーキテクチャだから。
# これが生データ（res.text）の正体です。
# 両端がシングルクォートで囲まれた、ただの「1つの文字列（str型）」です。

'{"books": [{"title": "独習Java 新版", "price": 2980}, {"title": "独習Python", "price": 3300}]}'
# 取得した bs の本当の姿（.json() メソッドを実行した「後」のPython専用オブジェクト（辞書とリスト）の姿）
{ # ① 一番外側は「辞書（ディクショナリ）」
    'books': [ # ② 'books' というキーの中身は、複数の本を格納する「リスト（配列）」
        { # ③ リストの0番目（1冊目の本）。これはまた「辞書」になっている
            'title': '独習Java 新版', # ④ その辞書の 'title' というキー
            'price': 2980
        },
        { # リストの1番目（2冊目の本）...
            'title': '独習Python',
            'price': 3300
        }
    ]
}
print(requests.get)
print(requests)
#<function get at 0x0000021E7F439300>
#<module 'requests' from 
# 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib\\site-packages\\requests\\__init__.py'>
#⇒paizeで実行して結果見ようとしたら、
#Traceback (most recent call last):
#  File "/workspace/Main.py", line 2, in <module>
#    import requests
#ModuleNotFoundError: No module named 'requests'
print(res.text)
#Webサーバーから送られてきた「生のJSON文字列」がそのまま入っています。
print(res.json)
# <bound method Response.json of <Response>？
print(type(res))
#<class 'requests.models.Response'> となります。
#「これはただの文字列や辞書ではなく、Requestsモジュール専用に作られた
#『Responseクラス』のインスタンスである。
print(dir(res))
print(dir(requests))

#%%# 7.5 その他の機能
# 7.5.1　数学演算 mathモジュール+組み込み関数
import math
print(abs(-100))
print(abs(100))
print(math.ceil(1234.567))
print(math.floor(1234.567))
print(math.trunc(1234.567))
print(round(1234.567, 2))

print(pow(2, 4))

#%% 7.5.2 乱数を生成する　randomモジュール
import random
print(random)
print(random.random)
print(type(random))

print(type(random.random))
print(random.random())
print(type(random.random()))

print(random.randint)
print(type((random.randint(0, 10))))
print(type(random.randint))
print(random.randint(0, 10))

print(random.randrange)
print(type(random.randrange))
print(random.randrange(0,10,2))
print(type(random.randrange(0,10,2)))

print(random.uniform)
print(type(random.uniform))
print(random.uniform(1, 10))
print(type(random.uniform(1, 10)))

print(random.gammavariate)
print(type(random.gammavariate))
print(random.gammavariate(15, 20))
print(type(random.gammavariate(15, 20)))
'''
<module 'random' from 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib\\random.py'>
<built-in method random of Random object at 0x0000021E74F31590>
<class 'module'>
<class 'builtin_function_or_method'>
0.20226297997340026
<class 'float'>
<bound method Random.randint of <random.Random object at 0x0000021E74F31590>>
<class 'int'>
<class 'method'>
2
<bound method Random.randrange of <random.Random object at 0x0000021E74F31590>>
<class 'method'>
8
<class 'int'>
<bound method Random.uniform of <random.Random object at 0x0000021E74F31590>>
<class 'method'>
5.895058918465637
<class 'float'>
<bound method Random.gammavariate of <random.Random object at 0x0000021E74F31590>>
<class 'method'>
235.02734182640557
<class 'float'>
'''

# リストから要素をrandomに取り出す
import random
data = ["大吉","中吉","小吉"]
print(random.choice(data))
print(random.choice)
print(type(random.choice))
print(type(random.choice(data)))

print(random.sample)
print(type(random.sample))
print(type(random.sample(data,2)))
print(random.sample(data,2))

print(random.choices)
print(type(random.choices))
print(type(random.choices(data, k=10)))
print(random.choices(data,k=10))
print(random.choices(data,weights=[1,10,1],k=10))

'''
中吉
<bound method Random.choice of <random.Random object at 0x0000021E74F31590>>
<class 'method'>
<class 'str'>
<bound method Random.sample of <random.Random object at 0x0000021E74F31590>>
<class 'method'>
<class 'list'>
['小吉', '中吉']
<bound method Random.choices of <random.Random object at 0x0000021E74F31590>>
<class 'method'>
<class 'list'>
['小吉', '中吉', '小吉', '小吉', '中吉', '小吉', '中吉', '大吉', '小吉', '小吉']
['中吉', '大吉', '中吉', '中吉', '中吉', '中吉', '中吉', '中吉', '中吉', '中吉']
'''

#リストを任意順序にシャッフルする
import random
data = ["大吉","中吉","小吉"]
random.shuffle(data)
print(data)
print(type(data))
print(random.shuffle)
print(type(random.shuffle))
'''
['大吉', '小吉', '中吉']
<class 'list'>
<bound method Random.shuffle of <random.Random object at 0x0000021E74F31590>>
<class 'method'>
'''

#%% 7.5.3 データ型を変換/判定する　int/float関数など
print(bool(''))
print(bool)
print(type(bool))
print(type(bool('')))
#False
#<class 'bool'>
#<class 'type'>
#<class 'bool'>

dec_num = int('10')
print(dec_num)
print(type(dec_num))
print(int)
print(type(int))
#10
#<class 'int'>
#<class 'int'>
#<class 'type'>

#i_num = int('1.414')
#print(i_num)
#print(type(i_num))
#    i_num = int('1.414')
#ValueError: invalid literal for int() with base 10: '1.414'

hex_num = int('0x10',16)
print(hex_num)
print(type(hex_num))
#16
#<class 'int'>

f_num = float('1.414e-5')
print(f_num)
print(type(f_num))
print(type(float))
#1.414e-05
#<class 'float'>
#<class 'type'>

print(dir())
print(dir(dir))
print(dir(type))
#print(dir(class))










