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
def calc_temperture():
    d_noontime_temptr = {'8時':None,'9時':None,'10時':None,'11時':None,
                     '12時':None,'13時':None,'14時':None,
                     '15時':None,'16時':None,'17時':None}
    temp = d_noontime_temptr
    for time in d_noontime_temptr:
    #理由：Pythonは他の言語と違い、変数の事前宣言（名札の準備）が不要な言語です。
    #動作：for 新しい変数名 in データ: と書くだけで、システムが自動で箱を作り、データを
    #取り出して入れてくれます。　取り出されたキーが、変数 time に代入されます。
        try:
            user_input = input(F'{time}の気温を入力してください：')
            temp[time] = float(user_input)
            '''
            temp[time] と temp.time は何が違うのか？（最重要）
            [ ] （角括弧）＝ 添字表記（サブスクリプション）
                意味：「このコンテナ（辞書やリスト）の中に入っている、
                この名前（キー）のデータを取り出せ／書き換えろ」という命令です。
            特徴：括弧の中には変数を入れることができます（例： time 変数の中身をキーとして探す）。
            
            . （ドット）＝ 属性参照
                意味：「このオブジェクトそのものが持っている、機能（メソッド）や構造（プロパティ）を呼び出せ
                」という命令です。
                特徴：変数を使うことはできません。 temp.time と書くと、システムは変数 time の
                中身（'8時'）ではなく、「文字通りの time という名前の機能」を探します。
                '''
        except ValueError:
                    # 3. 変換失敗（空打ち、'N/A'、文字入力など）のValueErrorが出たらここに来る
                    # クラッシュさせず、代わりに文字列の 'N/A' を代入して処理を続ける
                    d_noontime_temptr[time] = 'N/A'
                    print(F'{time}の気温の入力に失敗しました。')
    print("\n【データ入力完了】")
    print(temp)
       #2.
       #3.
    temp_new = d_noontime_temptr
    try:
        user_input = input(F"{'13時'}の気温を入力してください：")
    except ValueError:
       # 3. 変換失敗（空打ち、'N/A'、文字入力など）のValueErrorが出たらここに来る
       # クラッシュさせず、代わりに文字列の 'N/A' を代入して処理を続ける
       d_noontime_temptr[time] = 'N/A'
       print(F'{time}の気温の入力に失敗しました。')
    print("\n【データ再入力完了】")
    print(temp_new)
   # 【修正部分】
    # 1. 'N/A' ではない、有効な数値だけを取り出したリストを作る（リスト内包表記）
    valid_temps = [val for val in temp_new.values() if val != 'N/A']
    # 2. 有効なデータが1件以上あるかチェックして平均を計算する（ゼロ割りエラーを防止）
    if len(valid_temps) > 0:
        avg = sum(valid_temps) / len(valid_temps)
        print(F'平均気温は{avg:.2f}度です。')
    else:
        print('有効な気温データがないため、平均を計算できません。')
calc_temperture()
#%%練習４－６
#1.
#%%