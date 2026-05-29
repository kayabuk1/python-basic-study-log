# -*- coding: utf-8 -*-
"""
Created on Fri May 29 09:41:11 2026

@author: iot01
"""

#%% 9.1.4 一部処理を他ジェネレータへ委譲　yield from命令
#↓リストから順にﾌｧｲﾙﾊﾟｽを取り出して、読み込みは委譲
def read_files(*files):
    for file in files:
        yield from read_lines(file)
#↓ファイル読み込みを担う サブジェネレーター
def read_lines(path):
    with open(path,'r',encoding='UTF-8') as file:
        for line in file:
            yield line.rstrip('\n')
for line in read_files(
        './chap09/sample1.dat',
        './chap09/sample2.dat',
        './schap09/sample3.dat'):
    print(line)
'''
自力でプログラム実行の流れを書いてみる。
for line in read_files():でgeneratorが生成され、
next()?が押され実行される。
与えらたファイルパス名文字列をタプルとしてまとめてfilesに代入。
filesから一つずつ取り出してfileに代入、
yield from read_lines(file)でもう一つのジェネレータが呼ばれる。
path=fileとして受け取り、 with open()でファイル名をpathとして、
読み取り専用でfileにも紐付けられたファイルを開く。
fileから 1行ずつ取り出し？デフォルトで1行ずつになっている？
lineに代入。
line.rstrip('\n')が分からない。\nを付けるか外している？
その処理をしてread_linesに戻る。
yieldがあるのでfor line...に戻って1行表示される。？
'''

#%% 9.2.5　ジェネレーター式　(式 for 仮引数 in シーケンス型)
#Q.シーケンス型とは？
#A.シーケンス型とは、**「 リスト、 タプル、 文字列、 range など、複数のデータが
#  順番に並んでいて、左から右へ1つずつ取り出せるデータ型」**の総称です
#  for ループの in の後ろに置ける「イテラブル（反復可能オブジェクト）」の代表格
import random
gen = (random.random() for i in range(100))
#(式 for 仮引数 in シーケンス型)（）内がこの形？式に関数が入ったら？genになる？
#無名関数みたいに()内がgenerator型で生成されるのか。
#それで、式がyieldで戻すものになる？
## システムの裏側で自動翻訳されているイメージ
#def 無名のジェネレーター工場():
#    for i in range(100):
#        # 一番左に書いた式（random.random()）が、自動的に
#        # yield の後ろにセットされる！
#        yield random.random()
# そして、その工場を実体化して名札を貼る
#gen = 無名のジェネレーター工場()
#
#for num in gen:
#    print(num)

#↓今での書き方で同じ処理をさせると
import random
def my_gen():
    for i in range(100):
        yield random.random()
gen = my_gen()
for num in gen:
    print(num)
#0.21953327730459304
#0.8356080651080853
#0.836481736880253
#0.09619735595407009
#0.5101548658181305
#0.5473623018620268
#0.47528046060186824以下略

#%% 9.3 関数のモジュール化
# 9.3.1 モジュールの定義
# figure.py に三角形の面積を求めるモジュールを書く。
from figure import get_triangle
#※右上 ・ ・ ・ で実行環境フォルダをfigure.pyと同じにすること。 
#print(figure)
#NameError: name 'figure' is not defined
print(get_triangle)
    #<function get_triangle at 0x000001EECD3B8040>
print(get_triangle(10, 9))
    #45.0

import figure
#print(get_triangle(10, 9))
    #NameError: name 'get_triangle' is not defined
print(figure)
    #<module 'figure' from 'd:\\python\\figure.py'>
print(figure.get_triangle(10, 9))
    #45.0

from figure import * #すべてインポートすればモジュール名を省くこと出来る
print(get_triangle(10, 9))
    #45
    #しかし、組み込み関数かimportしたものか判別出来なくなるので、非推奨

#import * でのインポートを制限する __all__ =[] or def _piyo()

#モジュールに別名を付与する as
import figure as f
print(f.get_triangle(10, 9))

