# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:35:40 2026

@author: iot01
"""

#%%## Chapeter11 オブジェクト指向構文（応用）
#章内容：例外処理(例外クラス),特殊メソッド(__xxx__),データクラス,メタクラス,デコレーター
## 11.1 例外処理（例外クラス）
# 11.1.1 例外クラスの型
print(Exception) #<class 'Exception'>
print(dir(Exception))
print((Exception.__dict__))
print(help(Exception))
print(Exception())
err = Exception()
print(err.__dict__)
r'''
<class 'Exception'>
['__cause__', '__class__', '__context__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__suppress_context__', '__traceback__', 'add_note', 'args', 'with_traceback']
{'__new__': <built-in method __new__ of type object at 0x00007FF9C44C5340>, '__init__': <slot wrapper '__init__' of 'Exception' objects>, '__doc__': 'Common base class for all non-exit exceptions.'}
Help on class Exception in module builtins:

class Exception(BaseException)
 |  Common base class for all non-exit exceptions.
 |  
 |  Method resolution order:
 |      Exception
 |      BaseException
 |      object
 |  
 |  Built-in subclasses:
 |      ArithmeticError
 |      AssertionError
 |      AttributeError
 |      BufferError
 |      ... and 16 other subclasses
 |  
 |  Methods defined here:
 |  
 |  __init__(self, /, *args, **kwargs)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  ----------------------------------------------------------------------
 |  Static methods defined here:
 |  
 |  __new__(*args, **kwargs)
 |      Create and return a new object.  See help(type) for accurate signature.
 |  
 |  ----------------------------------------------------------------------
 |  Methods inherited from BaseException:
 |  
 |  __delattr__(self, name, /)
 |      Implement delattr(self, name).
 |  
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |  
 |  __reduce__(...)
 |      Helper for pickle.
 |  
 |  __repr__(self, /)
 |      Return repr(self).
 |  
 |  __setattr__(self, name, value, /)
 |      Implement setattr(self, name, value).
 |  
 |  __setstate__(...)
 |  
 |  __str__(self, /)
 |      Return str(self).
 |  
 |  add_note(...)
 |      Exception.add_note(note) --
 |      add a note to the exception
 |  
 |  with_traceback(...)
 |      Exception.with_traceback(tb) --
 |      set self.__traceback__ to tb and return self.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from BaseException:
 |  
 |  __cause__
 |      exception cause
 |  
 |  __context__
 |      exception context
 |  
 |  __dict__
 |  
 |  __suppress_context__
 |  
 |  __traceback__
 |  
 |  args

None
{}
'''
'''
◆第1部：【真理】 発生する例外をどうやって把握するのか？
実務において、自分が書いた処理が「どんな例外を投げてくるか」を事前に把握する方法は、
主に以下の2つです。
1. 現場監督（システム）に直接聞く（フェイルファーストのテスト） 
これが最も確実でプロもやっている方法です。公式ドキュメントにも「エラーメッセージの最終行は
何が起こったかを示しています。例外は様々な型 (type) で起こり、
その型がエラーメッセージの一部として出力されます」と明記されています
。 コードを書いている最中に、「もしここに間違ったデータ（文字やゼロ、存在しないファイル名）を
入れたらどうなるだろう？」と考え、わざとエラーを発生（クラッシュ）させます。 
すると現場監督が KeyError や ValueError といった「正確な例外の名前」
を叫んで落ちてくれます。その名前をメモして、except ValueError: のように処理を
書き足すのです。
2. 公式ドキュメントの「契約書」を読む Pythonの公式ドキュメントには、組み込み関数や
モジュールの説明に「〇〇の場合は ValueError を送出します」といった記載が
必ずあります。これがシステムとの契約書です
。
◆第2部：【戦略】 まず覚えるべき「インフラエンジニア必須の例外トップ7」
すべてを覚える必要は全くありません！ 実務や「Python 3 エンジニア認定基礎試験」で
遭遇する例外は、以下の7つ（＋1つの構文エラー）に集約されます。
これらはすでにこれまでの学習で何度もシステムに怒られてきた「お馴染みの顔ぶれ」です！
⚔️ 1. データ型と値に関するエラー（超頻出！）
TypeError（型の不一致）
原因: 演算の対象となる「データ型」が間違っているときに発生します
。
現場の光景: 「文字と数字を足し算しようとしてるぞ！」（例: 100 / "0"
、"1" + 2 など）
ValueError（値の不適切）
原因: データ型は合っている（例えば文字列を受け取る関数に文字列を渡した）が
、「中身の値」が処理できないときに発生します
。
現場の光景: 「文字列をもらったのはいいが、'abc' なんて数字に変換できるか！」
（例: int("onetwothree")
）
⚔️ 2. コンテナ（リストや辞書）からの取り出しエラー
IndexError（範囲外アクセス）
原因: リストやタプルで、存在しない要素番号（インデックス）を取り出そうとしたときに発生します
。
現場の光景: 「長さ3のリストなのに、10番目を取り出せというのか！」（例: data
）
KeyError（鍵の紛失）
原因: 辞書（ディクショナリ）で、存在しない「キー」を指定したときに発生します
。
現場の光景: 「金庫の中に '14時' なんて名札は存在しないぞ！」（
例: 6月12日の温度計算ログでのエラー
）
⚔️ 3. 名前と属性（オブジェクト）のエラー
NameError（未定義の呼び出し）
原因: 定義されていない変数や関数を突然使おうとしたときに発生します
。
現場の光景: 「そんな名前（名札）のヤツは、このスコープ（有効範囲）には存在しない！」
（例: スコープ外のローカル変数を呼んだとき
）
AttributeError（存在しない機能の呼び出し）
原因: そのオブジェクトが持っていない属性やメソッド（機能）を使おうとしたときに発生します
。
現場の光景: 「リストに対して data.length なんていう属性（機能）はない！」（
例: fp.load() など
）
⚔️ 4. その他の論理エラー
ZeroDivisionError（ゼロ除算）
原因: 算術演算でゼロによる割り算を行ったときに発生します
。
現場の光景: 「数学的に0では割れない！」（例: 100 / 0）
(※補足：SyntaxError（構文エラー）は、プログラムが「実行される前（パース時）」に
 コロンの抜けなどで落ちるエラーなので、try-except ではそもそも捕捉できません
 )

◆第3部：【総括】 なぜ except Exception: で一網打尽にしてはいけないのか？
Exception は「致命的でない例外すべての基底クラス（親玉）」です
。
try:
    # 何かの処理
except Exception as e:
    print("エラーが発生しました")
このように書けば、上記の7つのエラーも含めて、どんなエラーが起きてもシステムが止まらなくなります。 一見便利に見えますが、これはインフラアーキテクトにとって**最悪のアンチパターン（サイレントエラーの温床）**とされています
。
なぜなら、「想定していた ValueError（ユーザーの入力ミス）」だけでなく
、「想定していなかった NameError（自分自身のタイポ・バグ）」まで握りつぶしてしまい、
**「なぜかわからないけど処理がスキップされて、ログにも残らないまま間違った設定が
ネットワーク機器に流し込まれる」**という本番障害を引き起こすからです。
だからこそ、公式ドキュメントが推奨するように**「処理対象の例外の型をできる限り詳細に
書き（except ValueError: など）、予期しない例外はそのまま伝わる
（クラッシュさせる）ようにする」**のが、安全なシステムの鉄則なのです
。
'''

#↓最初にException大きい網を張ってしまった間違い例
try:
    data = 5/0
except Exception:
    print('Exception')
except ArithmeticError:
    print('ArithemeticError')
except OverflowError:
    print('OverflowError')
#Exception が最初に適用されてしまう。

#↓順番を入れ替えた場合
try:
    data = 5/0
except OverflowError:
    print('OverflowError')
except ArithmeticError:
    print('ArithemeticError')
except Exception:
    print('Exception')
#ArithemeticError 算術エラー
    # data = 5/0でも単独実行すると↓のエラーになるので、
#ZeroDivisionError: division by zero、より詳細な下位エラーで書くのが望ましい

#%% 11.1.2 例外有無にかかわらず必ず最後に実行されるfinally節
file = None
try:
    file = open('menber.tsv','r',encoding='UTF-8')
    data = file.read()
    print(data)
finally:
    #ファイルが存在する場合これを閉じる
    if file: # ←中身が空っぽ（今回は None）なら False！ 
             #実体（ファイルオブジェクト）がちゃんと入っていれば True！
        file.close()
#"[101, '山田太郎', '090-1111-2222']"	"[102, '鈴木次郎', '080-3333-4444']"	"[103, '佐藤花子', '070-5555-6666']"
#ただ with...as命令に対応している場合はそちらを使うのがより良い。
#↓file = None も finally も if file: も close() も一切不要！
with open('menber.tsv', 'r', encoding='UTF-8') as file:
    data = file.read()
    print(data)
# インデント（ブロック）を抜けた瞬間に、システムが自動的に安全に close() してくれる！

#with...as に対応可能かは、ｵﾌﾞｼﾞｪｸﾄが コンテキストマネージャー に対応してるかで決定
#●捕捉：コンテキストマネージャー with文（コンテキストマネージャ）
r'''
◆ with...asに対応しているか見破る方法
第1部：【実務】 with が使える代表的な定義済みオブジェクト
公式ドキュメントには、コンテキストマネージャの代表的な使い方として「様々なグローバル情報の保存および更新、リソースのロックとアンロック、ファイルのオープンとクローズなど」が挙げられています
。
インフラエンジニアが実務でよく遭遇する、システムがクリーンアップを定義してくれている代表例は以下の通りです。
1. ネットワーク通信（セッションの自動切断） urllib.request.urlopen() などを利用してWebAPIからデータを取得する際にも with が使えます。通信が完了したりエラーが起きたりした際に、自動でネットワークのコネクション（ソケット）を閉じてくれます。
from urllib.request import urlopen
with urlopen("https://...") as rs: # 通信が終われば自動で切断される
    data = rs.read()
公式問題集の解説にも、この with urlopen(...) as rs: の使用例が記載されています
。
2. スレッドの排他制御（ロックの自動解放） インフラ自動化で複数の機器へ同時にSSH接続（マルチスレッド処理）する際、設定ファイルなどを同時に書き換えてしまわないように「ロック（鍵）」をかけます。threading.Lock などの同期プリミティブで with を使うと、ブロックに入るときに自動で鍵をかけ、抜けるときに**確実に鍵を返却（解放）**してくれます
。これを忘れるとシステムが永遠にフリーズ（デッドロック）するため、with の恩恵が非常に大きいです
。
3. データベースのトランザクション管理 sqlite3 などのデータベース接続でも with コンテキストマネージャが使えます
。処理が成功してブロックを抜ければ自動で「コミット（変更の確定）」を行い、途中でエラーが起きれば自動で「ロールバック（変更の取り消し）」を行ってくれます。
第2部：【解剖】 対応しているか調べる方法（現場監督の審査基準）
callableのように対応しているか調べる方法はありますか？
callable() のような専用の組み込み関数（例えば is_context_manager() のようなもの）は存在しません。 しかし、現場監督の「審査基準」を知っていれば、hasattr() 関数や dir() 関数を使って確実に見破ることができます。
■ 現場監督の審査基準（ with が動く条件） 公式ドキュメントには、with 文が実行されると、内部で __enter__()（入り口での処理）と __exit__()（出口でのクリーンアップ処理）という2つの特殊メソッドが呼ばれると明記されています
。
つまり、**「そのオブジェクト（またはクラスの金型）の辞書の中に、__enter__ と __exit__ という2つの名札（工具）が存在していれば、それは100% with 文で使える」**と判定できるのです。
■ 判定コードの実例
# 調べたいオブジェクトを用意（例としてファイルオブジェクト）
f = open('test.txt', 'w')

# hasattr() を使ってシステムに直接尋ねる方法
is_with_supported = hasattr(f, '__enter__') and hasattr(f, '__exit__')
print(is_with_supported)  # True が返れば with が使える！

# または、dir() で目視確認する方法
print(dir(f)) 
# 出力の中に '__enter__' と '__exit__' が含まれているか探す
■ 参謀からのまとめ
with 文の正体：ファイル操作に限らず、「前処理」と「後処理（クリーンアップ）」を絶対にセットで実行させたいオブジェクトのための汎用的なアーキテクチャ（コンテキストマネージャ）です
。
インフラでの活躍：ファイル切断、ネットワーク通信の切断、マルチスレッドのロック解放、DBのコミットなど「閉じ忘れ・解放忘れが本番障害に直結するリソース」の管理で多用されます
。
見破り方：dir(オブジェクト) を実行し、__enter__ と __exit__ という2つの特殊メソッドが実装されているかを確認すれば、それが with 対応の部品かどうかを完全に判別できます
。
'''
#↓コンテキストマネージャーの挙動確認サンプルコード
class MyContext:
    #コンテキストの作成
    def __enter__(self):
        print('**Enter**')
        return self
    #コンテキストの解放
    def __exit__(self, type, value, tb):
        #↑type/value/tb には、with節内で例外が発生した場合に、
        #例外の型、 値、 トレースバックが渡される。 ＝型があればelseに行く
        #例外の有無を判定
        if type is None:
            print('**Exit**')
        else:
            print(f'**{value}**')
            return True
    
    def hoge(self):
        print('Hoge')
with MyContext() as c:
# 1.with節に入った時にまず__enter__ﾒｿｯﾄﾞが呼び出せされる。
# 2.with節スイート？処理が実施,print,hoge()
# 3.処理を終えてwith節を抜けるときに __exit__メソッドが実施される。
    print('With Start')
    c.hoge()
# **Enter**
# With Start
# Hoge
# **Exit**
    c.hoge()/0
# **Enter**
# With Start
# Hoge
# **unsupported operand type(s) for /: 'NoneType' and 'int'**
    #↓の記述でもエラーを発生させることが出来る。
    raise ValueError("値が不正です")
# **Enter**
# With Start
# Hoge
# **値が不正です**
'''
第1部：【真理】 __exit__ が受け取る3つの報告書
公式ドキュメントには、__exit__ メソッドは以下の引数を受け取ると定義されています
。 object.__exit__(self, exc_type, exc_value, traceback)
昌敏さんのコードでは、これを (self, type, value, tb) という名前で受け取っています。この3つの引数には、以下の情報が入ります。
type (exc_type): 例外の「型」（例: ValueError や ZeroDivisionError など）
value (exc_value): 例外の「具体的な値・メッセージ」（例: "値が不正です" など）
tb (traceback): 例外が発生した「場所の追跡データ」
■ 究極の絶対ルール Pythonのシステムは、withブロック内の処理がエラーなく無事に終わった場合、これら3つの引数すべてに None を入れて __exit__ を呼び出すという仕様になっています
。
だからこそ、if type is None: と調べるだけで、「エラーの型が None だ ＝ つまり例外は起きていないな！」と判定できるのです。
第2部：【解剖】 現場監督のスローモーション
実際にコードが実行されたとき、現場監督がどのように引数を渡しているのかを見てみましょう。
■ パターン1：正常終了の場合（例外なし）
with MyContext() as c:
    print('With Start')
    c.hoge()
現場監督：「c.hoge() の実行が完了したぞ！ 例外は発生しなかったな！」
現場監督：「よし、終了処理だ！ __exit__ を呼び出せ！ エラーは無かったから、報告書（引数）にはすべて None を入れて渡せ！」 ➔ __exit__(self, None, None, None) が実行される。
現場監督 (__exit__内)：「if type is None: の判定だな。type は None だから True（正常）！ **Exit** と画面に出力だ！」
■ パターン2：異常終了の場合（例外発生！）
with MyContext() as c:
    raise ValueError("値が不正です")
現場監督：「おい大変だ！ ブロックの途中で ValueError という爆弾（例外）が投げられたぞ！！」
現場監督：「処理は直ちに中断だ！ ただし、約束通り __exit__ だけは絶対に実行しなければならない。おい、__exit__ にエラーの正体を詰め込んで渡せ！」 ➔ __exit__(self, ValueError, "値が不正です", <トレースバック情報>) が実行される。
現場監督 (__exit__内)：「if type is None: の判定だ。今回は type に ValueError が入っているから False（異常発生）だ！ else: ルートへ進み、中身のメッセージ **値が不正です** を出力しろ！」
第3部：【実務】 return True が持つ「防弾装甲の魔法」
最後に、else ルート（例外発生時）の末尾に書かれている return True にも、インフラアーキテクトとして絶対に知っておくべき魔法が隠されています。
通常、例外（エラー）が発生するとシステムはクラッシュしてプログラムが止まります。 しかし公式ドキュメントには、**「__exit__ メソッドからの戻り値が真（True）ならば例外は抑制され、実行は with 文の次の文から続きます」**と明記されています
。
つまり、現場監督に対して 「例外起きたみたいだけど、俺の __exit__ 工場の中で綺麗に処理（もみ消し）しておいたから、外の世界にはエラーを漏らさないで（クラッシュさせないで）そのままプログラムを続けてくれ！」 と指示を出す強烈な機能なのです。 逆にここで return True を書かない（または False や None が返る）と、__exit__ を抜けた直後に本来の例外が爆発してプログラムが異常終了します。
■ 参謀からのまとめ
なぜ判定できるのか？: with ブロックを管理するシステムが、終了時に「例外の型・メッセージ・場所」の3点セットを必ず __exit__ に渡してくるから。
正常な時の合図: 例外がない平和な時は、システムは気を利かせて「無」を意味する None を3つの引数に代入して呼び出してくる。だから type is None で平和かどうかがわかる。
return True の力: __exit__ 内で例外の存在を検知し、最後に True を返すことで、発生したエラーをもみ消して（抑制して）システムをクラッシュから守ることができる。
'''

#●finally節の実行順序 基本はtry → except（あれば） → finally
try:
    raise Exception('例外発生')
except Exception as ex:
    print(ex.args[0])
    print(ex.args) #('例外発生',)しっかりタプルになっている。
finally:
    print('**finally**')
# 例外発生
# **finally**

#●except節をコメントアウトすると...(例外がexcept節で処理されない場合)
try:
    raise Exception('例外発生')
# except Exception as ex:
#     print(ex.args[0])
#     print(ex.args) 
finally:
    print('**finally**')
# **finally**
# Traceback (most recent call last):
#   Cell In[32], line 2
#     raise Exception('例外発生')
# Exception: 例外発生
# finally節が実行された後に、例外が再送出されている。

#●except節で新たな例外が発生した場合。 
try:
    raise Exception('例外発生')
except Exception as ex:
    print(ex.args[0])
    raise Exception('例外発生') #←ここを追加
finally:
    print('**finally**')
#例外発生
# **finally**
# Traceback (most recent call last):
#   Cell In[34], line 2
#     raise Exception('例外発生')
# Exception: 例外発生
# During handling of the above exception, another exception occurred:
# Traceback (most recent call last):
#   Cell In[34], line 5
#     raise Exception('例外発生') #←ここを追加
# Exception: 例外発生


#●try節の中で、return,break/countinueが呼び出された場合
def hoge():
    try:
        return 'Hoge'
    finally:
        print('**finally**')
print('start')
print(hoge())
print('end')
# start
# **finally** hoge関数終了(return処理)の前にfinallyが実行される。
# Hoge
# end

#●finally節がreturn命令を持つ場合
def hoge():
    try:
        return 'Hoge'
    finally:
        print('**finally**')
        return 'Hoge finally'
print('start')
print(hoge())
print('end')
# start
# **finally**
# Hoge finally ←　try配下のreturnは実行されていないことに注目
# end

#%% 11.1.3 例外をスロー（発生）させる raise 命令

#後で書く

#●捕捉: sys.exc_info関数 と トレースバック
#例外情報を(例外クラス, 例外クラスのインスタンス, トレースバック)形式タプルで返してくれる

#%% 11.1.4 独自の例外クラス
#↓アプリ独自の例外クラスを作るサンプルコード
#↓アプリ独自の例外基底クラス
class MyAppError(Exception):
    pass
#↓アプリ独自の例外個別クラス
class MyInputError(MyAppError):
    def __init__(self, code, message):
        self.code = code
        self.message = message
if __name__=='__main__':
    try:
        raise MyInputError(501, 'Invlid Input')
    except MyAppError as ex:
        print(ex.args)
        #(501, 'Invlid Input')
        print(dir(ex))
        #'__traceback__', '__weakref__', 'add_note', 'args',
        #'code', 'message', 'with_traceback']
        #例外クラスの初期化メソッドで受け取った情報は、
        #インスタンス変数 args 経由でアクセスできる。
r"""
第1部：【真理】 LBYL (if) vs EAFP (except)
Pythonの公式ドキュメントの用語集には、プログラミングにおける2つの対極的な安全確認のアプローチが定義されています。
⚔️ if の思想 ＝ LBYL（転ばぬ先の杖）
意味: Look Before You Leap（跳ぶ前に見よ）。実行する前に、明示的に前提条件を if で確認するスタイルです
。
現場監督の思考: 「よし、割り算をするぞ！ その前に if divider != 0: で確認だ！ ヨシ、0じゃないな！ 安全確認完了、割り算を実行しろ！」
⚔️ except の思想 ＝ EAFP（許可より謝罪）
意味: Easier to Ask for Forgiveness than Permission（許可を求めるより、後で許しを請う方が簡単）。前提条件が正しいと信じて突撃し、ダメだったら except で事後処理をするというPythonの王道スタイルです
。
現場監督の思考: 「いいからまずは try: で割り算を実行しろ！ え？ 0で割って爆発（ZeroDivisionError）したって？ しょうがない、爆発物処理班（except）を出動させて事後処理（エラーログ出力や代替値の代入）をしろ！」
つまり、if は**「事前確認」、except は「事後対応」**という明確な役割の違いがあります。
第2部：【解剖】 except に隠された「家系図チェック機構」
if と except のもう一つの決定的な違いは、**「条件の判定基準」です。if が値の大小や一致（==）を見るのに対し、except は「飛んできた例外オブジェクトの『家系図（クラスの継承関係）』」**を調べます。
公式ドキュメントには**「except 節内のクラスは、そのクラスや派生クラスのインスタンスである例外とマッチします」**という絶対ルールが定義されています
。
昌敏さんが書かれた見事なコードで、現場監督がどう動いたかを見てみましょう。
try:
    # 爆弾（MyInputError）を投げる！
    raise MyInputError(501, 'Invlid Input')
