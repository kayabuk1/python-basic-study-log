# -*- coding: utf-8 -*-
"""
Created on Thu May 28 09:03:32 2026

@author: iot01
"""

#%% 9.1.1 デコレータの基本※教科書のコードは良いコードだが難しいので
#先生が簡単コードで解説してくれました。
#デコレータの目的は作った関数をカスタマイズする為
#関数 testを呼ぶだけ　←これに機能を付け加えて行く。
def test():
    print("hello")
test()
#デコレータ用の関数
#関数の中に関数があるのがデコレータの特徴
#⇒つまり関数が呼ばれたときに新たな関数オブジェクトを定義出来る＝作れる
def deco(func):
    #仮引数としてfuncと書いて関数オブジェクトが引き渡されることを
    #明示的にしている。 しかし、この時点では仮引数の名札funcを
    #作るだけ
    def inner():
        #関数内の関数に装飾する処理。
        print("---------")
        func()
        #func=関数オブジェクトとして仮引数に紐づけれて渡された関数自体
        #を呼び出す＝デコレート前の関数処理を実行している。
        #パーサーはfuncをスコープそとのenclose領域まで探しに行っていることに
        #注意。
    return inner
    #decc()が実行された時に、再定義された内部関数innerオブジェクト
    #自体を返す。
#関数 test呼ぶだけ
@deco #deco関数で次の関数をデコレートする　の意味。
#パーサーは@を見るとどんな判断をする？＠の意味は？
#decoは予約語？@の後ろにはdeco以外にも入る関数はあるの？
#パーサーにとって @ は、**「これから定義される関数を、指定した改造工場に入れて、
#元の名前のまま上書きしろ！」という絶対的な命令（シンタックスシュガー
#＝甘くコーティングされた省略記法）**です。
#公式ドキュメントでも、デコレータを導入する「デリミタ（区切り文字）および演算子」として
#定義されています
#つまり @ は、昨日面倒くさいと感じた
# log_hoge = log_func(hoge) のような**「関数の受け渡しと
#上書き」を全自動でやってくれる魔法の記号
def test():
    print("hello")
test()
    #---------
    #hello

#もし引数をデコレート付きの関数で表示しようとすると
@deco
def test(x):
    print("hello")
    print(x)
test(100)
#TypeError: deco.<locals>.inner() takes 0 
# positional arguments but 1 was given
#エラー：inner()関数の引数は０なのに、引数が1つ渡されたぞ

#エラーを解消するなら
def deco(func):#func=test(x)関数
    def inner(get_x):
        #get_x=100、仮引数が関数のように見えるがただの100
        print("--------")
        func(get_x)#元の関数test()に100を渡して実行させる
    return inner

@deco
def test(x):
    print("hello")
    print(x)
test(100)
#★ここで実行されているのは元のtest(x)関数ではなく、
#inner関数オブジェクト
    #--------
    #hello
    #100

#%% 9.1.4 引数を受け取るデコレーター
def log_func(details=True):
    #なぜ関数を外側に1つ増やさないと受け取れないのだろうか？
    #Q.log_func(detaile=Ture,func)ではダメなの？
    #関数を外側に1つ増やす理由」は、
    #『引数が渡されるタイミングが完全に2回に分かれているから』**です。
    #1回目（@ の行）：設定値（details）だけを渡して、
    #カスタマイズされた「デコレータ本体」を作る。
    #2回目（システムの裏側）：
    #作られたデコレータ本体に、システムが自動で「対象の関数（func）」を放り込む。
    #
    #引数を持たない単純なデコレータ @deco は、システムの裏側で
    #以下のように翻訳されることを学びました。 hoge = deco(hoge)
    #（deco 工場に hoge 関数オブジェクトを1つだけ投げて、出てきた
    #新製品に hoge の名札を貼り直す）
    #
    #では、今回の「引数を受け取るデコレータ 
    #@log_func(details=False)」をパーサーはどう翻訳するのでしょうか？
    #公式ドキュメント（8.7. 関数定義）の仕様に従うと、裏側では
    #以下の2段階の処理が行われます
    # 1. まず、@の直後にある式をそのまま 実行 し、その結果として
    #「デコレータ本体」を受け取る
    #temp_deco = log_func(details=False)
    # 2. 出来上がったデコレータ本体に対して、
    #下の関数(hoge)を1つだけ投げる！
    #hoge = temp_deco(hoge)
    #これを1行にまとめると、こうなります。
    #hoge = log_func(details=False)(hoge)
    #
    #もし def log_func(details, func): と設計したら？
    #2つの材料を同時に受け取る工場を作ったとしましょう。
    #def log_func(details, func):
    # ...
    #そして、@log_func(details=False) と書きます。
    #パーサーはまず、1段階目の log_func(details=False) を
    #実行しようとします。
    #しかしシステムは**「おい！ log_func 工場は details と
    #func の2つの材料が必要なのに、details しか渡されてないぞ！
    #func はどこいった！」**とパニックになり、TypeError: missing 1
    #required positional argument: 'func' を出してクラッシュします。
    #「じゃあ @log_func(details=False, hoge) って書けばいいじゃん！」と
    #思うかもしれませんが、**文法上 @ の行を書いている時点では、
    #すぐ下の def hoge の関数オブジェクトはまだ生成されていない
    #（存在しない）**ため、引数として渡すことは不可能なのです。
    #Q.つまり@()の時点で一度一番外側が実行されるの？
    #＠（）⇒log_func()⇒def hoge生成⇒hoge=inner???
    #少し流れが違う気がする。
    #A.@の後ろがカッコ付きだから先に実行して、帰ってきた関数を@にセット（待機）させてから下の行に進む
    def outer(func):
        def inner(*args, **keywds):
            print('--------------------')
            print(F'Name:{func.__name__}')
            if details:
                print(f'Args:{args}')
                print(f"Keywds:{keywds}")
            print("-------------------")
            return func(*args, **keywds)
        return inner
    return outer