'''
◆C言語の#includeとの違い。
 C言語の #include は 「テキスト（文字列）のコピー＆ペースト（展開）」 
 Pythonの import は「裏側でのファイル実行と、 
 隔離された 『名前空間（オブジェクトの部屋）』の生成」 という、極めて高度で安全なシステム
 --------------------------------------------------------------------------------
第1部：【解剖】 「コピペ」 vs 「隔離された部屋の生成」
■ C言語の #include （テキストの展開） C言語で #include <stdio.h> と
    書くと、コンパイル前の段階（プリプロセッサ）で、 stdio.h というファイルの中に
    書かれているテキストデータがそのままその場所にコピー＆ペーストされます。
    ただの「文字の流し込み」です。
■ Pythonの import （名前空間の生成） 一方、Pythonではテキストのコピペは
    行われません。公式ドキュメントには**「各々のモジュールは、自分のプライベートな
    名前空間を持っていて、 モジュールで定義されている関数はこのテーブルを
    グローバルな名前空間として使います」**と定義されています
    
実行した2つのコードは、この「部屋（名前空間）からどうやって道具を取り出すか」の違いを表しています。
import figure の裏側 
    システムは figure.py を裏で実行し、メモリ上に figure という名前の
    「隔離された部屋（モジュールオブジェクト）」を作ります。 
    そのため、中にある道具を使うには figure.get_triangle(10, 9) 
    のように、**「部屋の名前 . 道具の名前」 **という形でアクセスしなければなりません。
from figure import get_triangle の裏側
     システムは figure.py を裏で実行しますが、部屋ごと持ってくるのではなく、
     **「figure の部屋から get_triangle という道具だけを直接引っ張り出して、
     現在の自分の部屋（グローバル空間）に置く」**という動きをします。
     そのため、get_triangle(10, 9) と直接呼ぶことができますが、
     部屋自体は持ってきていないため print(figure) は NameError になります。
--------------------------------------------------------------------------------
第2部：【解剖】 「名前の衝突」というインフラの大事故を防ぐ壁
C言語の #include の最大の弱点は、単なるコピペであるがゆえに**「名前の衝突（汚染）」**
が起きやすいことです。 もし2つのヘッダーファイルに同じ calculate() という関数が
書かれていて、両方をインクルードしてしまうと、コンパイラが「どっちの calculate だ！」と
パニックになりクラッシュします。
しかしPythonの import figure は、figure という防護壁（カプセル）の中に
道具を閉じ込めておいてくれます。 もし別の math_tool.py にも get_triangle()
 があったとしても、figure.get_triangle() と math_tool.get_triangle()
 として明確に区別できるため、大規模なシステム開発でも名前の衝突が絶対に起きない
 安全なアーキテクチャになっているのです
--------------------------------------------------------------------------------
第3部：【真理】 なぜPythonには「インクルードガード」が無いのか？
C言語を学んだことがある方なら、ヘッダーファイルに必ず書く #ifndef や #define 
といった**「インクルードガード（二重読み込み防止）」**をご存知かと思います。
コピペの重複を防ぐための呪文ですね。
Pythonの import には、これが一切不要です。 
なぜなら、公式ドキュメントに**「実行効率上の理由で、各モジュールはインタープリタの
 1 セッションごとに 1 回だけ import されます」**と明確に記されているからです
システムの裏側では、 sys.modules というキャッシュ管理システムが動いています。 
どれだけ多くのファイルで import figure と何百回書かれたとしても、 
現場監督（システム）は「おっ、 figure 部屋はさっき作って sys.modules 
に登録済みだな！じゃあ新しく作らずに、いまある部屋への案内図（参照）だけを渡しておこう
」と判断します。 これにより、無限ループ（循環インポート）や無駄なメモリ消費、
二重ロードによる事故がシステムレベルで全自動で防止されているのです。
--------------------------------------------------------------------------------
■ 参謀からの総括（アーキテクトの視点）
C言語の #include: コンパイル前の物理的なテキストの合体。
Pythonの import: 実行時における論理的な
    オブジェクト（名前空間）の生成と、安全なキャッシュ管理システム（sys.modules）の連携。
'''

