# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:48:51 2026

@author: iot01
"""
#%% 7.4.3 JSONデータを取得する
import requests
res = requests.get('http://wings.msn.to/tmp/books.json')
bs = res.json()
print(bs)
print(bs['books'][0]['title'])
    #KeyError: 'book'
    #%runfile 'D:/python/20260519_7.4.3_http_json~.py' --wdir
    #独習Java 新版
print(requests.get)
print(requests)
    #<function get at 0x0000021E7F439300>
    #<module 'requests' from 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib\\site-packages\\requests\\__init__.py'>
print(res.text)
print(res.json)
print(type(res))
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










