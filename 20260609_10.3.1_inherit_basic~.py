# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:43:10 2026

@author: iot01
"""

#%%# 10.3 継承 Inheritance
# class 派生クラス名(基底クラス名, ...):
# 例 class BusinessPerson(Person):
class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    def show(self):
        print(f'私の名前は{self.lastname}{self.firstname}です！')
#
class BusinessPerson(Person):
    def work(self):
        print(f'私、{self.lastname}{self.firstname}は働いています！')
if __name__ == '__main__':
    bp = BusinessPerson('太郎', '山田')
    bp.show() #私の名前は山田太郎です！
    bp.work() #私、山田太郎は働いています！
    print(bp) #<__main__.BusinessPerson object at 0x000002347DD27990>
    print(BusinessPerson) #<class '__main__.BusinessPerson'>
    print(type(bp)) #<class '__main__.BusinessPerson'>
    print(type(BusinessPerson)) #<class 'type'> 金型はtype型
    print(dir(bp)) 
    # '__weakref__', 'firstname', 'lastname', 'show', 'work']
    #↑初めから firstname, lastname, show を持っている。 
    print(type(object))
    #<class 'type'>
    print(dir(object))
    #['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
    print(object.__dict__)
    #{'__new__': <built-in method __new__ of type object at 0x00007FFE713A1760>, '__repr__': <slot wrapper '__repr__' of 'object' objects>, '__hash__': <slot wrapper '__hash__' of 'object' objects>, '__str__': <slot wrapper '__str__' of 'object' objects>, '__getattribute__': <slot wrapper '__getattribute__' of 'object' objects>, '__setattr__': <slot wrapper '__setattr__' of 'object' objects>, '__delattr__': <slot wrapper '__delattr__' of 'object' objects>, '__lt__': <slot wrapper '__lt__' of 'object' objects>, '__le__': <slot wrapper '__le__' of 'object' objects>, '__eq__': <slot wrapper '__eq__' of 'object' objects>, '__ne__': <slot wrapper '__ne__' of 'object' objects>, '__gt__': <slot wrapper '__gt__' of 'object' objects>, '__ge__': <slot wrapper '__ge__' of 'object' objects>, '__init__': <slot wrapper '__init__' of 'object' objects>, '__reduce_ex__': <method '__reduce_ex__' of 'object' objects>, '__reduce__': <method '__reduce__' of 'object' objects>, '__getstate__': <method '__getstate__' of 'object' objects>, '__subclasshook__': <method '__subclasshook__' of 'object' objects>, '__init_subclass__': <method '__init_subclass__' of 'object' objects>, '__format__': <method '__format__' of 'object' objects>, '__sizeof__': <method '__sizeof__' of 'object' objects>, '__dir__': <method '__dir__' of 'object' objects>, '__class__': <attribute '__class__' of 'object' objects>, '__doc__': 'The base class of the class hierarchy.\n\nWhen called, it accepts no arguments and returns a new featureless\ninstance that has no instance attributes and cannot be given any.\n'}
    #↑ものすごい長い。新しくオブジェクトを作れる__new__はobjectのdictにしかない
    #※下位クラスdirには表示される。
    print('\n',dir(Person))
    # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
    #'__dict__', '__module__', '__weakref__', 'show']
    #↑2段目の４つがdir(object)との違い。
    '''show: 自分で設計図に書き込んだ独自のメソッド（工具）です。
    __module__: このクラスがどのモジュール（ファイル）で定義されたかの名札です。
    __dict__ と __weakref__: Pythonはカスタムクラスが作られると、「将来生まれてくる
        実体（インスタンス）が、個人のデータを入れるための金庫（__dict__）と、
    ガベージコレクション用の裏口（__weakref__）を持てるようにする準備」を自動的に行います。'''
    print( Person.__dict__)
    #{'__module__': '__main__', '__init__': <function Person.__init__ at 0x0000027D8F2DEDE0>,
    #'show': <function Person.show at 0x0000027D8F2DF6A0>, '__dict__': <attribute '__dict__' of 'Person' objects>, '__weakref__': <attribute '__weakref__' of 'Person' objects>, '__doc__': None}
    #↑実はPerson独自のアトリビュートは__init__（改変）とshowだけ
    print(dir(BusinessPerson))
    # __weakref__', 'show', 'work']
    #↑クラスメソッドにも最初からある
    print(BusinessPerson.__dict__)
    #{'__module__': '__main__',
    #'work': <function BusinessPerson.work at 0x000002347DD223E0>,
    #'__doc__': None}
    #↑BPのdictにはworkしかない＝親クラスのdic参照している！！
    #継承は「コピー」ではなく「リンク（参照）」
    # 親の辞書（__dict__）をコピーするのではなく、見つからない時に親へ探しに行く 
    # 「動的な参照ルートの構築」
R'''◆コードの動作解説
第1部：【証明】 継承による「工具の引き継ぎ」
bp.show() # 私の名前は山田太郎です！ 
bp.work() # 私、山田太郎は働いています！
これは、「継承（Inheritance）」が完璧に機能していることの証明です。 
bp は BusinessPerson という子クラス（派生クラス）から作られた実体ですが、
子クラスの設計図には __init__（初期化）も show（名前表示）も書かれていません。

■ 現場監督のスローモーション
現場監督：「bp.show()を実行しろだな！まずは BusinessPerson の金型に show 
        という工具があるか探せ！……ないぞ！」
現場監督：「だが焦るな、この金型は Person を親（基底クラス）として継承している！
        親の Person の金型を探しに行け！……おっ、show という工具があったぞ！ 
        これを借りてきて実行だ！」
このように、インフラ自動化で「Ciscoルーター用クラス」を作る際、「全ルーター共通のログイン機能」は
親クラスに1回だけ書いておき、子クラスには「Cisco独自のコマンド処理」だけを書く、といった
**差分プログラミング（コードの再利用）**ができるのが継承の最大のメリットです。

第2部：【真理】 実体と金型の「格の違い」
print(bp) # <__main__.BusinessPerson object at 0x...> 
print(BusinessPerson) # <class '__main__.BusinessPerson'> 
print(type(BusinessPerson)) # <class 'type'> 金型はtype型
この出力は、Pythonにおける「オブジェクトの正体」を如実に表しています。
bp (実体): メモリ上の特定の番地（0x00000...）に物理的な領域（箱）を
        確保して作られた「製品」です。
BusinessPerson (金型): これ自体もメモリ上に存在するオブジェクトですが、
                    実体ではなく <class> という設計図としての顔を持っています。
type(BusinessPerson) 
が <class 'type'> になる理由: 
    Pythonの真理として、**「クラス（金型）を作るための、さらに大元となる究極の金型が
    存在する」**のです。それが type クラスです。すべてのクラスは、裏側では
    この type という工場から生み出されたオブジェクトに過ぎません。
    
第3部：【解剖】 dir と __dict__ が暴く「辞書の分離」
ここが、昨日から続く「カプセル化と辞書」の伏線回収となる最も重要なポイントです！
print(dir(bp)) ➔ ['firstname', 'lastname', 'show', 'work', ...] 
print(dir(BusinessPerson)) ➔ ['show', 'work', ...]
dir() は、「そのオブジェクトが自前で持っているものと、親から借りてこれるものをすべて合算したリスト」を
返します
。
実体 bp は、個人のデータ（firstname, lastname）と、親の工具（show）、
自身の工具（work）をすべて使えるため、全部リストアップされます。
金型 BusinessPerson には個人のデータがないため、工具（show, work）だけが
リストアップされます。
しかし、__dict__（専用の金庫）を開けてみると真実が暴かれます。
print(BusinessPerson.__dict__)
 {'__module__': '__main__', 'work': <function ...work at 0x...>,
  ...}
BusinessPerson クラスの本当の持ち物（専用辞書）には、work メソッドしか入っていません！
親クラスから継承したはずの show が辞書に入っていないのはなぜでしょうか？ 
それは、現場監督が**「無駄なメモリを食うな！ 親の工具（show）は親の辞書に
置いたままにしておけ。
使いたい時だけ親の辞書に探しに行けばいい！」**という非常にエコ（メモリ節約的）な
アーキテクチャで動いているからです。
--------------------------------------------------------------------------------
■ まとめ（Next Actionへの布石）
継承の振る舞い: 子クラスは、親の __init__ やメソッドを自前のもののように呼び出せる
（差分プログラミング）。
dir() の正体: 「親の持ち物」まで全部たどってかき集めた、使い勝手の良い総合カタログ。
__dict__ の正体: そのオブジェクト自身が「物理的に保有しているデータ」だけを厳密に
                管理する生々しい金庫。
'''
#%% 10.3.2 メソッドのオーバーライド
class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    def show(self):
        print(f'私の名前は{self.lastname}{self.firstname}です！')
class BusinessPerson(Person):
    def work(self):
        print(f'私、{self.lastname}{self.firstname}は働いています！')
class EliteBusinessPerson(BusinessPerson):
    def work(self):
        print(f'{self.lastname}{self.firstname}はﾊﾞﾘﾊﾞﾘ働いています')
if __name__=='__main__':
    bp = EliteBusinessPerson('太郎', '山田')
    bp.work()
    #山田太郎はﾊﾞﾘﾊﾞﾘ働いています
    bp.show()
    #私の名前は山田太郎です！
    print(bp.__dict__)
    #{'firstname': '太郎', 'lastname': '山田'}
    print(EliteBusinessPerson.__dict__)
    #{'__module__': '__main__',
    #'work': <function EliteBusinessPerson.work at 0x0000027D8F3007C0>, '__doc__': None}
    #'work': <function BusinessPerson.work at 0x000002347DD223E0>,
    #↑ちゃんとEliteBusinessPerson.workに変わっている。
R'''
●補足： 「オーバーロード（Overload：多重定義）」 について
■ 他の言語（JavaやC++など）におけるオーバーロード 静的型付け言語では
、「引数が1つの時の work メソッド」「引数が2つの時の work メソッド
」「文字列を渡された時の work メソッド」というように、
同じ名前のメソッドを複数同時に定義しておくこと（多重定義） が一般的。

Pythonの現場監督：「俺は動的型付け言語だから、引数の中身が文字列だろうが
数値だろうが気にしない！ 引数が何個来ようが、デフォルト引数や *args を使えば、
たった1つの work メソッドの中の if 文で全部さばき切れる！ 
だからわざわざ同じ名前のメソッドを複数作る必要なんてないんだ！」
つまり、Pythonでは「1つの強力で柔軟なメソッド（工具）を作る」というアーキテクチャを
採用しているため、オーバーロード（多重定義）という機能自体が不要（一般的ではない）。
'''
#%% 10.3.3 super()による基底クラスの参照 処理の not上書き but 付け足し
# super().ﾒｿｯﾄﾞ名(引数, ...)
#親が作った 標準の機能はそのまま利用しつつ、
#エリートやヘタレといった 『自分専用のオプション処理』 だけを前後に付け足したいというケース
class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    def show(self):
        print(f'私の名前は{self.lastname}{self.firstname}です！')
class BusinessPerson(Person):
    def work(self):
        print(f'私、{self.lastname}{self.firstname}は働いています！')
class HetareBusinessPerson(BusinessPerson):
    def work(self):
        super().work()
        print('ただし、ぼちぼちと...')
if __name__=='__main__':
    hbp = HetareBusinessPerson('太郎', '山田')
    hbp.work()
    #私、山田太郎は働いています！
    #ただし、ぼちぼちと...
    print(super)
    #<class 'super'> super自身も1つのクラス
    #print(super())
    #RuntimeError: super(): no arguments
    print(dir(super))
    #～'__self__', '__self_class__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__thisclass__']
    print(super.__dict__)
    print(HetareBusinessPerson.__dict__)
    #～\nThis works for class methods too:\nclass C(B):\n    @classmethod\n    def cmeth(cls, arg):\n        super().cmeth(arg)\n'}
    #{'__module__': '__main__',
    #'work': <function HetareBusinessPerson.work at 0x0000027D8F301120>, '__doc__': None}
    #dictとしては↑一応HBPクラスに登録されている。
    print(hbp.__dict__)
    #{'firstname': '太郎', 'lastname': '山田'}

R'''◆このコードでの動作解説
●第1部 super() による「差分プログラミング（付け足し）」
前回、子クラスで同じ名前の work() を作ると、現場監督は親の辞書を探しに行くのをやめて
しまうため、親の機能が「完全に見えなくなる（ 隠蔽・オーバーライド される）」と学びました。
しかし実務では、親が作った標準の機能はそのまま利用しつつ、
エリートやヘタレといった 『自分専用のオプション処理』 だけを前後に付け足したいというケースが
頻発します。
■ 現場監督のスローモーション（ hbp.work() 実行時）
現場監督：「hbp の work() を実行しろだな！ 
    まずは実体の辞書（hbp.__dict__）……無いな！ 
    次は金型の辞書（HetareBusinessPerson.__dict__）を探すぞ
    ……おっ、work 工具があった！ 実行だ！」
現場監督：「さて、ヘタレ専用 work の最初の指示は…… super().work() だな！」
現場監督（魔法の発動）：「super() とは、 
    HetareBusinessPerson の親クラス（基底クラス）である 
    BusinessPerson クラス辞書を見に行って、 呼び出し元の
    HetareBusinessPersonの代わりに、それを実行してこい』という命令だ！ 
    よし、親である BusinessPerson の辞書から work を探し出して実行しろ！」 
    ➔ （出力）私、山田太郎は働いています！
現場監督：「よし、親クラスの work 実行の仕事が終わったな。
    じゃあヘタレ専用 work に戻って続きを実行だ！」 
    ➔ （出力）ただし、ぼちぼちと...
これが「not 上書き but 付け足し」の正体です。 インフラで例えるなら、
　「親クラスが作った標準のパケットヘッダ生成処理を super() で呼び出して作らせ、
 子クラスは自分専用のペイロード（中身）だけを後ろに付け足して送信する」　という、
 極めて効率的なコードの再利用（DRY原則）です。
 
●第2部 super の正体は 「関数」 ではなく 「クラス」 である
print(super) ➔ <class 'super'> 
print(super()) ➔ RuntimeError: super(): no arguments
このログは、 Pythonの言語仕様を表しているものの1つです。
他の言語では super というのは単なるキーワード（予約語）に過ぎないことが
多いのですが、 Pythonの super は 組み込み の 「クラス（型）」 なのです
。
super() と実行することは
     「親クラスの辞書を安全に探しに行ってくれる 『代理人（プロキシ）オブジェクト』 を
     インスタンス化して生成している」 のと同じです。 
     引数なしで super() と書けるのは、 Pythonのコンパイラが裏側で
     自動的に 「今いるクラス（__class__）」 と 「現在のインスタンス（self）」 を
     こっそり代理人に渡してくれているからです（魔法のクロージャー参照）
。
だからこそ、メソッドの外の適当な場所で単に super() と実行しようとすると
 「誰の代理人になればいいか分からない！（no arguments）」 とエラーを吐くのです。
 
●第3部 辞書（ __dict__ ）の美しい分業体制
最後に、出力された辞書ログが証明しているアーキテクチャの真理をまとめます。
print(HetareBusinessPerson.__dict__)
     {'work': <function HetareBusinessPerson.work...>}
     dictとしては↑一応HBPクラスに登録されている。
➔ その通りです！ 「上書き」 であれ 「付け足し」 であれ、子クラスに def work: と
    書いた時点で、それは独自の工具として子クラスの金庫に登録されます。
print(hbp.__dict__) {'firstname': '太郎', 'lastname': '山田'}
➔ ここが最も美しいポイントです。 hbp は HetareBusinessPerson の実体ですが、
その親の BusinessPerson、さらに親の Person と3世代にわたる継承を受けています。 
しかし、hbp が誕生した瞬間に Person の __init__ が実行された結果、
実体である hbp 個人の金庫（__dict__）に入っているのは、純粋なデータである
 「名前」 だけです。
 
■ まとめ
super() の役割: 完全に機能を上書きしてしまうのではなく、親クラスのメソッドを
         「部品」 として呼び出し、前後に独自の処理を「付け足す」ための強力な魔法。
super の正体: 実は関数ではなく、MRO（メソッド解決順序）というルールに則って
        正しく親を探し出すための 「代理人（プロキシ）オブジェクトを生成するクラス」 である。
辞書の真理: 3世代継承しようとも、メソッドはそれぞれの 「クラスの辞書」 に
        分散保管され、「個人の辞書」 にはデータ（変数）だけがシンプルに格納される。
'''
r'''◆さらに詳しくsuper()の正体について
第1部：【真理】 super クラスの本来の姿（定義）
私たちが普段 super() と引数なしで使っているものは「超・省略形」です。 実際の super クラスの初期化メソッド（__init__）は、内部的に以下のような2つの引数を受け取るように定義されています。
■ super クラスの内部定義（擬似コード）
class super:
    def __init__(self, current_class, instance):
        # 第1引数：今自分がいるクラス（例：HetareBusinessPerson）
        self.current_class = current_class
        # 第2引数：実際の呼び出し元の実体（例：hbp）
        self.instance = instance
つまり、代理人（プロキシ）として正しく機能するためには、**「私は今どのクラスの設計図の中にいるのか（現在地）」と「誰の代わりに仕事をするのか（依頼主）」**という2つの絶対的なコンテキストが必要なのです。
第2部：【解剖】 引数なし super() に隠されたコンパイラの魔法
では、なぜ私たちは引数なしの super() だけで済んでいるのでしょうか？ 公式ドキュメントには、この魔法の種明かしが次のように書かれています。
「__class__ は、メソッドが __class__ または super のいずれかを参照している場合に、コンパイラによって作成される暗黙のクロージャー参照です。これにより (...) super() の無引数形式がレキシカルスコープに基づいて定義されているクラスを正確に識別することを可能にします」
■ 現場監督（コンパイラ）のスローモーション
プログラマ がコードに super().work() と書いた。
コンパイラ：「おっ、引数なしの super() だな！ 開発者にいちいち自分のクラス名や self を書かせるのはDRY原則に反するから、俺が裏でこっそり書き換えてやろう！」
コンパイラ（魔法の発動）：「このコードは HetareBusinessPerson クラスの中で書かれているな。よし、第一引数には隠し変数の __class__ を、第二引数にはメソッドの第一引数である self をこっそり渡して、super(__class__, self).work() というコードに強制変換しろ！」
これが、メソッド外で super() を実行すると「誰の代理人になればいいか分からない！（no arguments）」とエラーになる理由の完全な裏付けです。
第3部：【アーキテクチャ】 代理人の仕事＝MRO（ルーティングテーブル）の走査
無事に super(HetareBusinessPerson, hbp) として誕生した代理人オブジェクトは、次に .work() と呼ばれた時、どうやって親の辞書から正しい work を探してくるのでしょうか？
ここで昨日学習した**「MRO（メソッド解決順序）」**のリストが火を噴きます。
■ 代理人（superインスタンス）の思考回路（擬似コード）
    def __getattr__(self, method_name):  # method_name には 'work' が入る
        # 1. 依頼主（hbp）の完全な家系図（MROリスト）を取得する
        mro_list = type(self.instance).__mro__
        # 例：(Hetare, BusinessPerson, Person, object)

        # 2. 家系図の中で、現在地（Hetare）がどこにいるかを探す
        current_index = mro_list.index(self.current_class)  # ➔ 0番目

        # 3. 現在地の「次（1番目）」のクラスから順番に、親の辞書を探しに行く！
        for parent_class in mro_list[current_index + 1 :]:
            if method_name in parent_class.__dict__:
                # 発見！親の辞書のメソッドを、依頼主(hbp)の代わりに実行できるようにして返す
                return 実行可能なメソッド
        
        # どこにも無ければエラー
        raise AttributeError
この 「自分の現在地をMROリストから探し出し、その『次（Next-Hop）』から探索を再開する」 というのが super の内部アルゴリズムの絶対的な真理です
。
だからこそ、多重継承のダイアモンド構造という複雑なネットワークの中にあっても、現場監督はルーティングループを起こすことなく、安全に次の親戚のメソッドを呼び出すことができるのです。
■ 参謀からの総括（インフラ的メタファー）
super の内部定義をインフラエンジニアの視点に翻訳すると、以下のようになります。
super クラスの実態: BGPの「Next-Hop（ネクストホップ）」を計算するためのルーティング計算エンジンである。
引数なし super(): 「現在の自ルーターのAS番号（__class__）」と「送信元パケット（self）」を自動で検知して計算エンジンに渡す、最強のマクロ機能である。
探索のアルゴリズム: AS-PATH（MROリスト）を参照し、自分自身のASの**「次のAS」**に対してパケット（メソッド呼び出し）を転送する仕組みである。
単なる「親を呼ぶ関数」だと思っていたものの正体が、実は**「コンパイラによる引数の自動補完」と「MROリストを使った高度な経路探索プロキシ」**の合わせ技であったという真理。
'''
#%%　初期化 ﾒｿｯﾄﾞのオーバーライド super().__init__
class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    def show(self):
        print(f'私の名前は{self.lastname}{self.firstname}です！')
class Foreigner(Person):
    def __init__(self, firstname, middlename, lastname):
        super().__init__(firstname, lastname)
        self.middlename = middlename
    def show(self):
        print(f'私の名前は{self.lastname}・{self.middlename}・\
{self.firstname}です！')
if __name__=='__main__':
    fr = Foreigner('太郎','ヨーダ ', '山田')
    fr.show()
    #私の名前は山田・ヨーダ ・太郎です！
    print(Foreigner.__dict__)
    #{'__module__': '__main__', '__init__': <function Foreigner.__init__ at 0x0000027D8F301800>,
    #'show': <function Foreigner.show at 0x0000027D8F3019E0>, '__doc__': None}

r'''
公式ドキュメントにも「基底クラスとその派生クラスがともに __init__() メソッドを持つ場合、派生クラスの __init__() メソッドは基底クラスの __init__() メソッドを明示的に呼び出して、インスタンスの基底クラス部分が適切に初期化されること保証しなければなりません
」と絶対ルールが記されています。
このコードで現場監督（システム）がどのように動いているのか、そしてなぜこの書き方がインフラ自動化設計において「最強」なのか、完全に解剖いたします！
第1部：【真理】 初期化における super().__init__ の絶大な価値
子クラスである Foreigner にも __init__ を書いたため、親クラス（Person）の __init__ は完全に隠蔽（オーバーライド）されました。
もしここで super().__init__ を使わなかったらどうなるでしょうか？
class Foreigner(Person):
    def __init__(self, firstname, middlename, lastname):
        # ❌ 親の機能を無視して、全部自分で書き直す（最悪の設計）
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
これでも動きます。しかし、これは「DRY原則（Don't Repeat Yourself：同じコードを二度書くな）」に完全に反しています。もし将来、親クラスである Person の仕様が変わり、「性別の変数も追加しよう」となったとき、子クラスの Foreigner のコードもいちいち書き直さなければならなくなります。
これを防ぐのが、昌敏さんが書かれた 「親の初期化処理の再利用」 です。
第2部：【解剖】 現場監督のスローモーション（インスタンス化の瞬間）
fr = Foreigner('太郎','ヨーダ ', '山田') が実行された瞬間、裏側では極めて美しいパス回しが行われています。
■ 現場監督のスローモーション
現場監督：「Foreigner の実体（箱）を作れだな！ よし、箱（fr）を用意したぞ。次は初期データの投入だ！ Foreigner の辞書にある __init__ を起動しろ！」
現場監督：「Foreigner の __init__ に入ったぞ。最初の命令は…… super().__init__(firstname, lastname) だな！」
現場監督（代理人の派遣）：「俺の代理人（super）よ、親クラスである Person の金庫へ行って __init__ を実行してこい！ その際、荷物（'太郎' と '山田'）と、今作っている実体（fr）も一緒に持っていけ！」
現場監督（親の処理）：「Person の __init__ が実行された！ 実体（fr）の個人辞書に firstname: '太郎' と lastname: '山田' が書き込まれたぞ！」
現場監督（子の処理へ復帰）：「親の処理が終わったな。じゃあ Foreigner の __init__ に戻って続きだ！ self.middlename = middlename を実行して、実体の個人辞書に middlename: 'ヨーダ ' を追加して作業完了だ！」
このように、「共通のデータ（姓名）は親にセットさせ、自分専用のデータ（ミドルネーム）だけ自分でセットする」という見事な分業体制が敷かれているのです。
第3部：【証明】 Foreigner.__dict__ が語るオーバーライドの事実
print(Foreigner.__dict__) {'__init__': <function Foreigner.__init__ ...>, 'show': <function Foreigner.show ...>}
出力されたクラスの辞書が、これまでの真理を物理的に証明しています。 Foreigner クラスの金庫には、昌敏さんが新しく書き直した独自の __init__ と show だけがキッチリ登録されています。
この結果、現場監督は以下のように動きます。
実体の誕生時: Foreigner の辞書にある独自の __init__ が最優先で呼ばれ、その中から super() で親が呼ばれる。
fr.show() 実行時: Foreigner の辞書にある独自の show が見つかるため、親の show は完全に無視（オーバーライド）され、ミドルネーム入りの豪華な挨拶が出力される。
■ 参謀からのまとめ
クラス変数の継承: 自動で引き継がれる。
メソッドの継承: 書かなければ親のものを自動で借りてくる。同じ名前を書けば上書き（オーバーライド）される。
初期化（__init__）の拡張: 全てを上書きするのではなく、super().__init__ に共通の引数を渡して親に下請け作業を任せ、その後に自分専用の初期化処理を付け足すのが、Pythonにおけるクラス設計の「黄金パターン」である。
'''
#%% 10.3.4 多重継承とﾒｿｯﾄﾞの検索順序
class Top:
    def hoge(self):
        print('TopA')
class MiddleA(Top):
    def hoge(self):
        print('MiddleA')
class MiddleB(Top):
    def hoge(self):
        print('MiddleB')
class Low(MiddleA, MiddleB):
    pass
if __name__=='__main__':
    l = Low()
    l.hoge()
    #MiddleA
    print(Low.hoge)
    #<function MiddleA.hoge at 0x0000027D8F3018A0>
    print(Low.__mro__)
    #(<class '__main__.Low'>, <class '__main__.MiddleA'>,
    #<class '__main__.MiddleB'>, <class '__main__.Top'>, <class 'object'>)
r'''
出力結果が MiddleA になるのは、決して偶然ではありません。 Pythonの現場監督（システム）が、複雑な継承関係の中で「どの親の工具（メソッド）を優先して使うか」を厳密に定めた絶対ルールに従って動いた結果です。
このコードで起きている「ダイアモンド継承」と「MROの真理」について、現場監督のスローモーションで完全に解剖いたします！
第1部：【解剖】 現場監督のスローモーション（ l.hoge() 実行時）
Low クラスは class Low(MiddleA, MiddleB): と定義されており、2つの親クラスを同時に継承しています。
■ 現場監督のスローモーション
現場監督：「実体 l の hoge() を実行しろだな！ まずは実体の個人の辞書（l.__dict__）、そして金型の辞書（Low.__dict__）を探すぞ……両方とも無いな！」
現場監督：「よし、Low は MiddleA と MiddleB を継承している！ ここで MRO（メソッド解決順序） のルール発動だ！」
現場監督：「Pythonの絶対ルールとして、多重継承の際は『左から右へ』の順番で親を探す！ つまり、左側に書かれている MiddleA の辞書を最初に探しに行け！」
現場監督：「おっ、MiddleA の辞書の中に hoge という工具を発見したぞ！ 右側の MiddleB や、大元の Top にも同じ工具があるようだが、1つ見つかった時点で捜索は打ち切りだ！ この MiddleA の hoge を実行しろ！」
このように、クラス定義の括弧の中に書かれた順番（今回は左側の MiddleA）が最優先されるため、出力が MiddleA となったのです
。
第2部：【真理】 ダイアモンド継承と「C3線形化」の魔法
今回のコードの継承関係をインフラのネットワーク図のように図解すると、見事な「ひし形（ダイアモンド）」の形になります。
Low は MiddleA と MiddleB を継承。
その MiddleA と MiddleB は、どちらも大元の Top を継承。
公式ドキュメントによると、このような「ダイアモンド継承」が発生した場合、昔の単純なルール（深さ優先探索など）では「Low ➔ MiddleA ➔ Top ➔ MiddleB」のように、末端の MiddleB よりも先に大元の Top が検索されてしまうという設計上の不具合が起きていました
。
これを解決するため、現在のPythonは 「C3メソッド解決順序（C3 MRO）」 という非常に賢いルーティングアルゴリズムを採用しています
。 このアルゴリズムは、「左側の親を優先しつつも、共通の祖先（Top）は一番最後に1回だけ検索する」 という矛盾のない一本道（線形化）の検索ルートを全自動で構築してくれます
。
これにより、現場監督の検索ルートは以下の順序に確定します。 Low ➔ MiddleA ➔ MiddleB ➔ Top ➔ object（究極の親方）
第3部：【Next Action】 __mro__ で検索ルートを可視化する
インフラエンジニアが traceroute コマンドでパケットの経路を確認するように、Pythonでもクラスが「どの順番で親を探しに行くか」の経路を完全に可視化するコマンドがあります。
ぜひ、昌敏さんのコードの最後に以下の1行を付け足して実行してみてください。
print(Low.__mro__)
出力結果として、現場監督がたどる辞書の検索ルート（タプル）が生々しく表示されるはずです。
■ 参謀からのまとめ
多重継承の優先順位: class 子(親1, 親2): と書いた場合、左側に書かれた親（親1）の辞書が優先して検索される
。
ダイアモンド継承: 複数の親が同じ大元の祖先を持っている複雑な継承関係のこと
。
MRO（メソッド解決順序）: 現場監督が迷子にならないよう、Pythonが裏側で自動構築する「矛盾のない一本道の辞書検索ルート（C3線形化）」
。
'''
#%% もう少しだけ複雑な多重継承の場合
class TopA:
    def hoge(self):
        print('TopA')
class TopB:
    def hoge(self):
        print('TopB')        
class MiddleA(TopA,TopB):
    def hoge(self):
        print('MiddleA')
# class MiddleB(TopB,TopA):
#     def hoge(self):
#         print('MiddleB')
    #このままでは↓のエラーが出る。
    #TypeError: Cannot create a consistent method resolution
    #order (MRO) for bases TopA, TopB
    #↑一貫性のある順序）が作れない！！
class MiddleB(TopA,TopB):
    def hoge(self):
        print('MiddleB')        
class Low(MiddleA, MiddleB):
# class Low(MiddleB, MiddleA):だと、
#MiddleB
#<function MiddleB.hoge at 0x0000027D8F2DFB00>
#(<class '__main__.Low'>, <class '__main__.MiddleB'>,
# <class '__main__.MiddleA'>, <class '__main__.TopA'>,
# <class '__main__.TopB'>, <class 'object'>)
    pass
if __name__=='__main__':
    l = Low()
    l.hoge()
    #MiddleA
    print(Low.hoge)
    #<function MiddleA.hoge at 0x0000027D8F302980>
    print(Low.__mro__)
    #(<class '__main__.Low'>, <class '__main__.MiddleA'>,
    #<class '__main__.MiddleB'>, <class '__main__.TopA'>,
    #<class '__main__.TopB'>, <class 'object'>)
r'''
TypeError: Cannot create a consistent method resolution order (MRO) というエラー。これこそが、Pythonが複雑なシステムを構築する際に「絶対にバグを起こさせないための最強の安全装置（フェイルセーフ）」が作動した決定的な証拠です。
この複雑な階層の中で、現場監督（システム）がどのように「矛盾」を検知し、どのようにして安全な「一本道の検索ルート（MRO）」を構築したのか。完全に解剖いたします！
第1部：【解剖】 なぜ MiddleB(TopB, TopA) はクラッシュしたのか？
まずは、コメントアウトされているエラーの震源地を解剖します。 もし MiddleA(TopA, TopB) としつつ、MiddleB(TopB, TopA) と書いてしまった場合、現場監督はどう動くでしょうか。
■ 現場監督のスローモーション（クラス定義のパース時）
現場監督：「MiddleA の定義だな！ ここでは TopA が左、TopB が右だから、**『絶対に TopA を TopB よりも先に検索しろ』**というルールAが成立した！」
現場監督：「次は MiddleB の定義だ！ ここでは TopB が左、TopA が右だから、**『絶対に TopB を TopA よりも先に検索しろ』**というルールBが成立した！」
現場監督：「最後に大元となる Low(MiddleA, MiddleB) の定義だ！ よし、全員のルールを合体させて一本道の検索ルートを作るぞ！」
現場監督：「……おい待て！！！ ルールAは『TopAが先』、ルールBは『TopBが先』だぞ！ 『どちらを優先すればいいか矛盾していて一本道（一貫性のある順序）が作れない！！（Cannot create a consistent method resolution order）』 強制終了だ！！」
PythonのMRO（C3線形化アルゴリズム）は、「親クラスで指定された左から右への優先順位のルールを、子クラスで絶対に崩してはいけない（単調性の維持）」 という絶対的な設計思想を持っています
。だからこそ、親クラス間で矛盾した順序を指定すると、システムが破綻する前に安全装置が働いてくれるのです
。
第2部：【真理】 修正後のMROが導き出したルーティング
昌敏さんはこの矛盾に気づき、見事に MiddleB(TopA, TopB) と順序を揃えて修正されました。これにより矛盾が解消され、現場監督は以下の完璧なルート（ print(Low.__mro__) の出力）を構築しました。
(<class '__main__.Low'>, <class '__main__.MiddleA'>, <class '__main__.MiddleB'>, <class '__main__.TopA'>, <class '__main__.TopB'>, <class 'object'>)
なぜこの順番になったのか、MROの構築ルール
に従って現場監督の思考を追います。
Low： まずは自分自身の辞書を探す。
MiddleA： 自分に無ければ、括弧内の左側に指定した親（MiddleA）を探す。
MiddleB： MiddleA の次は、その親である TopA に行きそうになるが、ここでC3アルゴリズムが発動！ TopA は右側の親（MiddleB）にとっても親（共通祖先）であるため、**「共通の祖先は後回しにする」**というルールに基づき、先に右側の親である MiddleB を検索する
。
TopA： Middle 層の検索が全て終わったので、ここでようやく祖先層へ進み、ルール通り左側である TopA を検索する。
TopB： 次に右側の TopB を検索する。
object： 最後にすべてのクラスの究極の親方である object を検索する。
第3部：【証明】 l.hoge() が MiddleA になる理由
構築されたMROのルートさえ可視化してしまえば、実行結果は火を見るより明らかです。
■ 現場監督のスローモーション（ l.hoge() 実行時）
現場監督：「実体 l から hoge を探せ！ 個人の辞書、そして Low の辞書には無い！」
現場監督：「MROに従い、次は MiddleA の辞書を探せ！」
現場監督：「おっ！ MiddleA の辞書に hoge が見つかったぞ！ MROリストの後ろにいる MiddleB や TopA のことはもう知らん！ この MiddleA の hoge を実行だ！」
昌敏さんがコメントに追記されている通り、もし class Low(MiddleB, MiddleA): と左と右を入れ替えて定義したならば、MROの2番目に MiddleB が来るため、結果は見事に MiddleB へと変化します
。
■ 参謀からのまとめ
Inconsistent MROエラーの真理: 多重継承において、複数の親クラス間で「祖先クラスの優先順位（左と右）」が矛盾していると、Pythonは安全装置を発動させてシステムを止める。
C3線形化の魔法: 左側を優先しつつも、ダイアモンド継承（共通の祖先）を持つ場合は、「サブクラス（Middle層）をすべて調べ終わるまで、共通祖先（Top層）の検索を後回しにする」ことで、意図しない古いメソッドの呼び出しを防いでいる
。
インフラで例えるならば、「OSPFやBGPのようなルーティングプロトコルが、ルーティングループ（矛盾）を検知してパケットを破棄した（TypeError）後、正しいメトリック（MRO）を設定し直すことで、最短かつ安全なパケットの通り道を全自動で確立した」 のと全く同じ構造です。
'''
#%%　継承ツリーが異なる場合
# ※本当はメソッド名が重複するような多重継承は極力避けるべきとのこと。
#●↑具体的にはそれが避けられない事態とはどんな時？
      #   Top
      #    |
      # MiddleA    MiddleB
      #    |__________|
      #          |
      #         Low
class TopA:
    def hoge(self):
        print('TopA')       
class MiddleA(Top):
    def hoge(self):
        print('MiddleA')
class MiddleB:
    def hoge(self):
        print('MiddleB')        
class Low(MiddleA, MiddleB):
    pass
if __name__=='__main__':
    l = Low()
    l.hoge()
    #MiddleA
    print(Low.hoge)
    #<function MiddleA.hoge at 0x0000027D8F2DEE80>
    print(Low.__mro__)
    #(<class '__main__.Low'>, <class '__main__.MiddleA'>,
    #<class '__main__.Top'>, <class '__main__.MiddleB'>, <class 'object'>)

r'''
「メソッド名が重複する多重継承が避けられない事態とは具体的にどんな時か？」**という極めて実務的な疑問について、インフラアーキテクトの視点で完全に解剖いたします！
第1部：【解剖】 ダイアモンド継承と独立ツリーの決定的な違い
前回の「ダイアモンド継承（MiddleAとMiddleBが両方ともTopを継承している状態）」では、現場監督は**「共通の祖先（Top）の検索は後回しにする」**という特別なC3アルゴリズムを発動させました。 ➔ Low ➔ MiddleA ➔ MiddleB ➔ Top
しかし今回のコードは、MiddleA だけが Top を継承し、MiddleB は何も継承していません（独立しています）。
■ 現場監督のスローモーション（ Low.__mro__ 構築時）
現場監督：「Low クラスのMROを作るぞ。まずは自分自身だ！」（➔ Low）
現場監督：「次は左側の親、MiddleA だな！」（➔ MiddleA）
現場監督：「さて、次はどうする？ MiddleA は Top を継承しているな。この Top は、右側の MiddleB にとっての親（共通祖先）か？……いや、違うな！ ならば『後回し』にする必要はない！ そのまま左側のツリーを上まで登り切れ！」（➔ Top）
現場監督：「左の家系図をたどり終えたぞ。じゃあ、右側の親である MiddleB を検索だ！」（➔ MiddleB）
現場監督：「最後に究極の親方だ！」（➔ object）
結果として、MROは Low ➔ MiddleA ➔ Top ➔ MiddleB ➔ object となり、「左側のツリーを深さ優先で登りきる」という動きに変化しました。昌敏さんの出力結果と完全に一致していますね！
第2部：【真理】 なぜメソッドの重複を避けるべきなのか？
さて、ここからが本題です。 なぜ、教科書では「メソッド名が重複するような多重継承は極力避けるべき」と警告されているのでしょうか？
それはまさに、今可視化されたこのMRO（ Top が MiddleB より先に来るという事実）が、予期せぬ「隠蔽バグ」を引き起こすからです。
もし、MiddleA の中身が空っぽ（pass）で、Top クラスと MiddleB クラスの両方に hoge メソッドが存在したとします。 昌敏さんが l.hoge() を呼んだ時、直感的には「すぐ親である MiddleB の hoge が呼ばれるだろう」と思うかもしれません。しかし実際には、はるか遠い先祖である Top の hoge が先にMROにヒットして実行されてしまい、MiddleB の hoge は永遠に無視されてしまうのです。
このように、「意図していない親戚のメソッドが勝手に実行されてしまう」ことを防ぐために、自作クラスではメソッド名がかぶらないように命名するのが鉄則とされています。
第3部：【実務】 メソッド名の重複が「避けられない事態」とは？
では、「メソッドの重複を避けられない事態」とは具体的にどんな時か？ それはズバリ、**「自分たちで作ったコードではなく、外部の巨大なライブラリ（フレームワーク）を複数組み合わせて多重継承しなければならない時」**です。
■ 避けられない事態の具体例 昌敏さんが、あるインフラ自動化のシステムを作っているとします。
左の親（MiddleA）： Web通信を処理する「サードパーティ製 WebHandler クラス」
右の親（MiddleB）： データベース接続を管理する「オープンソースの DBMixin クラス」
これらの便利機能を両方使いたくて、class MySystem(WebHandler, DBMixin): と多重継承しました。 しかし、両方のライブラリの開発者が、それぞれのクラスの中にたまたま setup() や close()、save() といった非常にありがちな名前のメソッドを定義していたらどうなるでしょうか？
昌敏さんは「DBのセットアップ」のつもりで self.setup() を呼んだのに、MROのルールによって「Webのセットアップ」が先に実行されてしまい、DBが初期化されずにシステムが謎のクラッシュを起こします。
外部のライブラリのソースコード（変数名やメソッド名）を勝手に書き換えることはできません。 だからこそ、そのような事態に遭遇したプロのPythonエンジニアは、**「__mro__ をプリントして、どのライブラリの setup() が優先されているかを可視化し、必要であれば super() を使わずに DBMixin.setup(self) のようにクラス名指しで直接呼び出して衝突を回避する」**という高度なアーキテクチャの制御を行うのです。
■ 参謀からのまとめ
MROの動的変化: 共通の祖先を持たない多重継承では、「左側の家系図」を最上部（Top）まで深さ優先で検索し終えてから、「右側の親」の検索に移る。
重複の恐怖: このMROの動きにより、遠い先祖のメソッドが、近い親の同名メソッドを「隠蔽（オーバーライド）」してしまう事故が起きやすい。
避けられない事態: 外部のライブラリ同士を多重継承した際、close() や save() などの一般的なメソッド名がバッティングしてしまった時。
'''


















    
    
    
        