#%% 9.3.3 モジュールの検索先とそれの確認　sys.path
#◆pythonのモジュール検索順
#１．カレントディレクトリ （現在のスクリプトが配置されているフォルダー）
#Q.↑これはどうやって決まっている？確認するの？
#A.実行したスクリプトファイルが存在する場所、またはIDE（Spyderなど）の
#  右上などで指定した「作業ディレクトリ」のこと
#  /home/user/ を最優先の検索パス
#  ''（空の文字列）現在のカレントディレクトリを意味する。
#2．環境変数PYTHONPATH（フォルダー名のリスト）
#Q.↑環境変数とは？どこのフォルダー名のリスト？
#A.Pythonの中の変数ではなく、「OS（WindowsやLinux）自体が持っている
#  システム設定」のこと
#  ユーザー自身が**「標準の場所以外にも、俺が独自に作った
#  オレオレ部品フォルダがあるから、そこも探してくれ！」とOS側に設定して教え込むためのリスト

#3．環境に応じた規定のパス
#Q.↑規定のパスとは具体的にどんなもの？
#A.Pythonがインストールされた大元のフォルダや、pipでインストールした外部パッケージが入る site-packages フォルダのことです
#。 昌敏さんの sys.path 出力結果の後半にある 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib\\site-packages' などがまさにこれに該当します。
import sys
print(sys)
    #<module 'sys' (built-in)>   
print(type(sys))
    #<class 'module'>
print(dir(sys))
'''
['__breakpointhook__', '__displayhook__', '__doc__', '__excepthook__', '__interactivehook__', '__loader__', '__name__', '__package__', '__spec__', '__stderr__', '__stdin__', '__stdout__', '__unraisablehook__', '_base_executable', '_clear_type_cache', '_current_exceptions', '_current_frames', '_debugmallocstats', '_enablelegacywindowsfsencoding', '_framework', '_getframe', '_getquickenedcount', '_git', '_home', '_stdlib_dir', '_vpath', '_xoptions', 'addaudithook', 'api_version', 'argv', 'audit', 'base_exec_prefix', 'base_prefix', 'breakpointhook', 'builtin_module_names', 'byteorder', 'call_tracing', 'copyright', 'displayhook', 'dllhandle', 'dont_write_bytecode', 'exc_info', 'excepthook', 'exception', 'exec_prefix', 'executable', 'exit', 'flags', 'float_info', 'float_repr_style', 'get_asyncgen_hooks', 'get_coroutine_origin_tracking_depth', 'get_int_max_str_digits', 'getallocatedblocks', 'getdefaultencoding', 'getfilesystemencodeerrors', 'getfilesystemencoding', 'getprofile', 'getrecursionlimit', 'getrefcount', 'getsizeof', 'getswitchinterval', 'gettrace', 'getwindowsversion', 'hash_info', 'hexversion', 'implementation', 'int_info', 'intern', 'is_finalizing', 'last_traceback', 'last_type', 'last_value', 'maxsize', 'maxunicode', 'meta_path', 'modules', 'orig_argv', 'path', 'path_hooks', 'path_importer_cache', 'platform', 'platlibdir', 'prefix', 'ps1', 'ps2', 'ps3', 'pycache_prefix', 'set_asyncgen_hooks', 'set_coroutine_origin_tracking_depth', 'set_int_max_str_digits', 'setprofile', 'setrecursionlimit', 'setswitchinterval', 'settrace', 'stderr', 'stdin', 'stdlib_module_names', 'stdout', 'thread_info', 'unraisablehook', 'version', 'version_info', 'warnoptions', 'winver']
'''
print(sys.path)
'''
['C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\python311.zip', 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\DLLs', 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib', 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime', '', 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib\\site-packages', 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib\\site-packages\\win32', 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib\\site-packages\\win32\\lib', 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib\\site-packages\\Pythonwin']
'''
print(type(sys.path))
    #<class 'list'>
print(dir(sys.path))
#print(PYTHONPATH)
    #NameError: name 'PYTHONPATH' is not defined
import os
print(os.environ.get('PYTHONPATH'))
    #None
    #OSの世界の変数なので、Pythonから覗き見るには、import os をした上で
    #os.environ.get('PYTHONPATH') のように、OSに直接問い合わせる
    #関数を使わなければなりません。
print(sys.executable)
#C:\ProgramData\spyder-6\envs\spyder-runtime\python.exe
print(sys.version)
#3.11.10 | packaged by conda-forge | (main, Oct 16 2024, 01:17:14) [MSC v.1941 64 bit (AMD64)]
print(sys.version_info)
#sys.version_info(major=3, minor=11, micro=10, releaselevel='final', serial=0)
sys.exit()


#%%  9.1.4 インポート時の作法