except MyAppError as ex:
    # ここでキャッチできるのはなぜ？
■ 現場監督のスローモーション
現場監督：「おい！ MyInputError という爆弾が飛んできたぞ！ 爆発物処理班（except）はいるか！」
処理班：「こちら MyAppError 処理班です！」
現場監督：「お前たちにこの爆弾が処理できるのか？ 家系図（継承関係）を確認するぞ！」
現場監督：「MyInputError の親は MyAppError だな！ つまり MyInputError はお前たちの一族（派生クラス）だ！ （裏側で isinstance(飛んできた爆弾, MyAppError) が True になる）
 よし、お前たちなら安全に解体できる、処理を任せた！」
もしここが if 文だったら、「完全に名前が一致しているか（==）」しか見られませんが、except は「オブジェクト指向の継承関係（is-a関係）」を理解した上で、**「指定されたクラスの子供や孫のエラーまで、すべて一網打尽にキャッチしてくれる」**という極めて高度な属性を持っています。
第3部：【実務】 なぜインフラエンジニアは except (EAFP) を多用するのか？
「事前に if でチェックした方が安全なのでは？」と思うかもしれません。しかし、インフラ自動化の実務において、if (LBYL) は時に**致命的なバグ（レースコンディション＝競合状態）**を引き起こします
。
たとえば、ファイルを開いて読み込むスクリプトを考えます。
❌ if を使った事前チェック（危険）
if os.path.exists('config.txt'): # ①まずファイルがあるかチェック
    # ！！もしこの0.001秒の間に、別のプロセスがファイルを消したら？！！
    with open('config.txt') as f: # ②開こうとしてクラッシュ（本番障害）
        pass
⭕ except を使った事後処理（堅牢）
try:
    with open('config.txt') as f: # ①とりあえず開いてみる
        pass
except FileNotFoundError:         # ②ダメだったら処理する
    print("ファイルがありませんでした")
インフラ環境では、ネットワークの切断やファイルの消失が「いつ」起きるか予測不可能です。そのため、「事前に if で全てをチェックする」のは現実的ではなく、**「とりあえず実行（try）し、飛んできた例外（エラーの種類）に応じて except で適切に捌く」**というアーキテクチャが最強の防弾装甲となります。
■ 参謀からのまとめ
if（LBYL）: **「実行前」**に値や状態をチェックするための「ゲート」。
except（EAFP）: **「実行後」**に発生した想定外の事態（例外オブジェクト）をキャッチして復旧するための「セーフティーネット」。
except の真の力: オブジェクト指向の「継承」を理解しており、親クラスを指定しておけば、その子孫の独自エラークラス（今回なら MyInputError）もまとめて処理してくれる

"""























