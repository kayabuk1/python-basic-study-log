# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 09:15:13 2026

@author: iot01
"""
#%%
###練習問題4
#%%練習４－１ 繰り返しが行われる回数を答えよ
#1.４回×　⇒５回
#2.４回×　⇒５回
#3.４回×　⇒５回
#4.５回〇
#5.５回〇
#6.５回〇
#7.４回〇
#8.４回×　⇒５回
#%%練習４－２
def wanko_curry():
    count = 0
    more_curry_flag = True
    while more_curry_flag == True:
        print('「カレーを食べる」')
        print(F'　「{count}皿のカレーを食べました」')
        more_curry = input('おかわりはいかがですか？（y/n）：')
        if more_curry == 'y':
            more_curry_flag = True
            count += 1
        elif more_curry == 'n':
            more_curry_flag = False
            print('「ごちそうさまでした」')
            break
        else:
            print('「カレーは飲み物です」')
            continue
wanko_curry()     
#%%練習４－３ カウントダウンプログラム
def contdown():
    count_number = [10,9,8,7,6,5,4,3,2,1,'THE END!']
    for i in count_number: 
        print(F"{str(i)}", end=',')

    count_number = [10,9,8,7,6,5,4,3,2,1,'THE END!']
    print(F"{','.join([str(i) for i in count_number])}",end='')

    count_number = [10,9,8,7,6,5,4,3,2,1,'THE END!']
    print(*F"{','.join([str(i) for i in count_number])}",sep='',end='')

    count_number = [10,9,8,7,6,5,4,3,2,1,'THE END!']
    # joinは使わず、リストの前に直接 * をつけ、隙間にカンマを指定する
    print(*[str(i) for i in count_number], sep=',')

    count_number = [10,9,8,7,6,5,4,3,2,1,'THE END!']
    print(*F"{[str(i) for i in count_number]}",end='')
    '''
    10,9,8,7,6,5,4,3,2,1,THE END!,
    10,9,8,7,6,5,4,3,2,1,THE END!
    10,9,8,7,6,5,4,3,2,1,THE END!
    10,9,8,7,6,5,4,3,2,1,THE END!
    [ ' 1 0 ' ,   ' 9 ' ,   ' 8 ' ,   ' 7 ' ,   ' 6 ' ,   ' 5 ' ,
     ' 4 ' ,   ' 3 ' ,   ' 2 ' ,   ' 1 ' ,   ' T H E   E N D ! ' ]
    '''
contdown()
#%%練習４－４
#1.九九の計算プログラム
def kuku():
    for i in range(1,10):
        for j in range(1,10):
            result = i*j
            print(F"{result:2}",end=' ')
        print()
kuku()
#2.奇数の段のみ計算するプログラム
def kuku_kisu():
    for i in range(1,10):
        for j in range(1,10):
            result = i*j
            if i % 2 == 0:
                continue
            else:
                print(F"{result:2}",end=' ')
        print()
kuku_kisu()
#3．奇数の段のみ、かつ、答えが50を超えたら次の段の計算へ進む
def kuku_kisu_under50():
    for i in range(1,10):
        for j in range(1,10):
            result = i*j
            if i % 2 == 0:
                continue
            else:
                if result >= 50:
                    break
                print(F"{result:2}",end=' ')
        print()
kuku_kisu_under50()
'''
 1  2  3  4  5  6  7  8  9 
 2  4  6  8 10 12 14 16 18 
 3  6  9 12 15 18 21 24 27 
 4  8 12 16 20 24 28 32 36 
 5 10 15 20 25 30 35 40 45 
 6 12 18 24 30 36 42 48 54 
 7 14 21 28 35 42 49 56 63 
 8 16 24 32 40 48 56 64 72 
 9 18 27 36 45 54 63 72 81 
 1  2  3  4  5  6  7  8  9 

 3  6  9 12 15 18 21 24 27 

 5 10 15 20 25 30 35 40 45 

 7 14 21 28 35 42 49 56 63 

 9 18 27 36 45 54 63 72 81 
 1  2  3  4  5  6  7  8  9 

 3  6  9 12 15 18 21 24 27 

 5 10 15 20 25 30 35 40 45 

 7 14 21 28 35 42 49 

 9 18 27 36 45 
'''
#%%練習４－５
#1.
d_noontime_temptr = {'8時':7.8,'9時':9.1,'10時':10.2,'11時':11.0,
                     '12時':12.5,'13時':12.4,'14時':14.3,'15時':13.8}
#2.
#3.
#%%練習４－６
#1.
#%%