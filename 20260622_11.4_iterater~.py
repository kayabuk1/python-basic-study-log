# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:12:19 2026

@author: iot01
"""

#%% 11.4 イテレーター
# 11.4.1 自作classでイテレーターを実装する
#↓まずはイテレーターを実装しないリストclassの例とのこと
class Person:
    def __init__(self,firstname,lastname):
        self.firstname = firstname
        self.lastname = lastname
    def show(self):
        print(f'私の名前は{self.firstname}{self.lastname}')
        
class PersonList:
    #Personclassのリストを格納する為の変数を準備
    def __init__(self):
        self.data = []
    def add(self, person)        :
        self.data.append(person)

if __name__=="__main__"        :
    #PersonListにPersonオブジェクトを格納
    pl = PersonList()
    pl.add(Person('太郎','山田'))
    pl.add(Person('奈美','掛谷'))
    pl.add(Person('悟助','田中'))
    
    #PersonListの内容を順に処理し、そのshowメソッドを実行
    for p in pl.data:
        p.show()
        # 私の名前は太郎山田
        # 私の名前は奈美掛谷
        # 私の名前は悟助田中
'''
PersonListで管理している Personのリストには、インスタンス変数 data経由で
アクセスすることになる。
しかし、変数dataにアクセスするのは少し冗長に感じるとのこと。
for p in pl: ~ と記述できたほうがよいとのこと。
''' 
#↓PersonListクラスに__iter__メソッドを追加して
#インスタンスそのものをforループに渡して簡単な記述でループ出来るようにする
class Person:
    def __init__(self,firstname,lastname):
        self.firstname = firstname
        self.lastname = lastname
    def show(self):
        print(f'私の名前は{self.firstname}{self.lastname}')
        
class PersonList:
    #Personclassのリストを格納する為の変数を準備
    def __init__(self):
        self.data = []
    def add(self, person)        :
        self.data.append(person)
    #↓を追加。 __iter__メソッドは、インスタンスに対して iter関数が呼ばれた時に
    #呼び出せられる予約メソッド。
    #戻り値としてイテレーターを返す必要があるとのこと
    #●そもイテレーターについて良くわかっていない。
    #●iter関数とはどんな関数？        
    def __iter__(self):
        return iter(self.data)

if __name__=="__main__"        :
    #PersonListにPersonオブジェクトを格納
    pl = PersonList()
    pl.add(Person('太郎','山田'))
    pl.add(Person('奈美','掛谷'))
    pl.add(Person('悟助','田中'))
    
    #PersonListの内容を順に処理し、そのshowメソッドを実行
    for p in pl:
        p.show()    
        # 私の名前は太郎山田
        # 私の名前は奈美掛谷
        # 私の名前は悟助田中
        
r'''
昌敏さん、データクラスを乗り越え、ついにPythonのループ処理の心臓部である**「イテレーター（Iterator）」**に到達しましたね！
「イテレーターについて良くわかっていない」「iter関数とはどんな関数？」という昌敏さんの疑問は、Pythonにおけるすべての for ループの「裏側のアーキテクチャ」を理解するための最強の問いです。
公式ドキュメント（契約書）の掟と、現場監督（システム）のスローモーションを用いて、1行1行完全に解剖します！
第1部：【真理】 イテレーターと iter() 関数の正体
#●そもイテレーターについて良くわかっていない。 #●iter関数とはどんな関数？
結論から言うと、イテレーターとは**「データを1つずつ順番に運んでくる『専用のベルトコンベア（運搬係）』」のことです。そして iter() 関数は、「対象のオブジェクトに対して『おい！お前専用のベルトコンベアを出せ！』と命令するコマンド」**です。
公式ドキュメント（9.8. イテレータ）には、この仕組みについて次のように絶対の掟が書かれています
。
「裏では for 文はコンテナオブジェクトに対して iter() 関数を呼んでいます。関数は、コンテナの中の要素に1つずつアクセスする __next__() メソッドが定義されているイテレータオブジェクトを返します。これ以上要素が無い場合は、 __next__() メソッドは StopIteration 例外を送出し、その通知を受け for ループは終了します。」
つまり、Pythonの for ループは、実は裏側で例外（エラー）を利用して停止するという、とんでもなくシステマチックな動きをしていたのです！
第2部：【解剖】 現場監督のスローモーション（for p in pl: の裏側）
それでは、PersonList クラスに __iter__ メソッドを追加したコードで、for p in pl: が実行されたときの現場監督の動きをスローモーションで追ってみましょう。
① ループの開始準備と iter() 関数の発動
    for p in pl:
現場監督：「よし、pl（PersonListのインスタンス）を対象に for ループを回すぞ！」
現場監督：「for ループの絶対ルールに従い、まずは pl に向かって iter(pl) を実行し、専用の運搬係（イテレーター）を提出させろ！」
現場監督：「pl クラスの設計図を確認……おっ！ __iter__ メソッドが定義（オーバーライド）されているな！ これを呼び出せ！」
② __iter__ メソッドの内部処理
    def __iter__(self):
        return iter(self.data)
現場監督（メソッド内部）：「自分自身の金庫の中にある self.data（リスト）を取り出せ。そして、そのリストに向かって iter(self.data) を実行し、**『リスト専用のベルトコンベア』**を作成して呼び出し元（forループ）に返せ！」
③ ベルトコンベア稼働（ループ本番） 5. 現場監督：「よし、pl から『リスト専用のベルトコンベア（イテレーター）』を受け取ったぞ！」 6. 現場監督：「コンベアのスイッチ（next()）を押せ！ 1人目の『山田太郎』が流れてきたぞ！ これを変数 p に代入して、ループの中身（p.show()）を実行しろ！」 7. 現場監督：「再びコンベアのスイッチを押せ！ 2人目の『掛谷奈美』が流れてきた！ p に代入して実行！」 8. 現場監督：「3人目の『田中悟助』も実行！」 9. 現場監督：「もう一度コンベアのスイッチを押せ！……おっと、もうデータがない！ コンベアが StopIteration という例外（エラー） を吐き出して停止したぞ！」 10. 現場監督：「StopIteration のエラーを検知したな。よし、ここで for ループを安全に終了しろ！」
第3部：【実務】 なぜこんな回りくどいことをするのか？
最初のコードのように、for p in pl.data: と書けば普通に動きます。なぜわざわざ __iter__ を追加して for p in pl: と書けるようにするのでしょうか？
これは先日学んだ**「カプセル化（情報の隠蔽）」**という設計思想の極みです。
もし for p in pl.data: という書き方を許してしまうと、このクラスを使う他のプログラマーは「pl の中には data という名前のリストが入っているんだな」と内部構造を知る必要が出てきます。 後になって、インフラの要件変更で「やっぱりリストじゃなくて辞書で管理しよう」と内部構造を変えた瞬間、pl.data と書いていた世界中のコードがすべてクラッシュします。
しかし、__iter__ を実装して for p in pl: と書けるようにしておけば、外側のプログラマーは「どうやってデータが保存されているか（リストなのか辞書なのかデータベースなのか）」を一切気にせず、**「とりあえず for に突っ込めば順番に出てくる便利な箱」**として直感的に扱うことができるのです。
■ 参謀からの総括（アーキテクチャの真理）
イテレーター（Iterator）: データを1つずつ順番に運んでくる「ベルトコンベア」。データが尽きると StopIteration エラーを出して止まる
。
iter() 関数: オブジェクトの __iter__ メソッドを呼び出し、そのベルトコンベアを生成・取得するためのコマンド
。
for ループの正体: 裏側で iter() を使ってコンベアを作り、next() を押し続け、StopIteration エラーが出たら終了するという自動化システム
。
「自作のクラスを、Python標準のリストや文字列と全く同じように for ループに放り込めるようにする魔法」。スッキリと腹落ちされましたでしょうか！🦁🔥
'''    
    
#%% 11.4.2 素数を求めるイテレーター
import math

class Prime:
    def __init__(self, max):
        self.max = max
        self.__current = 1
    
    #イテレーター※自分自身を返す
    def __iter__(self):
        return self
    
    #イテレーターの本体を実装
    def __next__(self):
        while True:
            self.__current += 1
            if self.__current > self.max:
                raise StopIteration
            elif self.__is_prime(self.__current):
                return self.__current
    
    #引数valueが素数かどうかを判定
    def __is_prime(self, value):
        result = True #素数かどうかを表すフラグ
        # 2~sqrt(value)で Valueを割り切れる(=余りが0)ものがあるか判定
        #10なら、 平方根は√100≒10．0これを切り捨て 10 。
        #これに+1 して 11。 range(始まりの数, 終わりの数（含まない）までなので)、
        #11まで 1つずつ数を取り出して、 value=__currentを i (1~10)で割って、 割り切れる場合は、
        #素数でないのでFalse を返して、break。 次のforの数が割り切れるかのループになる。
        #そのforループも終われば、whileループに戻り__currentが1加算され、次のforループになる
        for i in range(2, math.floor(math.sqrt(value))+1):
            if value % i == 0:
                result = False #割り切れるものがあれば素数でない
                break
        return result
    
if __name__=="__main__"    :
    pr = Prime(100)
    for p in pr:
        print(p, end=",")
    #2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,
    
    
#%% 11.4.3 コンテナー型で利用出来る特殊メソッド
class Person:
    def __init__(self, firstname, lastname)    :
        self.firstname = firstname
        self.lastname = lastname
    def show(self):
        print(f'私の名前は{self.lastname}{self.firstname}です！')

class PersonList:
    #Personクラスを格納する為の変数を準備
    def __init__(self):
        self.data = []
    
    def add(self, person):
        self.data.append(person)
    def __iter__(self):
        return iter(self.data)
    
    #↓コンテナー型に関わる特殊メソッド
    def __getitem__(self, key):
    #↑obj[key]で参照した時に呼び出されている。
        return self.data[key]
    def __setitem__(self, key, value):
    #↑obj[key]=valueで設定した時呼び出されている。
        self.data[key] = value
    #●つまりobj[key]、 obj[key]=value この2つは糖衣構文？
    #●内部的には pl.__getitem__(pl, key)の様に変換されている？
    #●代入はすべて__setattr__とgetattribute__を経由すると聞いたけれど、
    # それはただの変数への代入であって、 コンテナー型への代入は異なるメソッド
    # __setitem__が呼び出されているということ？
    
if __name__=="__main__"        :
    pl = PersonList()
    pl.add(Person('太郎','山田'))
    pl.add(Person('奈美','掛谷'))
    pl.add(Person('悟助','田中'))
    
    print(pl[:])
    #[<__main__.Person object at 0x000001C8BA8AE910>, <__main__.Person object at 0x000001C8BA8B1BD0>, <__main__.Person object at 0x000001C8BA8B1FD0>]
    # print(pl[0:3].firstname)
    #AttributeError: 'list' object has no attribute 'firstname'
    #↑の書き方ではfirstnameにはアクセスできない。
    for p in pl:
        print(p.firstname) #太郎　奈美　悟助

    #↓listに値を代入＝__setitem__メソッドが呼び出される
    pl[1] = Person('哲也', '佐藤')
    #↓listの値を参照＝__getitem__メソッドが呼び出される
    print(pl[1].firstname)
    #哲也
    print(pl[0:3])
    #[<__main__.Person object at 0x000001C8BA8AE910>, <__main__.Person object at 0x000001C8BA8B0210>, <__main__.Person object at 0x000001C8BA8B1FD0>]
    for p in pl:
        print(p.firstname)
     #太郎　哲也　悟助
    
    
    
    
    
    
    
    
    
    
    