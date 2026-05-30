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
print(math.ceil(1234.567)) # 天井（切り上げ）1235
print(math.floor(1234.567)) # 天井（切り上げ）1234
print(math.trunc(1234.567)) # 0に向かっての切り捨て 1234
#正の数の場合: 1.9 を切り捨てると 1 になります。（0に近づく）
#負の数の場合: -1.9 を切り捨てると -1 になります。（0に近づく）
#これが「0に向かって」という意味です。
#もしこれを math.floor（床：常に小さい方へ切り捨てる）で処理すると、-1.9 はより小さい -2 に
#なってしまいます。math.trunc は、単純に**「小数点以下を見なかったことにして、物理的に削り落とす」
#*という直感的な処理を行います。
print(round(1234.567, 2)) #1234.57
#round() だけ、math. が付いていませんよね。
#これは round() が特別なモジュールを必要としない**「組み込み関数」**だからです。
# そして、基礎試験で最も狙われるのが、この round() の挙動です。
#多くの人は round() を「四捨五入」だと思い込んでいますが、
#Pythonの round() の正体は**「偶数丸め（銀行丸め）」です。
#もしちょうど中間の値（例：2.5 や 3.5）を round() に渡すと、
#Pythonは「四捨五入」ではなく「最も近い『偶数』の方向」**へ丸めます。
#round(2.5) ➔ 2 （※3にはなりません！）
#round(3.5) ➔ 4
'''
銀行丸め（偶数丸め）は、「常に結果を偶数にする機能」ではありません！ 
「丸める対象が、前後の『ちょうどド真ん中（5）』だった場合のみ、偶数側に引き寄せる」
という例外ルールのことです！
なぜこんな面倒なことをするのか？ インフラの実務で、数百万件のトラフィックデータや
金額データを集計するとします。もし小学校で習う「四捨五入（5は常に切り上げ）」を使うと、
データ全体がわずかに「大きい方向」へ偏って（上ブレして）しまいます。 
この上ブレによる誤差の蓄積を防ぐため、「真ん中の場合は、偶数（上か下か）に
均等に散らして統計的な偏りをなくそう」と考えたのが銀行家たちでした。
だから「銀行丸め（Banker's rounding）」と呼ばれ、
PythonやIEEE 754（浮動小数点数の世界標準）でデフォルト採用されているのです。
'''
print(pow(2, 4))
#16
#pow とは、「Power（べき乗）」の略です。
# 2 ** 4 と書くのと全く同じ処理です
#※ちなみに pow(x, y, z) のように3つ目の引数を与えると、
#「xのy乗を計算した後、zで割った余り（剰余）を出す」という、
#暗号技術（RSA暗号など）の計算で狂ったように多用される超高速な特殊機能に変化します。

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
#◆ randint と randrange の境界線
#この2つは「終端の数値（この場合は 10）を含めるかどうか？」という設計思想
#（ゲシュタルト）が完全に真っ二つに分かれています。
# random.randint(0, 10) ➔ 10を含む（完全ランダム）
#    「0から10までの間で、10も含めてどれかを出してくれ」という指示です。
# random.randrange(0, 10, 2) ➔ 10を含まない（シーケンス志向）
# 名前に range と付いているのが最大のヒントです！以前学んだ for i in range(0, 10):
# と全く同じルールが適用されるため、**「終端の10は絶対に選ばれない」**という
# 絶対法則が発動します（つまり選ばれるのは 0, 2, 4, 6, 8 のみです）。

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

# リストから要素をrandomに取り出すrandom 抽出三兄弟と「インプレース」の法則
#最も重要なのが random モジュールによる「リストからの抽出」です。
import random
data = ["大吉","中吉","小吉"]
print(random.choice(data))
#中吉
#random.choice(data) ＝ ランダムに 「1個」 だけ取り出す。
print(random.choice)
#<bound method Random.choice of <random.Random object at 0x0000021E74F31590>>
print(type(random.choice))
#<class 'method'>
print(type(random.choice(data)))
#<class 'str'

print(random.sample)
print(type(random.sample))
print(type(random.sample(data,2)))
print(random.sample(data,2))
#<bound method Random.sample of <random.Random object at 0x0000021E74F31590>>
#<class 'method'>
#<class 'list'>
#['小吉', '中吉']
#random.sample(data, 2) ＝ ランダムに 「複数個」 取り出すが、
#「重複なし（非復元抽出）」。タプルやリストから完全に別々のものを選ぶ時に使います。

print(random.choices)
print(type(random.choices))
print(type(random.choices(data, k=10)))
print(random.choices(data,k=10))
print(random.choices(data,weights=[1,10,1],k=10))
#<bound method Random.choices of <random.Random object at 0x0000021E74F31590>>
#<class 'method'>
#<class 'list'>
#['小吉', '中吉', '小吉', '小吉', '中吉', '小吉', '中吉', '大吉', '小吉', '小吉']
#['中吉', '大吉', '中吉', '中吉', '中吉', '中吉', '中吉', '中吉', '中吉', '中吉']
#random.choices(data, k=10) ＝ ランダムに「複数個」取り出すが、
#「重複あり（復元抽出）」。サイコロを何度も振るような動きです。
# 重み付け（weights）を設定できるのもこれだけです。

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
なぜ data = random.shuffle(data) と変数で受け取っていないのでしょうか？
そうです！**「元のリストそのものを直接破壊的変更（インプレース操作）するメソッドの
戻り値は None になる」**という絶対原則がここでも完全に発動しています。
だからこそ、戻り値を受け取らず、直接 data を出力しているのです！
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
'''
「ブール演算のコンテキストにおいて、（中略）以下の値は偽 (false) と解釈されます: 
False、None、すべての型の数値のゼロ、および空の文字列とコンテナ
(文字列、タプル、リスト、辞書、集合、凍結集合を含む)」。
つまり、システムにとって、
'' （空の文字列）
[] （空のリスト）
{} （空の辞書）
0 （数値のゼロ）
None （値なし）
これらはすべて、中身が何もない＝「False（偽）である」とみなすというアーキテクチャになっているのです。
'''

dec_num = int('10')
print(dec_num)
print(type(dec_num))
print(int)
print(type(int))
#10
#<class 'int'>
#<class 'int'>
#<class 'type'>

i_num = int('1.414')
print(i_num)
print(type(i_num))
#    i_num = int('1.414')
#ValueError: invalid literal for int() with base 10: '1.414'
'''
システムの裏側（パーサー）から見ると、int() 工場に文字列が渡された場合、
システムは「これが純粋な10進数の整数の文字列（0〜9のみで構成されているか）」を厳格にチェックします。
小数点が混ざった文字列を渡されると、システムは「おい！これは『1.414』っていう文字の並びであって、
整数の文字列じゃないぞ！」とパニックを起こし、意図しない値の混入を防ぐために
ValueError（値が適切でないエラー）を投げつけて安全に停止するのです。
これを解決するには、一度 float('1.414') で浮動小数点数の実体に変換してから、
int() 工場に渡す（int(float('1.414'))）という2段階の処理が必要です。
'''

hex_num = int('0x10',16)
print(hex_num)
print(type(hex_num))
#16
#<class 'int'>
#この文字列は16進数（あるいは2進数）だから、解読してPythonの10進数整数オブジェクトに変換してくれ！」
#というオーダー。MACアドレスやIPv6アドレス、VLAN IDなど、インフラの世界は「16進数の文字列」。

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










