# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 13:44:57 2026

@author: iot01
"""

#%% 9.4.1-複数の処理を平行に実行するから
import time
import asyncio
async def heavy_process(name, sec):
    print(F'start{name}')
    await asyncio.sleep(sec)
    print(f'end {name}')
    return f'{name}/{sec}'
start = time.time()
loop = asyncio.get_event_loop()
result = await asyncio.gather(
#Q.ayncio.gatherとはどんな関数か？
#A.複数の作業指示書（コルーチン）を現場監督に一括で渡し、並行して走らせて、
#  全部が終わるのを待ち、その結果をリストとしてまとめる関数。
#直列処理の場合: 通常、await heavy_process('hoge', 2) と書くと、それが完全に終わるまで次の行には進めません。
#gather の場合: 現場監督に対して「おい監督！ここに『hoge』『bar』『piyo』『spam』という4つの作業指示書がある。
#    これらを全部並行して進めてくれ！全部終わったら結果をまとめて報告しろ！」
#    と一括発注（スケジューリング）する専用の命令です。
        heavy_process('hoge', 2),
        heavy_process('bar', 5),
        heavy_process('piyo', 1),
        heavy_process('spam', 3)
    )
end = time.time()
print(result)
print(f'Process Time: {end - start}')
r'''
starthoge
startbar
startpiyo
startspam
end piyo
end hoge
end spam
end bar
['hoge/2', 'bar/5', 'piyo/1', 'spam/3']
Process Time: 5.019075393676758

Q.結果について詳しく解説してほしい。
A.
① なぜ start は上から順番に出たのか？
starthoge
startbar
startpiyo
startspam
現場監督は gather で渡されたリストの順番（上から）にコルーチンを起動します。
しかし、それぞれの heavy_process の中で await asyncio.sleep(sec) に到達した瞬間、
作業員は「5秒の通信待ちに入ります！主導権を返します！」と監督にパスを出します。
監督はすかさず次の作業員を起動するため「全員の start だけが一瞬で順番に呼ばれ、
全員がほぼ同時に await（待ち状態）に入った」状態になります。
② なぜ end の順番はバラバラなのか？
end piyo
end hoge
end spam
end bar
ここが非同期処理の真骨頂です！全員が待ち状態に入った後
「待ち時間（sec）が短い順に作業が完了して復帰（レジューム）したから」です。
piyo (1秒) ➔ 1番目に完了して復帰。
hoge (2秒) ➔ 2番目に完了して復帰。
spam (3秒) ➔ 3番目に完了して復帰。
bar (5秒) ➔ 最後に完了して復帰。 
現場監督は作業が終わった（応答が返ってきた）作業員から順番に主導権を返し、
残りの処理（print(end...)）を終わらせています。
③ なぜリストの順番は「元の発注通り」なのか？
['hoge/2', 'bar/5', 'piyo/1', 'spam/3']
終わった順番はバラバラ（piyoが最初）だったにもかかわらず、
最終的な result のリストは、一番最初に gather に渡した引数の順番通りに綺麗に整列しています。
これは asyncio.gather() の非常に有能な仕様です。「裏側の処理がどんな順番で終わろうとも、
プログラマが後でデータを扱いやすいように、渡された指示書の順番通りに結果を並べ直して返してくれる」という機能を持っています。
④ なぜ処理時間が「約5秒」なのか？（最大の真理）
Process Time: 5.019075393676758
もしこれをC言語のような直列処理（サブルーチン）で実行した場合、 2秒 + 5秒 + 1秒 + 3秒 = 「合計11秒」 かかるはずです。
しかし、コルーチンによる並行処理では、全員が「手待ち時間（I/O待ち）」に主導権を譲り合って同時に待機したため、
全体の処理時間は「最も待ち時間が長かったタスク（bar の 5秒）にほぼ一致する」ということが起きています。
'''

#%% 9.4.2 非awaitableな処理をawait式に渡す run_in_executorメソッド
import asyncio
import requests
import time
async def get_content(url):
    print(f'start {url}')
    res = requests.request('get', url)
    print(f'end {url}')
    return res.text[:100]
start = time.time()
loop = asyncio.get_event_loop()
result = await asyncio.gather(
    get_content('https://codezine.jp'),
    get_content('https://wings.msn.to'),
    get_content('https://www.web-deli.com/')
    )
end = time.time()
print(result)
print(f'Process Time: {end - start}')
r'''
▲↓は非同期処理は実行されていない。
C:\ProgramData\spyder-6\envs\spyder-runtime\Lib\site-packages\urllib3\util\connection.py:7: RuntimeWarning: coroutine 'heavy_process' was never awaited
  from .timeout import _DEFAULT_TIMEOUT, _TYPE_TIMEOUT
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
❌ 前回のログ（罠にハマった直列処理）
start https://codezine.jp
end https://codezine.jp  (⬅️ 次のstartの前に必ずendが来ている)
start https://wings.msn.to
end https://wings.msn.to
start https://www.web-deli.com/
end https://www.web-deli.com/
['  \n    \n\n\n\n<!DOCTYPE html>\n  <!--[if lte IE 8]> 
        <html class="no-js lt-ie8" lang="ja">
        <![end', '<!DOCTYPE html>\n<html lang="ja">
           \n<head>\n<meta charset="UTF-8" />\n<title>
           サーバーサイド技術の学び舎 - WINGS</title', '\r\n<?xml version="1.0" encoding="utf-8"?>\r\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional/']
Process Time: 0.5743927955627441

【メモ】現場監督はなぜ「直列処理」に戻ってしまったのか？
このコードは、「9.4.2 非awaitableな処理をawait式に渡す」というタイトルの通り
「やってはいけない失敗例（Before）」を示すサンプルコードです。
■ 【事象】ログが証明する「並行処理の失敗」 実行結果のログを見ると、
前回の asyncio.sleep() の時のように start が一気に4つ出ず、以下のように1つずつ順番に終わっていることがわかります。
start https://codezine.jp
end https://codezine.jp
start https://wings.msn.to
end https://wings.msn.to
asyncio.gather で束ねて一気に着火したはずなのに、なぜ同時に進まなかったのでしょうか？
■ 【原因】 requests という「報告なしで寝る作業員」
原因は、requests.request('get', url) という処理にあります。
実はPythonの requests ライブラリ（および time.sleep など）は、
非同期処理（イベントループ）の世界を知らない古い道具なのです（これを「非awaitable」と呼びます）。
前回の await asyncio.sleep(sec) の動き：
    作業員「現場監督！今から5秒待ちます！その間、私のCPU主導権をお返しします（await）！」
    現場監督「よし、その隙に別のサイトの処理を進めるぞ！」（➔ 並行処理成功）
今回の requests.get(url) の動き：
    作業員「通信開始します！ （……通信中……）」
    現場監督「おい、待ち時間に入ったなら主導権を返せ（awaitしろ）！」
    作業員「（……通信中……何も聞こえない……）」
    現場監督「こいつ、主導権を持ったままフリーズ（ブロック）しやがった！
    こいつが通信を終えるまで、俺（イベントループ全体）も止まるしかないじゃないか！！」
このように、非同期の部屋（async def）の中で、1つでも「awaitできない重い処理（ブロッキング処理）」を実行してしまうと、
現場監督自身が巻き添えを食らってフリーズし、結果的にただの順番待ち（直列処理）に成り下がってしまうのです。
■ 【解決への道筋】 run_in_executor とは何か？
では、requests のような古い便利な道具を使って並行処理をしたい場合はどうすればいいのか？
ここで登場するのが次項の run_in_executor（別動隊の派遣） です。
現場監督「こいつ（requests）は俺の言うことを聞かずにフリーズする危険な奴だ。だから俺が直接面倒を見るのはやめて、
OSのディスパッチャに頼んで『別のスレッド（別動隊）』を作ってもらい、そこで隔離して作業させよう！
俺は結果だけを await で待つ！」という仕組みです。
※なお、ログの先頭に出ている RuntimeWarning: coroutine 'heavy_process' was never awaited は、
以前のセルで実行し忘れたコルーチンの残骸がガベージコレクトされた時に出た「過去の亡霊」なので気にしなくて大丈夫です！
'''
#↓requestsをコルーチン化に変えたコード run_in_executor を使った正しい形（並行処理が成功する形）
import asyncio
import requests
import time
async def get_content(url):
    print(f'start {url}')
    res = await loop.run_in_executor(None, requests.get, url)
    # 【ここが核心！】
    # loop.run_in_executor(None, 関数, 引数)
    # 第一引数の None は「標準のスレッドプール（別動隊）を使え」という意味。
    # 現場監督は requests.get 関数を別スレッドに丸投げし、結果を await で待つ！
    print(f'end {url}')
    return res.text[:100]
# 着火フェーズ（前回と同じ）
start = time.time()
loop = asyncio.get_event_loop()
result = await asyncio.gather(
    get_content('https://codezine.jp'),
    get_content('https://wings.msn.to'),
    get_content('https://www.web-deli.com/')
    )
end = time.time()
print(result)
print(f'Process Time: {end - start}')
r'''
⭕ 今回のログ（別動隊による並行処理成功！）
start https://codezine.jp
start https://wings.msn.to
start https://www.web-deli.com/
(⬇️ その後、別々のタイミングで終了)
end https://www.web-deli.com/
end https://wings.msn.to
end https://codezine.jp
['  \n    \n\n\n\n<!DOCTYPE html>\n  <!--[if lte IE 8]>         <html class="no-js lt-ie8" lang="ja"> <![end', '<!DOCTYPE html>\n<html lang="ja">\n<head>\n<meta charset="UTF-8" />\n<title>サーバーサイド技術の学び舎 - WINGS</title', '\r\n<?xml version="1.0" encoding="utf-8"?>\r\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional/']
Process Time: 1.0843505859375
requests が通信中であってもイベントループはブロックされず、3つのサイトへのリクエストが「同時に」スタートし、
処理時間が急激に短縮される。
ネットワーク機器を操作する Netmiko や NAPALM などの多くのツールは、裏側で通常の同期通信を行っています。
それらを並行処理して100台のルーターを同時に設定変更したい場合、
古い同期ツールを run_in_executor で別スレッドに隔離し、asyncio.gather で束ねて一斉に制御する、という設計パターンになる。
Q.awaitに対応しているかどうかはどう調べれば良い？
'''

#%% 9.4.3 タスクの作成と実行 awaitableｵﾌﾞｼﾞｪｸﾄTask creat_task関数
#↓ただ await を並べただけでは並行処理にならない。
import time
import asyncio
async def heavy_process(name, sec):
    print(F'start{name}')
    await asyncio.sleep(sec)
    print(f'end {name}')
    return f'{name}/{sec}'
async def main():
    print(await heavy_process('hoge', 2))
    print(await heavy_process('bar', 5))
    print(await heavy_process('piyo', 1))
start = time.time()
loop = asyncio.get_event_loop()
await main()
end = time.time()
print(f'Process Time: {end - start}')
r'''
starthoge
end hoge
hoge/2
startbar
end bar
bar/5
startpiyo
end piyo
piyo/1
Process Time: 8.028165102005005
「ただ await を並べただけでは並行処理にならない
■ 現場監督のスローモーション
現場監督「よし、まずは1行目の await heavy_process('hoge', 2) だな！ hogeの作業指示書を作って着火するぞ！」
hoge作業員「通信開始！ 2秒の待ちに入ったので主導権を返します（await asyncio.sleep(2)）！」
現場監督「主導権を受け取ったぞ！ その間に別の仕事を……って、おい！
    まだ bar や piyo の作業指示は俺のところに届いてないぞ！（コードが下の行に進んでいない）
    他にやる仕事が登録されていないから、hoge が終わるまでぼーっと待つしかないじゃないか！」
(2秒後) 現場監督「よし、hogeが終わった。じゃあやっと次の行に進めるな。次は await heavy_process('bar', 5) か、よし着火！」
(これを繰り返す)
【真理】 await は「待ち時間に入ったら他の仕事を進める」という魔法のキーワードですが、
    それはあくまで 「イベントループ（大元締め）のスケジュール帳に『他の仕事』がすでに登録されている場合」のみ 機能します。
    今回の書き方では、hogeが終わるまで次の行（barの着火）に進めないため、見事な直列処理になってしまったのです。
'''
#↓def main内をTaskに書き換え
import time
import asyncio
async def heavy_process(name, sec):
    print(F'start{name}')
    await asyncio.sleep(sec)
    print(f'end {name}')
    return f'{name}/{sec}'
async def main():
    t1 = asyncio.create_task(heavy_process('hoge', 2))
    t2 = asyncio.create_task(heavy_process('bar', 5))
    t3 = asyncio.create_task(heavy_process('piyo', 1))
    print(await t1)
    print(await t2)
    print(await t3)
start = time.time()
loop = asyncio.get_event_loop()
await main()
end = time.time()
print(f'Process Time: {end - start}')
r'''main前からawait外すとエラー
main()
end = time.time()
print(f'Process Time: {end - start}')
Process Time: 0.0
C:\Users\iot01\AppData\Local\Temp\ipykernel_1292\2598163482.py:17: RuntimeWarning: coroutine 'main' was never awaited
  main()
RuntimeWarning: Enable tracemalloc to get the object allocation traceback

↓await main()で実行
starthoge
startbar
startpiyo
end piyo
end hoge
hoge/2
end bar
bar/5
piyo/1
Process Time: 4.9989964962005615

 asyncio.gather() は、この「作業指示書の提出と着火」をひとまとめにして一斉にイベントループに登録する機能だったため、
 綺麗に並行処理されました。
そして、今回の単元のタイトルにある Task（create_task 関数）こそが、より細かく並行処理をコントロールするための主役となります。

第1部：【解剖】 main() から await を外すとなぜエラー（0秒）になるのか？
RuntimeWarning: coroutine 'main' was never awaited Process Time: 0.0
このエラーと0秒という結果は、今朝学習した**「コルーチン関数（async def）の絶対的な真理」**をシステムが証明してくれたものです。
現場監督のスローモーション
ユーザーがmain() と書いた！
システム：「おっ、main は async def で作られた関数だな。じゃあ中身は1ミリも実行せずに、
『mainという未実行の作業指示書（coroutine object）』だけを発行してメモリ上に置いておこう」
システム：「次は end = time.time() だな。はい終了！……っておい！！ さっき作った main の作業指示書、
現場監督（イベントループ）に渡してない（await してない）から、放置されたままプログラムが終わっちゃったぞ！！」
これが Process Time: 0.0 秒の理由であり、システムが coroutine 'main' was never awaited
（『main』コルーチンが一度も await されずに捨てられたぞ！）と警告を出した本当の理由です。
await main() と書くことで初めて、現場監督がその指示書を受け取って中に入り、実際の仕事（タスクの作成など）を始めてくれるのです。
第2部：【真理】 create_task の正体と gather との違い
前回の asyncio.gather() が「複数の指示書をドサッと一括で発注する」機能だったのに対し、
今回の asyncio.create_task() は「個別発注と即時着火」を行うインフラのコア機能です。
未実行の指示書： heavy_process('hoge', 2) （ただの紙切れ。まだ現場監督は知らない）
タスク化（即時着火）： asyncio.create_task(heavy_process('hoge', 2)) （現場監督に紙切れを手渡し
「今すぐお前のスケジュール表（ループ）に組み込んで、裏で作業を開始しといてくれ！」 と命じる絶対コマンド）
つまり、t1 = asyncio.create_task(...) と書いた瞬間に、
裏側ではすでに heavy_process の労働がフライングでスタートしているのです。
第3部：【アーキテクチャ】 実行結果の完全解剖（スローモーション）
このコードの出力結果には、非同期処理の「美しいパス回し」がすべて表現されています。順番に追ってみましょう。
① 着火フェーズ（startが連続で出る理由）
starthoge
startbar
startpiyo
現場監督が main の中に入り、上から順に t1, t2, t3 を create_task（スケジュール登録）しました。
登録された瞬間、それぞれのタスクが走り出し、全員が一瞬で start を叫んでから 
await asyncio.sleep(sec)（待ち状態）に入り、主導権を現場監督に返します。
② 完了待ちフェーズ（endの順番がバラバラな理由）
end piyo   (1秒後)
end hoge   (2秒後)
現場監督が次の指示を待っている間に、裏でスリープが終わったタスクから順番に復帰してきます。
待ち時間の短い piyo(1秒) ➔ hoge(2秒) の順で作業を終えて end を叫びます。
③ 結果受け取りフェーズ（なぜ t1 の結果が先に出るのか？）
hoge/2     (t1の出力)
end bar    (5秒後)
bar/5      (t2の出力)
piyo/1     (t3の出力)
ここが最大の真理です！ main の後半で、print(await t1) と書いてあります。
await t1 の意味：「おい現場監督！ t1 の作業が完全に終わって結果（return値）が出るまで、ここで待機しろ！」
この時点で経過時間は「ほぼ0秒」です。現場監督はここで t1 が終わるまで2秒間待機します。
2秒後、t1 が終わって hoge/2 を返してきたので、それを print します。
次に print(await t2) が呼ばれます。
t2（bar）の作業時間は 5秒 です。現在すでに2秒経過しているので、現場監督は残り3秒間ここで待機します。
5秒経過した時点で t2 が終わって end bar と叫び、bar/5 の結果を返してくるので、それを print します。
最後に print(await t3) が呼ばれます。
t3（piyo）の作業時間は 1秒 です。しかし、今はすでに開始から5秒経過しています。
つまり、t3 の作業はとっくの昔に終わって、結果を持ったまま待機していた状態です。
そのため、現場監督は1ミリ秒も待つことなく、即座に t3 の結果 piyo/1 を受け取って print します。

--------------------------------------------------------------------------------
■ 参謀からのまとめ（実務での絶大な価値）
asyncio.gather() ➔ 「設定変更するルーター100台のリストがあるから、全部並行でやって、
全員終わったら結果をまとめて持ってこい！」という大雑把な一括処理に便利。
asyncio.create_task() ➔ 「ルーターAの設定を裏で走らせておきつつ、
その間にルーターBのログを解析して……ルーターAが終わったら結果をここで受け取って……」というような
「複雑で自由なワークフロー（個別のタスク管理）」**を組み立てるための最強の部品。
Task を使えば、途中で「やっぱりこの通信はキャンセルだ！（t1.cancel()）」といった高度な操作も可能になります。 
'''



























