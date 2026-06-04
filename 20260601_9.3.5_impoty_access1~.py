# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:31:58 2026

@author: iot01
"""

#%%# 9.3.5 パッケージ 名前衝突を避ける複数のモジュールを束ねる仕組み。
#Pythonのアプリは パッケージ＞モジュール＞関数/型,変数の様に構成されることが多い。
#モジュールの実体がファイルなように、パッケージの実体はフォルダ。
#フォルダを入れ子に出来るのと同じく、パッケージも階層構造に出来る。サブパッケージ。

#mypackパッケージ配下のappモジュールをインポート
import mypack.app
mypack.app.app_func1()
'''Cell In[1], line 1
    import maypack.app
ModuleNotFoundError: No module named 'maypack'
重要
インストーラ由来ではないモジュールを使用しようとしているようです。これを行う方法については、
ドキュメントの FAQ をご覧下さい。
conda create -n my-env -c conda-forge spyder-kernels
 scikit-learn が必要？
◆appモジュールファイルの中身
def app_func1() -> None:
    print('mypack/appのapp_func1を実行')
def app_func2() -> None:
    print('mypack/appのapp_func2を実行')
print('【import】mypack/app module')
◆実行結果
  【import】mypack/app module
  mypack/appのapp_func1を実行

Out[2]: "Cell In[1], line 1\n
    import maypack.app\nModuleNotFoundError: 
        No module named 'maypack'
    \n重要\nインストーラ由来ではないモジュールを使用しようとしているようです。
    これを行う方法については、\nドキュメントの FAQ をご覧下さい。
   \nconda create -n my-env -c conda-forge spyder-kernels
   scikit-learn\nが必要？"
'''
import os
print(os.environ.get('PYTHONPATH'))
#D:\python\mypack ←Noneだったのが表示されている。
import sys
print(sys.path)
'''
Python言語の純粋な仕様:
    スクリプトと同じフォルダにあるモジュール/パッケージは、自動的に
    sys.path に追加されるため、そのままインポートできる
Spyder (IDE) の特殊仕様: 
    裏側で動き続けるIPythonコンソールが作業ディレクトリを固定してしまうため、
    右上メニュー等から手動で「ここが作業フォルダだ」と教えてあげる必要がある。
Q.ユーザー環境変数とシステムの環境変数の違いは？
A.① ユーザー環境変数
影響範囲: 今ログインしている「（そのユーザーアカウント）」にだけ影響します。
権限: 一般ユーザー権限で自由に追加・変更・削除が可能です。
用途: 自分専用のオレオレパッケージを PYTHONPATH に
登録したい場合などに使います。
もし別の人が同じPCに別のアカウントでログインしても、その人の環境は一切汚されません。
② システムの環境変数
影響範囲: そのPC（サーバー）を利用する「すべてのユーザーアカウント」、および
「OSのシステム全体（裏で動くサービスプロセスなど）」**に影響します。
権限: 変更するには**「管理者権限（Administrator）」が必要です。
用途: Python本体をインストールしたときに設定される
実行パス（PATH）などは、どのユーザーからもPythonコマンドを起動できるように、
システム環境変数に登録されます。
③プロセス環境変数 ＝ そのソフトが起動している間だけの一時的なルール
（今回のSpyderの裏技の正体）。
'''
#mypack配下のmysubサブパッケージ配下のhogeモジュールをimport
import mypack.mysub.hoge
mypack.mysub.hoge.hoge_func1()
help(mypack)
help(mypack.mysub)
help(mypack.mysub.hoge)
help(mypack.mysub.hoge.hoge_func1)
print(mypack.__init__)
#<method-wrapper>
help(mypack.__init__)
help(type(mypack.__init__))
#'__init__' of module object at 0x000002A8F0AB1760>
#【import】mypack/mysub/hoge module
#mypack/mysub/hogeのhoge_func1を実行
'''
Help on package mypack:
NAME
    mypack - # from mypack import app
PACKAGE CONTENTS
    __main__
    app
    hoge
    lib
    mysub (package)
    util
FILE
    d:\python\mypack\__init__.py

Help on package mypack.mysub in mypack:
NAME
    mypack.mysub
PACKAGE CONTENTS
    hoge
    lib
FILE
    d:\python\mypack\mysub\__init__.py

Help on module mypack.mysub.hoge in mypack.mysub:
NAME
    mypack.mysub.hoge
FUNCTIONS
    func() -> None
    hoge_func1() -> None
    hoge_func2() -> None
FILE
    d:\python\mypack\mysub\hoge.py

mypack/mysub/hogeのhoge_func1を実行
Help on NoneType object:

class NoneType(object)
 |  Methods defined here:
 |  __bool__(self, /)
 |      True if self else False
 |  __repr__(self, /)
 |      Return repr(self). 
 |  ----------------------------------------------------------------------
 |  Static methods defined here:
 |  __new__(*args, **kwargs)
 |      Create and return a new object.  See help(type) for accurate signature.
Help on method-wrapper:

__init__(*args, **kwargs) unbound builtins.module method
    Initialize self. 
    See help(type(self)) for accurate signature.

help(type(mypack.__init__))
Help on class method-wrapper in module builtins:

class method-wrapper(object)
 |  Methods defined here:
 |  
 |  __call__(self, /, *args, **kwargs)
 |      Call self as a function.
 |  
 |  __eq__(self, value, /)
 |      Return self==value.
 |  
 |  __ge__(self, value, /)
 |      Return self>=value.
 |  
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |  
 |  __gt__(self, value, /)
 |      Return self>value.
 |  
 |  __hash__(self, /)
 |      Return hash(self).
 |  
 |  __le__(self, value, /)
 |      Return self<=value.
 |  
 |  __lt__(self, value, /)
 |      Return self<value.
 |  
 |  __ne__(self, value, /)
 |      Return self!=value.
 |  
 |  __reduce__(...)
 |      Helper for pickle.
 |  
 |  __repr__(self, /)
 |      Return repr(self).
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __objclass__
 |  
 |  __self__
 |  
 |  __text_signature__
 Pythonのすべてのオブジェクトは、自身を初期化するための __init__
 という特殊メソッド（C言語で作られた組み込み機能）を持っています
。
つまり、mypack.__init__ と書いたとき、
現場監督はファイルシステムの __init__.py ではなく、**「mypack
 というモジュールオブジェクトをメモリ上で構築するための
 、C言語レベルの初期化機能（メソッド）」**を見つけてきてしまったのです！
 ファイル名とオブジェクトの機能名がたまたま同じ __init__ 
 であったために起きた、高度な錯覚
 '''

from mypack.mysub import hoge
hoge.hoge_func1()
#mypack/mysub/hogeのhoge_func1を実行 短く記述出来る。

#%%パッケージを初期化する __init__.py
import mypack
mypack.app.app_func1()
#これがAttributeErrorになると独習Pythonでは書かれているけれど、
#mypack/appのapp_func1を実行
#Q.と実行出来てしまうのはなぜ？
'''import mypack.app
mypack.app.app_func1()
これを実行した瞬間、Spyderの現場監督は
 「よし、親パッケージ mypack の中に、サブモジュール app の名札をくっつけておこう！」 
 と記憶（キャッシュ）してしまったのです。'''
#mypackパッケージがappモジュールを持つと認識されていない。
#mypack/__init__.pyでfrom mypack import appが
# #でコメントアウトされているからと書いてあったのだけれど。
#Q.__init__.pyとはどんな役割をしているファイルなのだ？
'''
__init__.py の正体 ＝ ディレクトリをパッケージとして認識させ、インポート時に
初期設定（自動インポートなど）を行うための一度だけ実行されるスクリプト。
A.① パッケージとして認識させる「通行手形」の役割「
公式ドキュメント「ファイルを含むディレクトリをパッケージとしてPython に扱わせるには、
ファイル __init__.py が必要です」
単なるWindowsのフォルダを、Pythonの「パッケージ（モジュールを束ねる階層）」として
システムに認識させるためのマーカーです
（※Python 3.3以降の名前空間パッケージという特殊な機能を除く）。
② インポート時に一度だけ走る「初期化スクリプト」の役割
「パッケージがインポートされたとき、この __init__.py ファイルが暗黙的に実行され、
それで定義しているオブジェクトがパッケージ名前空間にある名前に束縛されます」
これが今回の核心です。import mypack と書いた瞬間、
現場監督は真っ先に mypack フォルダの中にある __init__.py を
読み込んで実行します。 もし __init__.py の中に
 from mypack import app 
というコードを書いておけば、ユーザーが import mypack と書くだけで、
自動的に下層の app モジュールもロードされ、mypack.app として使えるようになるのです。

なぜ__init__メソッド、__init__.pyファイル紛らわしいのか？
Pythonの世界では「全てがオブジェクト」です。 「初期化（Initialize）」を行う際、
現場監督（システム）が裏側で呼び出す機能には、対象が何であれ init という
名前が与えられます。
① メモリ上の箱の初期化 ＝ __init__ メソッド クラスをインスタンス化
（実体化）した際、現場監督に「この新しく作った空っぽのオブジェクト（箱）に、
最初のデータ（インスタンス変数）をセットアップしろ！」と命令するための特殊メソッドです
。
② ディスク上のフォルダの初期化 ＝ __init__.py ファイル 単なるWindowsのフォルダを
Pythonの「パッケージ」としてインポートした際、現場監督に「このフォルダをモジュールオブジェクトとして
メモリ上に展開するついでに、最初の設定（サブモジュールの読み込みなど）をセットアップしろ！」
と命令するための特殊スクリプトです
。
つまり、**「扱う対象がメモリ上のクラスか、ディスク上のディレクトリかの違いだけで、
システムに『初期化処理を行え』と指示する役割は完全に同じ」**なのです。
だからこそ、同じ init という名前が冠されています。
'''
r'''◆__init__.pyの役割と実務的初期化処理について
教科書にある「初期化処理」という言葉だけだと少し抽象的でフワッとしていますよね。
実務（特にインフラ自動化で自作パッケージを作る際）において、__init__.py に書く具体的な「初期化処理」とは、
一言で言えば「そのパッケージを使う人（メインの実行スクリプト）の手間を極限まで省き、かつ安全に使わせるための
『裏側の事前セッティング』」のことです。
公式ドキュメントの定義と実務の観点から、__init__.py に実際に書かれる
「4つの代表的な初期化処理」を完全に解剖します。
--------------------------------------------------------------------------------
第1部：【解剖】 具体的に書かれる4つの初期化処理
公式ドキュメントには「__init__.py ではパッケージのための初期化コードを実行したり、
後述の __all__ 変数を設定してもかまいません」と明記されており
、他のモジュールに書けるPythonコードと同じものを自由に記述できます。
具体的には以下の処理を書きます。
① 階層を浅くする「事前インポート（ショートカット作成）」
深い階層にある関数やクラスを、パッケージがインポートされた瞬間に最上位へ引き上げておく処理です。
記述例: from .mysub.hoge import hoge_func1
効果: これを書いておけば、使う側は import mypack と書くだけで、
いきなり mypack.hoge_func1() と短い名前でアクセスできるようになります。
② __all__ リストによる「公開範囲（API）の制限」
パッケージのユーザーが from mypack import * とワイルドカードを使って中のモジュールを一気に
読み込もうとした際の挙動を制御する処理です。
記述例: __all__ = ["app", "hoge"]
効果: パッケージの中に開発途中の隠しモジュール（例：test_module.py）があったとしても、
__all__ に名前が書かれていない限り import * では読み込まれません。
意図しないモジュールが読み込まれてシステムが予期せぬ副作用を起こすのを防ぐ強力な安全装置になります。
③ パッケージ共通の「定数」や「独自の例外（エラー）型」の定義
__init__.py が実行されると、そこで定義されたオブジェクトは「パッケージの名前空間」に束縛されます。
つまり、パッケージ全体で使いたい共通ルールをここに書くことができます。
記述例: __version__ = "1.0.0" MAX_RETRY_COUNT = 3
効果: ユーザーは print(mypack.__version__) のように、パッケージ自身の情報や共通設定値に
直接アクセスできるようになります。
④ ログ設定や環境変数の事前読み込み（インフラ実務向け）
__init__.py の中のコードは、インポート文で「最初にモジュール名が見つかったときにだけ（1度だけ）」実行されます。
記述例: ネットワーク機器に接続する前の「共通のログ設定（出力先のファイル指定など）」を初期化したり、
APIキーなどの環境変数を裏側で読み込んでおく処理を書きます。
効果: パッケージ内のどのモジュールを呼び出しても、必ず事前にこのログ設定や準備が完了している状態を担保できます。
--------------------------------------------------------------------------------
■ まとめ（アーキテクトの視点）
__init__.py は「ただの空ファイル（通行手形）」としても使えますが、
中に「初期化処理」を書くことで、以下のような 「自作パッケージの現場監督（コントローラー）」として機能し始めます。
ルーティング: 長いパスを短く使いやすくしてあげる（ショートカット）。
セキュリティ: __all__ で外に見せたい機能と隠したい機能を分ける。
セットアップ: パッケージ全体で使う共通設定（定数やログ）を1度だけ準備する。
'''
#%%　名前空間パッケージ

#%%　パッケージの実行 __main__.py
#pythonコマンドでパッケージを呼び出した時に実行すべきコードを用意出来る。
#Q.Linuxなどでコマンドで実行したい時ということでしょうか？
#Q.pythonIDEで実行したときと処理は同じ？？
#Q.__main__.pyif __name__=='__main__':判定のパッケージ版とは？
#どういう意味汗
'''
LinuxのターミナルやWindowsのコマンドプロンプトで、パッケージ（フォルダ）自体を
「1つのプログラム」として起動したい時に使います！

大規模なプログラム（例えば、複数のモジュールが入った mypack フォルダ）を
丸ごと実行したい場面があります。
その際、コマンドラインから以下のように実行することができます。
python -m mypack （モジュールとして実行）
python mypack/ （ディレクトリを直接実行）
この時、現場監督（Python）はこう考えます。 
現場監督「おっ、今回はファイルじゃなくて、mypack というフォルダ全体を
直接実行しろと命令されたぞ！ ……でも、フォルダの中には
 app.py や hoge.py などファイルがたくさんある。
 一体どのファイルから実行を開始すればいいんだ！？」
この迷いを解決し、**「フォルダを実行されたら、真っ先にこのファイルを実行しろ！」
というエントリーポイント（玄関口）**となるのが、__main__.py なのです。

if __name__ == "__main__":
    print("このファイルが直接実行された時だけ動くよ！")
これは、現場監督に対する**「他のファイルから import された時は何もしないが、
このファイルが直接メインスクリプトとして実行された時だけ、このブロックを動かせ！」**
という判定処理でした
。
これを**「パッケージ（フォルダ）という巨大な単位」に拡張した物理的なファイル**が
 __main__.py なのです！
■ 単一ファイルの場合
部品として使う時: 他のコードから import module される。
直接実行する時: if __name__ == "__main__": の中身が動く。
■ パッケージ（フォルダ）の場合
部品として使う時: 他のコードから import mypack される。➔ __init__.py が動く！
直接実行する時: コマンドで python -m mypack と実行される。
➔ __main__.py が動く！
つまり、単一のファイルならファイルの中に if 文を書けば済みますが、
フォルダには直接コードを書き込めません。そこで、**「このパッケージが直接実行された時
専用の処理を、独立したファイル（__main__.py）として作ってフォルダの中に置いておけ！」**
というアーキテクチャになったのです。
'''

#%%# 9.4 非同期処理
#9.4.1 コルーチンの基本
#サブルーチン関数、 ジェネレーターとはどう違うの？
'''
関数の「一直線の実行（サブルーチン）」、データの「遅延評価（ジェネレータ）」、
そして待ち時間の「並行処理（コルーチン）」。
「サブルーチン」「ジェネレータ」「コルーチン」、この3つはどれも「関数」の親戚ですが、
**「現場監督（システム）が実行の主導権（コントロール）をどう扱うか」**という
アーキテクチャが根本的に異なります。
1.サブルーチン（通常の関数） ＝ 「直列・完全実行」 現場監督「この部屋（関数）
  に入ったら、上から下まで一気に最後まで終わらせるまで絶対に出ないぞ！」
2.ジェネレータ ＝ 「データの一時停止と再開」 現場監督「この部屋でデータを作ったら、
  **一旦作業を止めて（yield）**外の呼び出し元にデータを渡すぞ
  ！『次（next）！』と呼ばれたら、さっき止まった場所から再開する！」
3.コルーチン ＝ 「待ち時間の有効活用（非同期）」 
  現場監督「この部屋の作業中に『ネットワークの通信待ち（await）』が発生したな！
  待っている時間がもったいないから、この部屋の作業は一旦保留して、
  別の部屋（他のコルーチン）の作業を進めておくぞ！ 通信が終わったらまた戻ってくる！」

第2部：【解剖】 コルーチンとサブルーチンの違い
公式ドキュメントの用語集には、アーキテクチャの真理としてこう記されています。
「コルーチンはサブルーチンのより一般的な形式です。サブルーチンには決められた地点から入り、
別の決められた地点から出ます。
コルーチンには多くの様々な地点から入る、出る、再開することができます。」
■ サブルーチン（ def func(): ）の限界 通常の関数は、
呼び出されると「一番上」から入り、return に到達する「一番下」から出ます
。 もし関数の中で「ルーターからの応答を10秒待つ（time.sleep や通信処理）」
というコードがあった場合、現場監督はその10秒間、完全にフリーズして何もできなくなります
（ブロッキング）。
■ コルーチン（ async def func(): ）の革命
コルーチンは、関数の中に await（待機）という特別なチェックポイント
（一時停止ボタン）を持っています。現場監督が await に到達すると
、「よし、ここで通信待ちが発生するから、一旦外に出て他の仕事をしてこよう！」と
一時停止して抜け出し、裏で別の仕事を進め、通信が返ってきたら
先ほどの場所からシームレスに再開することができます
。
「ジェネレータ関数はコルーチンにとてもよく似ています。
ジェネレータ関数は何度も生成し、1つ以上のエントリポイントを持ち、
その実行は一時停止されます。ジェネレータ関数は yield した後で
実行の継続を制御できないことが唯一の違いです。」
この2つの決定的な違いは**「何のために一時停止するのか（目的）」**です。
ジェネレータ（yield）の目的： 大量のデータ（100GBのログなど）をメモリに
一気に載せないために、**「データを1個ずつ生成・返却するため」**に一時停止します
。主導権は常に呼び出し元（next() を呼ぶ側）にあります
。
コルーチン（await）の目的： I/Oバウンド（通信やファイル読み書きの待ち時間）
による無駄をなくし、**「CPUの実行権（主導権）を他の並行タスクに譲るため」**
に一時停止します。これを管理するのが「イベントループ（Event Loop）」
と呼ばれる高度なスケジューラーです
。
※Python 3.5以降、この2つを文法的に明確に分けるために、コルーチン専用の
 async def と await というキーワードが導入されました
。
'''
import asyncio
async def heavy_process(name, sec):
    print(F'start{name}')
    await asyncio.sleep(sec)
    print(f'end {name}')
    return f'{name}/{sec}'
# print(heavy_process('hoge', 5))

import time
start = time.time()
loop = asyncio.get_event_loop()
# result = loop.run_until_complete(
#     heavy_process('hoge', 5)
#     )
# ⭕ Spyder環境(IPython)なら、直接 await で着火できる！
r'''インフラ自動化のスクリプトを書く際、ネット上のサンプルコードではよく 
loop.run_until_complete() や asyncio.run() で実行するように書かれています。
0しかしSpyder（IPython）という環境は、すでに裏側でイベントループ（大元締め）が走り続けている特殊な部屋です。
すでに走っている大元締めに対して「もう一人大元締めを呼んでこい（get_event_loop）」と命令したことで
バッティングし、 RuntimeError: This event loop is already running でシステムがクラッシュしたわけです。
そこで、大元締めを新たに呼ぶのではなく「すでに回っている大元締めに対して、
トップレベルから直接 await で着火させる」というSpyder専用の正しい書き方が必要になります。
※Jupyter Notebookでも同じ現象が起きる。
※もしSpyderのコンソール上ではなく、コマンドプロンプトなどから python app.py として
「独立したプログラム」として実行する場合は、逆にトップレベルで await は使えないため、
一番外側だけ result = asyncio.run(heavy_process('hoge', 5)) を使う必要があります。
Q.この トップレベル というのは何を指している？'''
result = await heavy_process('hoge', 5)
end = time.time()
print(result)
print(f'Process Time: {end - start}')

# starthoge
# end hoge
# hoge/5
# Process Time: 5.001134157180786

r'''
 Cell In[5], line 12
    result = loop.run_until_complete(
  File C:\ProgramData\spyder-6\envs\spyder-runtime\Lib\asyncio\base_events.py:630 in run_until_complete
    self._check_running()
  File C:\ProgramData\spyder-6\envs\spyder-runtime\Lib\asyncio\base_events.py:589 in _check_running
    raise RuntimeError('This event loop is already running')
RuntimeError: This event loop is already running
'''
# 上のブロックだけ実行では帰ってきたオブジェクトをprintで表示しただけとのこと。
#async def で作られた関数（コルーチン）は、普通に呼び出しても「作業指示書（コルーチンオブジェクト）」
#がポロッと作られるだけで、中身は1ミリも動かないという非同期の動作になっている。
r'''
Q.そもそも async と await の文法的役割と定義がよく理解できていないと感じる。解説して欲しい。
Q.asyncio.get_event_loop() loop.run_until_complete()
  ↑この2つの命令がどんな命令になるのか具体的に詳しく解説して欲しい。
'''
# <coroutine object heavy_process at 0x000002A8F09EDC40>
# C:\Users\iot01\AppData\Local\Temp\ipykernel_3424
# \3917610962.py
# :7: RuntimeWarning: coroutine 'heavy_process
# ' was never awaited
# print(heavy_process('hoge', 5))
#↑asyncで作った関数をそのまま print してしまうと、
#システムから「おい！指示書を作らされたのに実行（await）されてないぞ！」と RuntimeWarning を食らいます。
# RuntimeWarning: Enable tracemalloc to get the object
# allocation
# traceback
# '''で囲ってエラーが出た。↓原因。
# \Users の\U を、パーサーが「Unicode文字を作る命令」だと勘違いして自爆したのです。
# Ctrl + 1 を押せば、一括で #
# 戦術2：「Raw（生の）文字列」にする どうしても ''' を使って残しておきたい場合は、
# 文字列の先頭に r を付けます。
r'''
<coroutine object heavy_process at 0x000002A8F09EDC40>
C:\Users\iot01\AppData\Local\Temp\ipykernel_3424\3917610962.py
Q.coroutine object とは具体的にどんな風に定義されていますか？
'''
'''◆イベントループとOSのディスパッチャの違い
イベントループはPython（1つのスレッド）の中だけで動く、専用の私設ディスパッチャである。
●OSのディスパッチャとイベントループの決定的な違い。
① OSのディスパッチャ（カーネルレベル）
権限: 絶対的（神）。CPUの割り当てを管理します。
動き方（プリエンプティブ）: 
    OSのディスパッチャは、各プログラム（スレッド）に対して「はい、君の持ち時間はここまで！次！」と、
    **強制的にCPUの主導権を剥奪（コンテキストスイッチ）**します。プログラムの都合はお構いなしです。
② Pythonのイベントループ（アプリケーションレベル）
権限: OSから与えられた「1つのスレッド（1つのCPU枠）」の中だけで仕切る「大元締め（私設ディスパッチャ）」です。
動き方（ノンプリエンプティブ / 協調的マルチタスク）: 
    イベントループは強制的に主導権を奪えません。その代わり、コルーチン（作業員）たちが
    「今は通信待ちで暇だから、CPUの主導権を返すよ（await）」と自主的に宣言することで、
    次のコルーチンに作業を割り振ります。※awaitはwaitと違い他動詞かつフォーマルな表現。
    
第2部：【解剖】 どう連携しているのか？（スローモーション）
では、OSとPythonのイベントループがどう連携して、あの「圧倒的な並行処理」を実現しているのか？

OSのディスパッチャ「よし、Pythonのプロセス（メインスレッド）にCPUの使用権を与えるぞ！ 走れ！」
Pythonのイベントループ「OSからCPUの許可が来たぞ！ よし、コルーチンA（ルーター1へのSSH接続）、お前動け！」
コルーチンA「ルータ1に接続要求を出しました！応答が来るまで暇なのでイベントループにCPU主導権を返します（await）」
Pythonのイベントループ「よし、主導権を受け取ったぞ！OSからもらった俺たちのCPU持ち時間はまだ残っているから、
    すかさずコルーチンB（ルーター2へのSSH）を動かすぞ！」
コルーチンB「ルーター2に接続要求を出しました！ 主導権を返します（await）！」
    (これを100台分繰り返す)
OSのディスパッチャ「おっと、Pythonの持ち時間が終わったな。一旦CPUを没収して、
    別のアプリ（ブラウザなど）にCPUを回すぞ。……はい、またPythonの番だ！」
Pythonのイベントループ「OSからCPUが戻ってきたぞ！ おっ、さっきのルーター1からデータが返ってきている
    （OSからのI/O完了通知）！ よしコルーチンA、再開しろ！」
--------------------------------------------------------------------------------
第3部：【アーキテクトの視点】 なぜOSに任せずに自分でディスパッチするのか？
「わざわざPythonの中でイベントループを作らなくても、全部OSのディスパッチャに任せて、
100個のOSスレッドを作ればいいのでは？」
実は、一昔前（マルチスレッド全盛期）はそうしていました。しかし、OSのディスパッチャは非常に重厚なため、
スレッドを1万個も作ると、OSが「誰にCPUを渡すか」の管理（コンテキストスイッチ）だけでCPUを使い果たしてしまい、
システムがパンクします（これを C10K問題 と呼びます）。
そこで生まれたのが、asyncio（イベントループ）のアーキテクチャです。
OSから見れば「Pythonという1つのスレッド」がずっと動いているだけなので、OSの負担は最小限です。
その「1つのスレッドの中で与えられたCPU時間」をPythonのイベントループがミリ秒単位で無駄なく
1万個のコルーチンに細かく割り振る（await でキャッチボールする）ことで、
「OSのオーバーヘッド限界を超えた超・軽量な並行処理」を実現しているのです！
--------------------------------------------------------------------------------
■ 参謀からのまとめ
OSのディスパッチャ ＝ 会社（OS）の社長。各部署（プロセス/スレッド）に予算（CPU時間）を強制的に割り当てる。
イベントループ ＝ Python部署の「現場監督」。社長（OS）からもらった限られた予算（CPU時間）の中で、
    部下（コルーチン）がサボっている時間（I/O待ち）を見つけては、別の部下に仕事を回し、
    部署全体の生産性を極限まで高める。
'''