@log_func(details=True)
#ここでデコレーター関数に渡す引数がdetaile=False or Trueで
#実行結果が変わる。
def hoge(x,y,m='bar',n='piyo'):
    print(F"hoge:{x}-{y}/{m}-{n}")
hoge(15,37,m='ほげ',n='ぴよ')
#実際に行われるのは@によって hoge = inner関数オブジェクトになっている
#False結果
#--------------------
#Name:hoge
#-------------------
#hoge:15-37/ほげ-ぴよ

#True結果
#--------------------
#Name:hoge
#Args:(15, 37)
#Keywds:{'m': 'ほげ', 'n': 'ぴよ'}
#-------------------
#hoge:15-37/ほげ-ぴよ

#%% 9.1.5 クロージャー　関数閉方
#ローカルスコープは関数の呼び出しの度に生成される。
# =c1とc2での変数countは別物
def counter(init):
    count = init
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
c1 = counter(1)
#counter()で呼び出された時点で 1に＋1する関数incrementが定義され、
#戻り値としても戻された、increment関数オブジェクトがc1名札に紐づけられる。
#c1（）はcallableなので呼び出して実行ができる。
c2 = counter(25)
print(c1())
print(c1())
print(c2())
print(c2())

#%%　9.2　ジェネレーター
# 9.2.1 yield命令
#Q.yieldとはどんな由来語源核となるイメージの単語？
#英単語の yield（イールド）には、大きく分けて以下の2つの意味
#そして、プログラミングにおける yield は、この両方のニュアンスを同時に体現しています。
#（農作物や利益などを）産出する、生み出す」：工場から製品（値）をポンッと外に出す。
#「（権利や道を）譲る、一時停止して明け渡す」
#作業を「一時停止（フリーズ）」して、呼び出し元の相手に処理の主導権を譲る。
#つまり yield の核となるイメージは、
#   **「値を一つだけ『産出』したら、そこで自分自身の動きをピタッと
#   『一時停止（主導権を譲る）』して、次の呼び出しが来るまで待機する」
#関数の中に yield という文字を一つでも見つけると、
#パーサは「おっ、これは普通の関数ではなく『ジェネレーター関数』だな！」と認識を切り替えます
def my_gen():
    yield 'あいうえお'
    yield 'かきくけこ'
    yield 'さしすせそ'
for value in my_gen():
    print(value)
    #あいうえお
    #かきくけこ
    #さしすせそ
##① 準備フェーズ (in my_gen():)
#システムの動き: for ループが my_gen() を呼び出します。
#しかし、ここでは中身の処理（文字列の産出）はまだ一切始まりません。
# システムは「とりあえず、一時停止・再開ができる特別なイテレータ
#（ジェネレータ・イテレータ）の装置を1つ作って渡しておくぞ」と
#、装置だけを for ループにセットします
#② 1回目の呼び出し
#システムの動き: for ループの裏側で、システムが「おい！1個目のデータをくれ！
#」（next()関数の呼び出し）と命令します
#Q.next（）とは？
#ジェネレーターが上から稼働し始め、yield 'あいうえお' に到達します。
#'あいうえお' をポンッと外に産出し、ジェネレーターはここでピタッと一時停止します
#for ループがそれを受け取り、画面に あいうえお と print します。
#③ 2回目の呼び出し
#システムの動き: for ループが「次をくれ！」と命令します。
#ジェネレーターは最初からやり直すのではなく、「前回一時停止した場所
#（1つ目の yield の直後）」から作業を再開します
#すぐ次の yield 'かきくけこ' に到達し、産出して再び一時停止します。
#画面に かきくけこ と表示されます。
#④ 3回目の呼び出し
#同じように前回停止した場所から再開し、yield 'さしすせそ' を産出して
#一時停止します。画面に さしすせそ と表示されます。
#⑤ 4回目の呼び出し（終了フェーズ）
#システムの動き: for ループが「次をくれ！」と命令し、ジェネレーターが再開します。
#しかし、もうその下には実行するコードがありません（関数の終端に到達しました）。
#ここでシステムは**「もう出すものがないぞ！」という意味の
# StopIteration（ストップ・イテレーション）という
#特別な例外サインを自動的に送出します**
#Q.これはNoneみたいなオブジェクトなの？
#for ループはこの StopIteration サインを裏側でこっそり受け取り
#、「あ、品切れだな」と察知して、エラーを出さずに綺麗にループを終了させます

