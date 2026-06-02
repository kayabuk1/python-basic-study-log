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

Q.そもそもawaitについて良くわかっていないと感じる。
  正確な文法用語と分かりやすい比喩両方用いて、詳しく解説してください。
Q.event loopはpythonシステム内のディスパッチみたいなもの？
  でもCPUの使用権をOSに貰ってプログラムを実行しているのだよね？
  OSのディスパッチャとはどう違う？そしてどの様に連携している？
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
start https://codezine.jp
end https://codezine.jp
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
'''
#↓requestsをコルーチン化に変えたコード
import asyncio
import requests
import time
async def get_content(url):
    print(f'start {url}')
    res = await loop.run_in_executor(None, requests.get, url)
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
start https://codezine.jp
start https://wings.msn.to
start https://www.web-deli.com/
end https://www.web-deli.com/
end https://wings.msn.to
end https://codezine.jp
['  \n    \n\n\n\n<!DOCTYPE html>\n  <!--[if lte IE 8]>         <html class="no-js lt-ie8" lang="ja"> <![end', '<!DOCTYPE html>\n<html lang="ja">\n<head>\n<meta charset="UTF-8" />\n<title>サーバーサイド技術の学び舎 - WINGS</title', '\r\n<?xml version="1.0" encoding="utf-8"?>\r\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional/']
Process Time: 1.0843505859375
'''

#%% 9.4.3 タスクの作成と実行 awaitableｵﾌﾞｼﾞｪｸﾄTask creat_task関数
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
'''



























