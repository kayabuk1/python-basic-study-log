# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:42:32 2026

@author: iot01
"""

#%%## chapter 8 ユーザー定義関数
## 8.1 ユーザー定義関数の基本
# 8.1.1 ユーザー定義関数の基本構文 def命令

#get_triangle関数を定義
def get_triangle(base,height):
    return base*height/2
#get_triangle関数を呼び出す
area = get_triangle(8, 10)
print(F'三角形の面積は{area:.5}です。')
    #三角形の面積は40.0です。
print(type(area))
print(get_triangle)
print(type(get_triangle))
print(dir(type(get_triangle)))
print(dir(get_triangle))
#<class 'float'>
#<function get_triangle at 0x0000021E7F5F0400>
#<class 'function'>
'''
['__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__getstate__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']

['__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__getstate__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
'''
import types
# types道具箱の中にある 'FunctionType' という名前の設計図を取り出す
print(dir(types.FunctionType))


#%% 8.1.4 戻り値 return命令
def show_current():
    import datetime
    print(datetime.datetime.now())
print(show_current())
print(show_current)
print(type(show_current))
print(type(show_current()))
#2026-05-19 15:14:22.172894
#None
#<function show_current at 0x0000021E7F5F16C0>
#<class 'function'>
#2026-05-19 15:18:05.700817
#<class 'NoneType'>

import datetime
print(datetime)
print(type(datetime))
print(type(datetime.datetime))
print(datetime.datetime)
print(type(datetime.datetime.now))
print(datetime.datetime.now)
print(dir(datetime.datetime))
print(dir(datetime.datetime.)
'''
<module 'datetime' from 'C:\\ProgramData\\spyder-6\\envs\\spyder-runtime\\Lib\\datetime.py'>
<class 'module'>
<class 'type'>
<class 'datetime.datetime'>
<class 'builtin_function_or_method'>
<built-in method now of type object at 0x00007FFEC27F2FC0>
'''

#%%　練習問題5
'''
次の各関数について、定義の1行目に記述する内容と、戻り値がある場合は望ましいデータ型を答えよ。なお、データ型は「int、float、str、bool」の4つの型、リスト・ディクショナリ・タプル・セットから選びなさい。
1呼び出すと、「今日は晴れです」という文字列を画面に表示するweather関数
2円の半径を渡すとその円の面積を返す calc_circle_are関数
3呼び出すと現在時刻を調べて、「18時25分30秒」のようなデータを返す nowstr関数
4呼び出しと現在時刻を調べて、時分秒を表す３つの数値を返すnowint関数
5西暦を渡すと、うるう年かを判定するis_leapyear関数

'''
# 5-1
#1.def weather():
#2.def calc_circle_area(radius): , float
#3.def nowstr(): , str
#4.def nowint(): , tuple
#5.def is_leapyear(year): , bool

#%% 5－2
'''
練習5－1の「5」is_leapyer関数を、以下の判定方法を参考にして関数定義を完成させなさい。
うるう年の判定方法
・400で割り切れる年はうるう年
・４で割り切れる年はうるう年だが、１００で割り切れる年はうるう年ではない
また、キーボードから現在の西暦を入力させてこの関数を呼び出して、次のように表示するプログラムを作成してください。
・うるう年だった場合　　　：西暦～～年は、うるう年です
・うるう年ではなかった場合：西暦～～年は、うるう年ではありません

'''
year = int(input('現在の西暦を入力してください:'))
def is_leapyear(year):
    if( year % 400 == 0):
        if(year % 100 == 0):
            return False
        else:
            return True
    else:
        return False
if (is_leapyear(year)==True):
    print(F'西暦{year}年は、うるう年です')
elif(is_leapyear(year)==False):
    print(F'西暦{year}年は、うるう年ではありません')

'''
現在の西暦を入力してください:2026
Traceback (most recent call last):

  Cell In[49], line 10
    if (is_leapyear(year)==True):

  Cell In[49], line 3 in is_leapyear
    if( year % 400 == 0):

TypeError: not all arguments converted during string formatting


'''