print(my_gen())
#<generator object my_gen at 0x000001B606B41C70>
#generatorオブジェクトとは？

#%% 9.2.2　素数を求めるジェネレーター
import math
def get_primes():
    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1
def is_prime(value):
    result = True
    for i in range(2, math.floor(math.sqrt(value))+1):
        if value % i == 0:
            result = False
            break
    return result
gen = get_primes()
for prime in gen:
    print(prime)
    if prime > 100:
        #break
        #get_primes().close()
        #なぜ上だとエラーになる？
        #get_primes.close()
        #AttributeError: 'function' object has 
        #no attribute 'close'
        #なぜこれだとエラー
        #get_primes()、（）がついているから関数が実行される。
        #⇒普通の関数なら戻り値が返されるけれど、これは
        #内部でyieldが使われている＝()は実行ではなく
        # generator生成しろとの意味。なので、get_primes()は
        #generatorオブジェクトが生成されて戻って来て、
        #それにgenという名札が貼られるという理解で良い？
        #関数の中に yield が1つでも存在すると
        #、システム（パーサ）はその関数を「ジェネレーター関数」として
        #特別扱いし、() スイッチを押した時の挙動を根底から書き換えます。     
        #公式ドキュメント（3.2.8.3. ジェネレータ関数）にも、
        # **「yield 文を使う関数が呼び出されたときは常に、
        #関数の本体を実行するのに使えるイテレータオブジェクト
        #（ジェネレータ）を返します」**と明確に定義されています
        
        #gen.close()
        #↓ジェネレーターに例外を投げて止める
        gen.throw(ValueError('result is over 100!'))
        '''
        Traceback (most recent call last):

          Cell In[22], line 28
            gen.throw(ValueError('result is over 100!'))

          Cell In[22], line 6 in get_primes
            yield num

        ValueError: result is over 100!
        '''
'''
2
3
5
7
11
13
17
19
23
29
31
37
41
43
47
53
59
61
67
71
73
79
83
89
97
101
'''
#%% ジェネレーターに値を送出する(双方向通信)　sendメソッド
def gen_com():
    while True:
        n = yield input('名前を教えてください。')
        #ｎ に代入する前の段階＝右辺の実行して値を
        #呼び出し元に返してnameに代入するまでが行われる。
        # ＝ 式の途中で止まる。
        yield f'こんにちは、{n}さん！'
        #なぜyieldの行にはprintも要らないの？？？
        #画面に文字を出力」しているのではなく、あくまで
        #**「外の世界（forループ）に向けてデータを出荷（yield）」
        #しているだけ**だからです。画面に表示しているのは、
        #出荷されたデータを受け取った外の世界にある
        #9行目の print(res) の役割です。
gen = gen_com()
    #中で yield が使われているdefを見つけると構文解析器は、
    #関数オブジェクトでなく、 generatorオブジェクトとして生成する予定？
    #になる。 gen_com()は関数の実行ではなくgeneratorオブジェクトの
    #生成しろという指示になる。 それに名札genを貼っているので、
    #下のin gen でgenと書かれただけで、generatorが
    #一度目のyieldまで実行される。
for name in gen:
    res = gen.send(name.upper())
    print(res)
    #公式ドキュメントには、generator.send(value) の機能について以下のように
    #明確に定義されています。「ジェネレータ関数の内部へ値を "送り"、実行を
    #再開します。引数の value はその時点の yield 式の結果になります。
    #gen.send(大文字の文字列オブジェクト) が実行されジェネレータの中へ投げ込みます。
    #ジェネレータ内部での受け取りと名札付け n = yield input(...) の右辺で一時停止
    #していたジェネレータが物が飛んできたことで目を覚まします。
    #そして、飛んできた「大文字の文字列オブジェクト」がそのまま
    #yield 式の評価結果（値）となり、左辺の n という
    #ローカル変数の箱（名札）にガチャン！と格納（代入）されるのです。
'''
名前を教えてください。横須賀
こんにちは、横須賀さん！
名前を教えてください。yokosuka
こんにちは、YOKOSUKAさん！
名前を教えてください。
'''









