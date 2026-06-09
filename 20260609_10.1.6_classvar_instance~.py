# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:56:42 2026

@author: iot01
"""

#%% 10.1.6補足 クラス変数をインスタンス経由で操作する
class Area:
    PI = 3.14
if __name__ == '__main__':
    a = Area()
    print(a.PI) #3.14クラス変数が表示
import decimal
a.PI = decimal.Decimal(3.141592)
print(a.PI) #3.1415920000000001621742740098... インスタンス変数が表示
print(Area.PI) #3.14 クラス変数が表示
r'''
◆インスタンス経由での、 クラス変数への代入は、 代入にならない。
  ⇒新たにインスタンス変数 a.PI が生成され、 それに代入がされるだけ。
  ※クラス変数と同名のインスタンス変数を生成してしまったので、 
    そのインスタンスからクラス変数にアクセス画できなくなることに注意。
'''
'''◆Pythonのインスタンス化：__new__と__init__の真実
第1部：【真理】 普通のクラスは全自動で親方（object.__new__）を呼んでいる
Q. 普通のclass定義で__init__しか書いていなけれど、自動的にobject.__new__が呼ばれている？
おっしゃる通りです。公式ドキュメントには、「クラスの新しいインスタンスを作るために __new__() が呼び出される」
、「インスタンスが ( __new__() によって) 生成された後、(...) __init__() が呼び出される」
と明確に定義されています。
普段、昌敏さんが Person('太郎', 30) のようにインスタンス化を行うとき、裏側では以下の「2段階の連係プレイ」が全自動で行われています。
■ 現場監督のスローモーション（通常のクラスの場合）
現場監督：「Person の実体を作れと呼ばれたぞ！ まずは物理的な箱を作るために __new__ を探せ！ ……おっと、Person クラスには __new__ が書かれていないな！」
現場監督：「ならば、親方（object）の __new__ を自動的に借りてこい！ 親方、Person の金型を使って空の箱を作ってください！」（➔ これでメモリ上に箱が確保されます）
現場監督：「箱ができたぞ！ 次は、その箱の中に初期データ（'太郎', 30）を入れる作業だ！ Person クラスに書いてある __init__ を呼び出して、先ほど作った箱（self）にデータを流し込め！」
このように、親クラスの機能を自動的に探しに行く「継承の仕組み」のおかげで、私たちは普段、箱作りの泥臭い部分（__new__）を完全に親方（object）に任せきりにし、データを入れる __init__ だけを書けば済んでいるのです。
第2部：【解剖】 なぜ MySingleton は __init__ を書いていないのか？
Q. なぜMySingltonは__init__を書いていないのだろう？
理由は2つあります。1つ目は単純に「今回のサンプルコードが『箱を1つしか作らせない』という仕組み（__new__）の検証に特化したものであり、中にデータを入れる必要がなかったから」です（書いていない場合は、親方である object の「何もしない __init__」が自動で呼ばれて終わります）。
そして2つ目の理由こそが、シングルトンパターンにおける**「最大の罠（オーバーライドのリスク）」**に関わってきます。
■ もしシングルトンに __init__ を書いてしまうと起きる悲劇 公式ドキュメントには、現場監督の絶対ルールとして以下のように書かれています。
「もし __new__() が (...) クラスのインスタンスを返した場合には、 (...) 新しいインスタンスの __init__() が呼び出されます」
シングルトンで __init__ を書いてしまった場合の動きを想像してみてください。
1回目 c1 = MySingleton('設定A'): __new__ で箱を作り、__init__ で箱に「設定A」を入れる。
2回目 c2 = MySingleton('設定B'): __new__ は「前回作った c1 の箱」をそのまま返す。しかし現場監督の絶対ルールにより、返ってきた箱に対して毎回必ず __init__ が実行されてしまうため、同じ箱の中身が勝手に「設定B」で上書きされ、c1の設定まで「設定B」に変わってしまうのです！
これを防ぐためには、「初回だけ初期化し、2回目以降は __init__ を無視する」といった複雑な制御を自分で追加しなければなりません。だからこそ、シングルトンの基本を学ぶコードでは、余計なバグや混乱を避けるために __init__ 自体が省略されているのです。
'''

#%%# 10.2 カプセル化
# ここからは、 よりオブジェクト指向らしいコードを記述する為の技術について学んで行く
#●ｷｰﾜｰﾄﾞ：１．カプセル化、 ２．継承、 ３．ポリモーフィズム※これでｵﾌﾞｼﾞｪｸﾄ指向の全てでは無い
# 10.2.1 カプセル化とは？ 使い手に関係無いものは見せない
'''
カプセル化とは：「オブジェクトの持つ変数（辞書）を外部からの直接の代入による破壊（今回 PI で起きたような事故）から守るための**『防弾装甲』であり、安全な窓口（メソッド）だけを外部に公開する『API設計』**である」。
教科書で「カプセル化」「隠蔽」「プロパティ」「アンダースコア」といった言葉が出てきた際、「あぁ、要するに現場監督が管理している辞書（__dict__）に、外の人間が直接アクセスできないようにルールや関所を作っている話
'''
#%% 10.2.2 インスタンスの隠蔽
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def show(self):
        print(f'私の名前は{self.name},{self.age}歳です！')
print(dir(Person.__dict__)) 
#dir() は『そのオブジェクトが持っている標準機能（ボタン）を一覧表示しろ』という命令。
#これだと辞書ｵﾌﾞｼﾞｪｸﾄ自体の機能表示しろになってしまう、、、。
#['__class__', '__class_getitem__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__ior__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__or__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__ror__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'copy', 'get', 'items', 'keys', 'values']
print(Person.__dict__)
#{'__module__': '__main__', '__init__': 
#<function Person.__init__ at 0x000002347DD12F20>, 'show': <function Person.show at 0x000002347DD13CE0>, '__dict__': <attribute '__dict__' of 'Person' objects>, '__weakref__': <attribute '__weakref__' of 'Person' objects>, '__doc__': None}
#↑クラス.__dict__には show はあるが name, age は無い。
#pythonはメソッド（工具）」と「インスタンス変数（データ）」の保管場所が明確に分離されている
'''現場監督:
    「おっ、Person という金型（クラス）の設計図だな。よし、Person.__dict__
    （金型専用の辞書）を用意しろ！」
    「設計図には def __init__ と def show という関数（工具）が
    書かれているな。これらは全製品で使い回す共通の工具だから、
    金型の辞書にしまっておけ！」
    「……ん？ __init__ の中に self.name = name と書かれているな？」
    「これは**『実体（self）が工場で作られた時に、その実体の個人の辞書に
    name を書き込め』**という未来への指示書だ！
    今はまだ実体が存在しない（インスタンス化されていない）から、
    こんな個人データはメモリ上のどこにも存在しないぞ！ 金型の辞書には書くな！」
つまり、
クラス（金型）の辞書には「全実体で共有するメソッド」しか入らないのです。
name と age は、 p = Person('太郎', 30) と実行して初めてメモリ上に
生成される「実体（インスタンス）の専用辞書（p.__dict__）」の中にだけ現れます。
'''
#↑これまでのコード。 インスタンス変数にそのままアクセス出来る。 これが好ましくない。
'''
◆なぜ好ましくないか
1．読み書きの許可/禁止を制御できない。
    インスタンス変数＝インスタンスの状態を管理するための変数。
    （値の読み取りは許可することが多い）
2.値の妥当性を確認できない
    pythonはデータ型に寛容＝ageに文字列その他型を入れられることも可能=エラー原因
3．内部状態に左右される
    age:int⇒age:decimal型になったら、参照している全てのコードが影響を受ける
'''
# 対処法： インスタンス変数名を __instans変数 （ｱﾝﾀﾞｰｽｺｱ2個）で命名するだけ
class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
    def show(self):
        print(f'私の名前は{self.__name},{self.__age}歳です！')
if __name__ == '__main__':
    p = Person('山田太郎', 15)
    print(p.__dict__)
    #{'_Person__name': '山田太郎', '_Person__age': 15}
    print(p.__age)
    #AttributeError: 'Person' object has no attribute '__age'
    #↑インスタンスの__dict__には _Person__ageとして登録されている！！ 
    #●名前マングリング（Name Mangling / 難号化）機能でリネームされている。
    #↓ _クラス名__インスタンス変数名 でアクセス出来てしまう。
    print(p._Person__age) #15と表示される。
    p.__age = 38
    p.show() #私の名前は山田太郎,15歳です！
    print(p.__age) #38 別のインスタンス変数を作ってしまった。
    print(p.__dict__)
    #{'_Person__name': '山田太郎', '_Person__age': 15,
    #'__age': 38}←これ
    p._Person__age = 38
    p.show() #私の名前は山田太郎,38歳です！ ←書き換えられてしまった、、、。

#%% 10.2.3 アクセサーメソッド Accessor Method （ｹﾞｯﾀｰ/ｾｯﾀｰﾒｿｯﾄﾞ）
# インスタンス内部から隠蔽された変数にアクセスする為のメソッド
class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
    #↓nameのｹﾞｯﾀｰ（__name変数の値を取得）
    def get_name(self):
        return self.__name
    #ageのｹﾞｯﾀｰ（__age変数の値を取得）
    def get_age(self):
        return self.__age
    #nameのｾｯﾀｰ（__name変数の値を更新）
    def set_name(self, value):
        self.__name = value
    #ageのｾｯﾀｰ（__age変数の値を更新）
    def set_age(self, value):
        if value <= 0:
            raise ValueError('ageは正数で指定します')
        self.__age = value
    #↑アクセサーメソッドは メソッド なので、 実行時に任意の処理を加えることが可能。
    # フェイルファースト（Fail First：失敗するなら、できるだけ早く失敗させろ
    # システムを破壊するような不正な設定値が、オブジェクトの内部（辞書）に混入するのを水際で防ぐ
    def show(self):
         print(f'私の名前は{self.get_name()},{self.get_age()}\
               歳です！')       
if __name__ == '__main__':
#↑ちなみに __name__ はこのPythonファイル（モジュール）自身が持っている、
#グローバルなシステム変数。
#Pythonのシステムは、ファイル（スクリプト）を実行する際、そのファイル全体を
#「1つのモジュール」という大きな箱として扱います。そして、その大きな箱の一番外側
#（グローバル名前空間）に、システムが勝手に __name__ という名札（変数）を用意します。
    p = Person('山田太郎', 15)
    print(dir(Person))
    #['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'get_age', 'get_name', 'set_age', 'set_name', 'show']
    #↑そのクラスが利用できる 「すべてのボタン（属性やメソッド）の名前リスト」
    print(Person.__dict__)
    #{'__module__': '__main__', '__init__': 
    #<function Person.__init__ at 0x000002347DD20C20>, 'get_name': <function Person.get_name at 0x000002347DD20B80>, 'get_age': <function Person.get_age at 0x000002347DD20AE0>, 'set_name': <function Person.set_name at 0x000002347DD20CC0>, 'set_age': <function Person.set_age at 0x000002347DD20EA0>, 'show': <function Person.show at 0x000002347DD20F40>, '__dict__': <attribute '__dict__' of 'Person' objects>, '__weakref__': <attribute '__weakref__' of 'Person' objects>, '__doc__': None}
    #↑class Person: のブロック内に書いた共通の辞書（工具（メソッド））だけ表示
    print(p.__dict__)
    #{'_Person__name': '山田太郎', '_Person__age': 15}
    #↑pというインスタンス実体だけが持つ個人の辞書データ（インスタンス変数）のみ表示
    p.set_age(35)
    print(p.get_age()) #35
    p.set_age(-15)
    #ValueError: ageは正数で指定します
'''◆なぜｾｯﾀｰ/ｹﾞｯﾀｰﾒｿｯﾄﾞを介することで、内部データの変更で他のコードへの影響を抑えれるのか？

A.窓口（インターフェース）と、裏側の仕組み（実装）を完全に切り離すことができるから」です。
これをアーキテクチャ用語で「疎結合（そけつごう）」**と呼びます。
--------------------------------------------------------------------------------
第1部：【密結合】直接アクセスさせていた場合の悲劇
もしカプセル化をせず、外のプログラムに p.age を直接読み書きさせていたとします。
ある日、システム要件が変わり、「年齢（age）を直接保存するのではなく、『生年月日（birth_year）』を
保存しておき、年齢が聞かれたらその都度計算して返す仕組みに変更しろ」という指示が出ました。
■ 現場の悲劇（直接アクセスの場合） クラスの裏側を self.birth_year に変更した瞬間、
どうなるでしょうか？ 
メインストリート（外のプログラム）で p.age = 15 や print(p.age) と書いていた何百箇所ものコードが、
すべて「そんな変数はない！」と一斉にエラーを吐いてシステムが崩壊します。 
裏側の仕組み（変数名や持ち方）を変えただけで、外側のコードまで全部書き直さなければならない。
これが「密結合（変化に弱い設計）」の末路です。
第2部：【疎結合】アクセサーメソッドがもたらす防弾装甲
一方、今回外のプログラムには p.get_age() と p.set_age() という**「窓口（メソッド）」だけを
使わせている場合**はどうなるでしょうか。
■ 現場監督のスローモーション（仕様変更後の世界）
import datetime
class Person:
    def __init__(self, name, birth_year):
        self.__name = name
        # 裏側のデータを「年齢」から「生年月日」に変更！
        self.__birth_year = birth_year 
    # 窓口（ゲッター）の名前と使い方は変えない！
    def get_age(self):
        # 現場監督：「年齢を聞かれたな！裏の生年月日から今の年齢を計算して返してやるぞ！」
        current_year = datetime.date.today().year
        return current_year - self.__birth_year
外のプログラム（他のコード）: print(p.get_age())
現場監督: 「おっ、get_age() が呼ばれたな。よし、裏側で生年月日から年齢を計算して、
    結果だけを返してやろう！」
外のコードは、今まで通り p.get_age() と呼び出すだけです。
裏側で「ただ変数の値をそのまま返している」のか、「生年月日から複雑な計算をして返している」のか、
外の人間は一切知る必要がありませんし、外のコードを1行も書き換える必要がありません。
--------------------------------------------------------------------------------
■ まとめ
答えは、**「外部のコードは『メソッドの名前と使い方（API）』にだけ依存し
、『裏側でデータをどう持っているか』には依存しなくなるから」**です。 
'''
#%% 10.2.4 プロパティ p.set_name('山田')を p.name = '山田'と直観的に表現可能にする
#その為にpythonでは、
#クラス内部ではメソッドの様に表現できるが、 外部から変数の様にアクセス出来る仕組みがある。
#それがpythonの プロパティ 。
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        #↑__nameの様に記述していない
    #↓プロパティの設定
    #プロパティ（値取得）
    @property
    def name(self):
        return self.__name
        #↑プロパティの中では __nameとアンダーバーがついている。
    @property
    def age(self):
        return self.__age
    #プロパティ（値設定）
    @name.setter
    def name(self, value):
        self.__name = value
    @age.setter
    def age(self, value):
        if value <= 0:
            raise ValueError('ageは正数で指定します')
        elif type(value) != int:
            raise TypeError('整数以外指定は出来ません')
        self.__age = value
    def show(self):
         print(f'私の名前は{self.name},{self.age}\
               歳です！')
               #↑こちらは.name表記
'''
プロパティ（@property）を設定したことで、name や age は「関数（メソッド）」としての顔を隠し、「変数」として振る舞うようになりました。 したがって、self.name() とカッコ () を付けて「関数として実行しろ」と命令すると、現場監督は「self.name で取得した文字列（'山田太郎'）に対してカッコがつけられたぞ！ 文字列は実行できない（not callable）！」と TypeError を出してクラッシュします。
'''
if __name__ == '__main__':
    p = Person('山田太郎', 15)
    p.name = '鈴木次郎'
    p.age = 35
    #↑変数に代入するように書ける
    print(p.name)
    print(p.age)
    print(Person.__dict__)
    #{'__module__': '__main__', '__init__':
    #<function Person.__init__ at 0x000002347DD218A0>,
    #'name': <property object at 0x000002347DD5C2C0>,
    #'age': <property object at 0x000002347DD5D8A0>,
    #'show': <function Person.show at 0x000002347DD21EE0>,
    #'__dict__': <attribute '__dict__' of 'Person' objects>, '__weakref__': <attribute '__weakref__' of 'Person' objects>, '__doc__': None}
    print(p.__dict__)
    #{'_Person__name': '鈴木次郎', '_Person__age': 35}
    print(property)
    #<class 'property'>
    print(type(property))
    #<class 'type'>
    print(dir(property))
    #['__class__', '__delattr__', '__delete__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__isabstractmethod__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__set__', '__set_name__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    #'deleter', 'fdel', 'fget', 'fset', 'getter', 'setter']
    print(property.__dict__)
    #'getter': <method 'getter' of 'property' objects>,
    #'setter': <method 'setter' of 'property' objects>,
    p.age = '-31'
    #    if value <= 0:
    #TypeError: '<=' not supported between instances of 'str' and 'int'
    #●思ったエラー動作にならなかったのはなぜ？
    #●propertyｵﾌﾞｼﾞｪｸﾄとは何か？
    #●なぜ@propertyブロック内では __ がついていたのか？
    #●そもそも @property @ .setter の仕組みとは？
R'''
A1.Pythonの厳格な型比較ルールが原因
    左は文字列（str）、右は数値（int）だ！ Pythonのルール（
）では、違う型同士を < や <= で大小比較することは絶対に禁止されている！ 比較しようとした時点で俺の権限で TypeError を強制発動する！！

A2A3.
■ カプセル化のジレンマ 前回作った「ゲッター/セッター（get_age(), set_age()）」は安全でしたが、使う側からすると p.set_age(35) と書かなければならず、直感的な p.age = 35 という書き方ができなくなってしまいました。 これを解決するのが 「プロパティ（データデスクリプタ）」 の魔法です。公式ドキュメント（
）にも「property() 関数はデータデスクリプタとして実装されています」と明記されています。
■ @property の正体 クラスの直下に書かれた @property は、単なる印ではなく**「現場監督への関所設置の命令」**です。
@property と書くと、関数 name は、property クラスの実体（関所オブジェクト）に変換されてクラスの辞書に置かれます。
外の人間が p.name = '鈴木次郎'（代入）や print(p.name)（取得）という**「ただの変数アクセス」**をしてきた瞬間、現場監督は「おっ、これはただの変数じゃないな。プロパティ（関所）が設置されているぞ！ じゃあ裏側でこっそり、設定された関数（セッターやゲッター）に誘導して実行してやろう！」と動くのです。
**「見た目はただの変数、中身はガチガチの関数（メソッド）」。**これがプロパティの正体です。

A4. 現場監督のスローモーション（ __init__ 実行時）
def __init__(self, name, age):
    self.name = name  # ← ここで何が起きるか？
現場監督：「おっ、self.name に値を代入しろという命令だな！」
現場監督：「name はただの変数じゃないぞ！ クラス側に @name.setter という関所（プロパティ）が設定されている！ よし、セッター関数を起動しろ！」
そう、実は __init__ に書かれた self.name = name はただの代入ではなく、いきなりセッターを呼び出しているのです！
■ もしセッターの中で __ を使わず self.name = value と書いたら？
@name.setter
def name(self, value):
    self.name = value  # もしこう書いたら…？
現場監督：「よしセッターを起動したぞ。中身の処理は……『self.name に値を代入しろ』だな！」
現場監督：「ん？ name には関所（セッター）が設定されているぞ！ よし、セッター関数を起動しろ！」
現場監督：「よしセッターを起動したぞ。中身の処理は……『self.name に値を代入しろ』だな！」
現場監督：「ん？ name には関所が……（以下、永遠に繰り返し）」
これが 「無限再帰（RecursionError）」 というクラッシュです。 【解決策】: セッターという「関所の処理」の中では、もう一度関所を通るようなコード（self.name）を書いてはいけません。関所を無事に通過した値は、関所のない**「裏の隠し金庫（self.__name）」**にそっと保存しなければならないのです。 だからこそ、プロパティの内部処理では必ず __（名前マングリング）を使った別の変数名に退避させているのです。
'''

#%% 補足： property関数
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    #↓nameのｹﾞｯﾀｰ（__name変数の値を取得）
    def get_name(self):
        return self.__name
    #ageのｹﾞｯﾀｰ（__age変数の値を取得）
    def get_age(self):
        return self.__age
    #nameのｾｯﾀｰ（__name変数の値を更新）
    def set_name(self, value):
        self.__name = value
    #ageのｾｯﾀｰ（__age変数の値を更新）
    def set_age(self, value):
        if value <= 0:
            raise ValueError('ageは正数で指定します')
        self.__age = value
    #↑アクセサーメソッドは メソッド なので、 実行時に任意の処理を加えることが可能。
    # フェイルファースト（Fail First：失敗するなら、できるだけ早く失敗させろ
    # システムを破壊するような不正な設定値が、オブジェクトの内部（辞書）に混入するのを水際で防ぐ
    def show(self):
         print(f'私の名前は{self.name},{self.age}\
               歳です！') 
               #↑ここでもge_nameの後ろの()が不要になっていることに注目
    name = property(get_name, set_name)
    age = property(get_age, set_age)
if __name__ == '__main__':
    p = Person('山田太郎', 15)
    p.show()
    #私の名前は<bound method Person.get_name of <__main__.Person object at 0x000002347DD26C10>>,<bound method Person.get_age of <__main__.Person object at 0x000002347DD26C10>>               歳です！
    #●？！？なんだこのエラーは？
    #class Person:
   #     def __init__(self, name, age):
   #        self.__name = name
   #        self.__age = age のままになっていたので修正、、、。
   #●{self.get_name},{self.get_age}\ここが原因だった。
   #(f'私の名前は{self.name},{self.age}\に修正。
   #私の名前は山田太郎,15               歳です！

r'''◆ propertyの仕組み
第1部：【解剖】なぜ <bound method...> が出力されたのか？
私の名前は<bound method Person.get_name of ...>... ●？！？なんだこのエラーは？
この奇妙な出力は、エラー（プログラムの異常終了）ではありません。現場監督（Pythonシステム）は、昌敏さんの指示を**「1ミリの狂いもなく正確に」**実行しただけなのです。
■ 現場監督のスローモーション（ print(self.get_name) 実行時）
現場監督：「show メソッドの中で、self.get_name を出力しろという命令だな！」
現場監督：「ん？ get_name の後ろに実行の合図であるカッコ () がついてないぞ！」
現場監督：「ということは、工具を使って作業しろという命令ではなく、**『工具（メソッド）そのものを見せろ』**という命令だな。よし、この get_name というメソッドがメモリ上のどこに結びついている（bound）かの情報をそのまま文字列にして返してやれ！」
Pythonでは、関数やメソッドも単なる「オブジェクト（第一級オブジェクト）」です。
self.get_name() ➔ カッコがあるので「実行して結果（名前）を返す」。
self.get_name ➔ カッコがないので「メソッドという物質そのもの」を返す。
昌敏さんが self.name （プロパティ）に修正したことで、現場監督は「おっ、プロパティが呼ばれたから裏で自動的にゲッター関数を実行して結果を返すぞ！」と正しく動き、解決に至ったのです。
第2部：【真理】 property() 関数の正体とデコレータ
name = property(get_name, set_name)
前回学習した @property デコレータの形式と、今回の property() 関数を使った形式。これらは全く同じシステムを構築しています。
公式ドキュメント（関数定義やデータモデル）が語る真理として、実は @property などのデコレータは、プログラマが書きやすくするための「シンタックスシュガー（構文糖衣）」に過ぎません。
今回昌敏さんが書いた name = property(get_name, set_name) こそが、現場監督に「関所」を設置させるための最も原始的で直接的な命令です。
現場監督：「よし、クラスの中に name という『プロパティ（データデスクリプタ）』を設置するぞ！」
現場監督：「設定書によると、外の人間が p.name を読もうとしたら get_name を裏で起動し、p.name = '鈴木' と書き込もうとしたら set_name を裏で起動して検問にかければいいんだな！」
見た目はただの変数ですが、裏ではガチガチに設定された関数（アクセサーメソッド）へ通信をルーティングする。インフラで言えば、ロードバランサー（VIP）の裏に実サーバー（メソッド）を隠す設計そのものです。
第3部：【アーキテクチャ】 __init__ の修正がもたらした「完全なる防弾装甲」
今回のデバッグ記録の中で、私が最も高く評価したいのが以下の修正です。
def __init__(self, name, age): self.__name = name ➔ self.name = name に修正
昌敏さんは最初、裏の隠し金庫（__name, __age）に直接代入していましたが、これをプロパティ（self.name, self.age）経由の代入に書き直しました。 これは単なるタイポの修正ではなく、**「システムの脆弱性を塞ぐ、劇的なアーキテクチャの改善」**です！
■ もし self.__age = age のままだったら起きる悲劇 メインプログラムで p = Person('太郎', -10) とマイナスの年齢を渡してインスタンスを作った場合を想像してください。 隠し金庫（__age）に直接アクセスしてしまうと、せっかく作った「マイナスを弾くセッター（set_age）の関所」を完全にすり抜けて、内部に不正な値が混入してしまいます。（初期化時のバリデーションすり抜けバグ）
■ self.age = age に直したことで実現したフェイルファースト これを self.age = age （プロパティへの代入）に直したことで、インスタンスが誕生する瞬間（__init__）であっても、必ず set_age の関所を通るようになります。 これにより、「システムが起動した瞬間に不正な値（-10）を検知して即座にクラッシュさせる（Fail First）」という、堅牢なシステムの絶対原則が完成したのです。

'''









