# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:31:12 2026

@author: iot01
"""
#%%# 11.2 特殊メソッド 
#前後に2つのアンダースコア（ダブルアンダースコア、略して Dunder：ダンダー）を持つメソッド
# 11.2.1 オブジェクトの文字列表現を取得する __str__メソッド
# __str__メソッドはすべてのクラスで可能な限り実装するべきと言及
#→なぜなら、print(obj) とするだけで、 オブジェクトの概要を確認できるから。
class Person:
    def __init__(self, firstname, lastname):
        self.__firstname = firstname
        self.__lastname = lastname
    #↓インスタンスの文字列表現を生成
    def __str__(self):
        return f'{self.lastname} {self.firstname}'
    '''strメソッドには、 そのクラスを特徴づける情報＝インスタンス変数を選んで、文字列化する
    ※すべてのインスタンス変数を書き出す必要はない。
    また__str__で使用したインスタンス変数は個別のゲッターでも取得出来る様にすること
    例：ルーターなら"Router(IP: 192.168.1.1, Hostname: Tokyo-RT)" のように、
    「オブジェクトを特定するのに必要な最小限の情報」'''
    #↓propertyを定義
    @property
    def firstname(self):
        return self.__firstname
    @property
    def lastname(self):
        return self.__lastname
if __name__=='__main__' :
    p = Person('太郎','山田')
    print(p)
    #山田 太郎
    print(Person.__str__)
    # <function Person.__str__ at 0x00000181A49731A0>
    #↑クラスから実行するとfunction。 まだselfが誰か、実体が決まって無いのでただの関数
    print(p.__str__)
    #<bound method Person.__str__ of
    #<__main__.Person object at 0x00000181A4984F50>>
    #これは バウンドメソッド（束縛されたメソッド） だ
    print(p.__str__.__func__)
    #↑<function Person.__str__ at 0x00000181A4A0F1A0>
    #（Personクラスにある元の関数！）
    print(p.__str__.__self__)
    #山田 太郎
    print(p.__str__.__self__ is p)
    #True
    
    print(p.self)
    #AttributeError: 'Person' object has no attribute 'self'
    print(Person.self)
    #AttributeError: type object 'Person' has no attribute 'self'
    print(Person.__self__)
    #AttributeError: type object 'Person' has no attribute '__self__'
    print(p.__self__)
    #AttributeError: 'Person' object has no attribute '__self__'
    '''
    インスタンスメソッドオブジェクトが、インスタンスを介してユーザ定義関数オブジェクトを取り出すことで
    作成された場合、その __self__ 属性はインスタンスとなり、メソッドオブジェクトは
    束縛 (bound) されているといいます。
    '''
    
r'''◆第1部：【真理】 なぜ self はエラーになるのか？
print(p.self)
print(Person.self)
これらがエラーになる理由は、公式ドキュメント（9.4. いろいろな注意点）に明確な答えが書かれています。
「よく、メソッドの最初の引数を self と呼びます。この名前付けは単なる慣習でしかありません。 
self という名前は、 Python では何ら特殊な意味を持ちません。」
■ 現場監督の視点 self とは、関数を定義するときに人間が勝手につけた**
「ただの第1引数の名前（名札）」**に過ぎません。
Ciscoルーターに enable password が設定されているのに、router.password というコマンド
（属性）で直接中身が見られないのと同じです。 インスタンス p や クラス Person という金庫
（オブジェクト）の中には、self という名前のデータ（変数）はそもそも存在しないため、
現場監督は「そんな属性はない！（AttributeError）」と怒るのです。

第2部：【解剖】 なぜ __self__ はエラーになるのか？
print(Person.__self__)
print(p.__self__)
 __self__ という属性は確かに実在します。しかし、これらがエラーになったのは、
 **「__self__ を持っているのはインスタンスやクラスではないから」**です。
公式ドキュメント（3.2.8.2. インスタンスメソッド）にはこう書かれています。
「Instance method objects にも属性があります。 
m.__self__ はメソッド m() の属しているインスタンスオブジェクトで、
 m.__func__ はそのメソッドに対応する function object です。」
 ●補足：【参謀による超・意訳（アーキテクチャ解説）】 
 「インスタンスからドット（.）で取り出されたメソッド（バウンドメソッド）は、単なる処理の塊ではなく、
 **内部に2つの重要な参照ポインタを保持した『状態維持カプセル』**です。
__self__ ポインタ: 『この専用ボタンは誰のものか？』を忘れないために、操作対象となる実体
                （インスタンス）のメモリアドレスをがっちり掴んで離さない安全装置です。
__func__ ポインタ: 『このボタンを押したらどんな処理をするのか？』を知るために、**クラスに置かれている
                共通の操作マニュアル（元の関数）**を指し示すショートカットリンクです。
■ 現場監督の視点 __self__ を持っているのは、インスタンス p ではなく、p から取り出された
「バウンドメソッド（メソッドオブジェクト）」の中なのです！
第3部：【証明】 真の __self__ を暴き出すコード
では、どうすれば __self__ を画面に表示できるのか？ ドット（.）の左側を、インスタンス（p）ではなく、
**メソッド（p.__str__）**にしてあげればよいのです。
お手元のコードの末尾に、以下の3行を書き加えて実行してみてください。
# 1. メソッドオブジェクトの中にある __self__ を覗き見る
print(p.__str__.__self__)
# 出力: <__main__.Person object at 0x...> （つまり p 自身！）

# 2. メソッドオブジェクトの中にある __func__ (元の関数) を覗き見る
print(p.__str__.__func__)
# 出力: <function Person.__str__ at 0x...> （Personクラスにある元の関数！）

# 3. p.__str__.__self__ が、本当に p と同一人物か（メモリアドレスが同じか）証明する
print(p.__str__.__self__ is p)
# 出力: True
■ 参謀からのまとめ：バウンドメソッドの正体
現場監督は、p.__str__ とドットでアクセスされた瞬間、
裏側でこっそり 「メソッドオブジェクト」という新しいカプセル を作っていました。 
そのカプセルの中身は、以下の2つのパーツがガチャンと結合（バインド）されたものです。
__func__ ＝ クラスが持っている「共通の操作マニュアル（関数）」
__self__ ＝ 操作の対象となる「私自身（インスタンス p）」
だからこそ、p.__str__() とカッコの中に何も引数を入れなくても、
現場監督はカプセルの中に入っている __self__（つまり p）を取り出して、
自動的に第1引数として渡してくれていたのです。

●補足：インタプリターは、ドット（.）でアクセスしたその瞬間（実行時）」に、毎回リアルタイムで
カプセル（メソッドオブジェクト）を動的生成している。
＊マニュアル（関数）の実体は、クラス（設計図）の場所に1つだけ置いておく。
＊インスタンスは自分専用の「データ（変数）」だけを持つ。
＊プログラマーがメソッドを呼び出そうとした（アクセスした）瞬間にだけ、
  一時的なカプセル（メソッドオブジェクト）を作って対応する。
'''
    
#%% 解析可能な表現を取得する　__repr__メソッド repr関数 eval関数
#元のオブジェクトを復元できる様な文字列がリターンされることが期待される __repr__
class Person:
    def __init__(self, firstname, lastname):
        self.__firstname = firstname
        self.__lastname = lastname
    #↓インスタンスの文字列表現を生成
    def __str__(self):
        return f'{self.lastname} {self.firstname}'
    #●↓__repr__メソッドを追加
    def __repr__(self):
        return f"Person({self.lastname!r}, {self.firstname!r})"
    #↓propertyを定義
    @property
    def firstname(self):
        return self.__firstname
    @property
    def lastname(self):
        return self.__lastname
if __name__=='__main__' :
    p = Person('太郎','山田')
    print(p)
    #↑山田 太郎
    print(Person.__str__)
    #↑<function Person.__str__ at 0x00000181A4A0D8A0>
    print(p.__str__)
    #↑<bound method Person.__str__ of Person('山田', '太郎')>
    print(Person.__str__())
    #TypeError: Person.__str__() missing 1 required positional argument: 'self'
    print(p.__str__())
    #山田 太郎
    print(Person.__repr__)
    #↑<function Person.__repr__ at 0x00000181A4973920>
    print(p.__repr__)
    #↑<bound method Person.__repr__ of Person('山田', '太郎')>
    
    #↓__eq__メソッドを実装せずに同値判定をした場合
    p1 = Person('太郎', '山田')
    p2 = Person('次郎','鈴木')
    p3 = Person('太郎', '山田')
    print(p1==p2) #False
    print(p1==p3) #False
    print(p1.__dict__==p3.__dict__) #True
    #↑★オブジェクト同士が同じが（is判定？）どうかで判定してしまっているのでFalse

r'''◆ __str__ と __repr__の違い
第1部：【解剖】 __str__ の真理（人間向け）
公式ドキュメントでは、__str__ について以下のように定義されています。
「str(object) や組み込み関数 print() によって呼び出され、
オブジェクトの『非公式の (informal)』または分かりやすく印字可能な文字列表現を計算します」
 「__str__() が有効な Python 表現を返すことが期待されないという点で、
 このメソッドは object.__repr__() とは異なります。
 より便利な、または簡潔な表現を使用することができます」
目的: 一般の人が画面を見たときに「なるほど」と理解しやすくすること。
トリガー: print(p) や str(p) を実行したとき
。
コードの例: return f'{self.lastname} {self.firstname}'
 ➔ 「山田 太郎」という、人間にとって自然な名前の文字列。
 
第2部：【解剖】 __repr__ の真理（開発者向け・デバッグ用）
一方、__repr__ については、公式ドキュメントで以下のように極めて厳密な定義がなされています。
「repr() 組み込み関数によって呼び出され、オブジェクトを表す『公式の (official)』文字列
を計算します。可能なら、これは (適切な環境が与えられれば) 同じ値のオブジェクトを再生成するのに
使える、有効な Python 式のようなものであるべきです」
 「典型的にはデバッグに利用されるため、情報が豊富で曖昧さがない表現であることが重要です」
目的: 開発者がデバッグ中に変数の中身を覗いたとき、「それがどんなクラスから、どんな引数を渡されて
作られたオブジェクトなのか」を1ミリの曖昧さもなく把握し、可能であればそのままコピー＆ペーストして
 eval() で実行すれば、クローン（全く同じオブジェクト）を復元・再生成できるようにすること
。
トリガー: repr(p) を実行したときや、Jupyter・対話モードで変数名 p だけを打ってEnterを押したとき。
    エラーのトレースバックが表示されるときにもこちらが使われます。
コードの例: return f"Person({self.lastname}, {self.firstname})" 
    ➔ 「これは Person クラスのインスタンスですよ」というシステムの内部構造が丸見えになっています。
    
第3部：現場監督（システム）のフォールバック機能
実は、現場監督はこれら2つのメソッドについて「ある特別な掟」を持っています。
もし、クラスに __repr__ しか定義しなかったとします。 その状態で print(p)を実行するとどうなるでしょうか？
公式ドキュメントにはこう書かれています。
「クラスが __repr__() を定義していて __str__() は定義していなければ、
そのクラスのインスタンスの『非公式の (informal)』文字列表現が要求されたときにも 
__repr__() が使われます」
■ 現場監督のスローモーション 「おい！ print(p) 命令が来たぞ！ p の中にある人間用の報告書
                    （ __str__ ）を出せ！」 
➔ 「現場監督、このクラスには __str__ が用意されていません！」 
➔ 「なんだと！？ しょうがない、開発者用の設計図（ __repr__ ）で代用して画面に出力しておけ！」
つまり、__repr__ は __str__ のバックアップ（フォールバック）としても機能します。
そのため、実務では「まずは __repr__ を必ず実装し、さらにエンドユーザー向けに綺麗にフォーマットしたい
場合のみ __str__ を追加で実装する」というのがオブジェクト指向のベストプラクティスとされています。
💡 Next Action
 __repr__ の実装（ return f"Person({self.lastname}, {self.firstname})" ）
ここで、インフラアーキテクトとして「完全にシステムを復元できる公式文字列」にするための、もう一段階上の
ハッカー・テクニックをご紹介します。
現状の出力は Person(山田, 太郎) となりますが、これをそのまま Python のプログラムとしてコピペして
実行しようとすると、山田 と 太郎 にクォーテーション（'）が付いていないため、
文字列ではなく「変数名」として解釈されてしまいエラーになります。
これを完全に有効な Python 式（文字列リテラル）にするには、
以前学習した f-string の **!r（repr変換）**プレフィックスを使います。
    def __repr__(self):
        # !r をつけることで、文字列に自動的にクォーテーションが付きます
        return f"Person({self.firstname!r}, {self.lastname!r})"
こうすると、出力は Person('太郎', '山田') となり、これをそのまま eval() に突っ込めば
完璧にオブジェクトが復活します（※引数の順番も __init__ の firstname, lastname の
順に合わせると完璧です）。
__str__ は「人間にとっての分かりやすさ」
__repr__ は「システムにとっての厳密さ・復元可能性」
'''

r'''◆なぜ __eq__ を上書きする前でも p1.__dict__ == p3.__dict__ が True になるのか
第1部：【真理】 __dict__ の正体と中身
インスタンスオブジェクトは、自分自身の状態を保存するために、
裏側に「専用の金庫（インスタンス辞書：instance dictionary）」を持っています
。その金庫の実体が __dict__ 属性です
 p1 と p3 を生成した時点での、それぞれの金庫の中身を見てみましょう。
p1.__dict__ の中身: {'firstname': '太郎', 'lastname': '山田'}
p3.__dict__ の中身: {'firstname': '太郎', 'lastname': '山田'}
どちらも文字列（str 型）を値として持つ、単純な辞書データになっています。

第2部：【解剖】 辞書（dict）における「等しい（==）」の掟
オブジェクト指向の「神なる始祖（組み込み型 object）」は、「等しいか？
（等価演算子：equality operator）」と聞かれたとき、「メモリの住所（同一性：identity）が
同じか？」で判定するデフォルトマニュアルを持っていました
。だから単なる p1 == p3 は False になります
。
しかし、比較対象が「辞書（マッピング型：mapping type）」になった瞬間、
現場監督はオブジェクト用のマニュアルを捨てて、辞書専用の判定マニュアルに切り替えます。 
公式ドキュメントには、辞書の比較ルールについて次のように明確に定義されています。
「マッピング (dict のインスタンス) の比較の結果が等価となるのは、同じ (key, value) を
持っているときかつそのときに限ります」
■ 現場監督（インタプリタ）のスローモーション
現場監督：「p1.__dict__ == p3.__dict__ という比較命令だな！ 
今比較しているのは Person オブジェクトではなく、単なる辞書（dict）同士だぞ！」
現場監督：「辞書の審査ルール（マッピング型の等価比較：
equality comparison for mapping types）を発動しろ！
 メモリの住所（同一性：identity）が別々の金庫であっても構わない！ 
 中に入っている『名札と中身のペア（キーと値のペア：key-value pairs）』が全て一致しているか確認しろ！」
現場監督：「左の金庫も右の金庫も、firstname が '太郎' で、lastname が '山田' だな！
中身（値：value）が完全に一致している！ よって合格（True）だ！」

第3部：【実務】 Pythonが用意している「ショートカット」
実は、この疑問から直感で書いた p1.__dict__ == p3.__dict__ という比較は、
実務においても**「すべてのインスタンス変数が一致しているかを手っ取り早く判定するハッカー・テクニック」**
として使われます。
もし Person クラスに年齢や部署、役職など数十個のデータ
（インスタンス変数：instance variables）があった場合、自分で __eq__ の中に
 self.firstname == other.firstname and self.lastname == ... と
 全部列挙するのは大変ですよね。
そんなとき、独自ルール（特殊メソッド：special method）である __eq__ を次のように上書き
（オーバーライド：override）すると、非常にスマートで保守性の高い設計になります。
def __eq__(self, other):
    if isinstance(other, Person):
        # 自分の金庫（__dict__）と相手の金庫を丸ごと辞書比較させる
        return self.__dict__ == other.__dict__
    return False
■ まとめ
p1 == p3 ➔ 「箱（インスタンス：instance）」 同士の比較。
デフォルトでは「住所（同一性：identity）」を見るため False
。
p1.__dict__ == p3.__dict__ 
➔ 「箱の中の辞書（インスタンス辞書：instance dictionary）」 同士の比較。
辞書のルールでは「中身（同値性：equality）」を見るため True
。
'''

#%% 11.2.2 オブジェクト同士が等しいかどうかを判定する __eq__メソッド
class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    
    #↓氏、 名、 共に等しければ同値とする
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.firstname == other.firstname and \
                self.lastname == other.lastname
        return False
if __name__=='__main__'    :
    p1 = Person('太郎', '山田')
    p2 = Person('次郎','鈴木')
    p3 = Person('太郎', '山田')
    print(p1==p2) #False
    print(p1==p3) #True
    print(p1.__dict__==p3.__dict__) #True
r'''
◆第1部：【真理】 __eq__ を実装しない場合の「==」の正体
Pythonにおけるすべての設計図（クラス：class）は、明示しなくても暗黙のうちに
「神なる始祖の設計図」（object 組み込み型）を引き継いでいます（継承：inheritance）
。 この object クラスには、最初から == （等価演算子：equality operator）が
使われたときのデフォルトの動作マニュアル（デフォルト実装：default implementation）
が定義されています
。
公式ドキュメント（3.3.1. 基本的なカスタマイズ）には、このデフォルトの動作について以下のように
明確に書かれています。
「デフォルトでは、object は is を使って __eq__() を実装しています
（True if x is y else NotImplemented）」
現場監督（インタプリタ）のスローモーション
p1 == p3 と書いた瞬間、現場監督は p1 の中にある比較マニュアル（__eq__ メソッド）を
探します
。
独自の __eq__ が無い場合、現場監督は始祖から受け継いだデフォルトマニュアルを使います。
そのデフォルトマニュアルには、「中身のデータ（値：value）はどうでもいい。
二つの箱（インスタンスオブジェクト：instance object）が、
メモリ上の完全に同じ住所（同一性：identity）を指しているか
（is 演算子）だけで判定しろ！」と書かれています
。
p1 と p3 は、それぞれ別々に作られた独立した箱（別々のインスタンス：instances）であり、
メモリ上の住所が違うため、中身が同じ「山田太郎」であっても無情に False と判定されるのです。

第2部：【解剖】 __eq__ メソッドによる「掟」の上書き
この「住所が違えば別人」というデフォルトのルールを、「住所が違っても、
中身のデータ（属性：attributes）が同じなら同一人物とみなす（同値性：equality）」と
いうルールに書き換える作業が、今回のコード後半部分です。
現場監督（インタプリタ）のスローモーション

独自クラス内に __eq__ という特別な直通ダイヤル
（特殊メソッド：special method、またはダンダーメソッド：dunder method）を設置しました
。これにより、始祖のルールが上書き（オーバーライド：override）されます。
p1 == p3 が実行されると、現場監督は裏側でこっそりと p1.__eq__(p3)
 という呼び出し（メソッド実行：method invocation）に自動変換します
。
引数 self には p1 自身が、引数 other には比較相手である p3 が代入
（束縛：binding）されます。
メソッド内では、まず isinstance(other, Person) で「比較相手の p3 が、
本当に Person の金型（クラス：class）から作られた仲間か？
（型チェック/サブクラスチェック：type checking / subclass check）」を確認します
。
仲間であれば、お互いの「名」と「姓」（インスタンス変数：instance variables あるいは
 データ属性：data attributes）同士を == で個別に比較し、両方一致していれば
 True を返す、という独自の審査基準が適用されます。
 
第3部：【実務】 なぜ最初から中身を比較してくれないのか？
「なぜPythonは、最初から親切に中身（インスタンス変数）を比較してくれないのか？」と
疑問に思うかもしれません。 これには、Pythonの極めて合理的な設計思想があります。
Pythonの現場監督（インタプリタ）は、「そのオブジェクトがどういう性質のものか」を勝手に
深読みしません。 たとえば、独自の「社員クラス」を作ったとき、「社員番号が同じなら
他が違っても同じとみなす」のか、「部署も名前もすべて一致して初めて同じとみなす」のか、
あるいは「大文字小文字を無視して同じとみなす」のか。それは、設計図（クラス：class）を
作るプログラマー自身が決めるべき「業務ルール（ドメインロジック：domain logic）」だからです。
だからこそ、Pythonは**「デフォルトでは最も厳密で安全な『メモリの住所（同一性：identity）
』で判定しておくから、中身の比較（同値性：equality）が必要なら、
お前の手で __eq__ に審査ルールを書け！」**というアーキテクチャ（設計：architecture）に
なっているのです。
'''        

#%% 派生クラスでの同値判定
class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        print(Person.__init__)
        #<function Person.__init__ at 0x00000181A4A0EDE0>
    #↓氏、 名、 共に等しければ同値とする
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.firstname == other.firstname and \
                self.lastname == other.lastname
        return False
#↓派生クラスであるBusinessPersonクラスを追加
class BusinessPerson(Person):
    def __init__(self, firstname, lastname, title):
        super().__init__(firstname, lastname)
        #<function Person.__init__ at 0x00000181A4A0EDE0>
        print(super().__dict__) #{'firstname': '太郎', 'lastname': '山田'}
        print(super().__init__)
        #<bound method Person.__init__ of
        #<__main__.BusinessPerson object at 0x00000181A498CA50>>
        #titleを追加
        self.title = title   
if __name__=='__main__'    :
    p = Person('太郎', '山田')
    bp = BusinessPerson('太郎', '山田', '部長')
    print(p==bp) #True
    print(bp==p) #True
    print(p.__dict__==bp.__dict__) #False

r'''
第1部：【疑問解消】 title には肩書きの意味があるのか？
英語の「title」には、本や映画の「題名」という意味のほかに、
**「肩書き、役職、敬称」**という意味があります。 

第2部：【真理】 なぜ super().__init__ に self がいらないのか？
「Person.__init__ と同じ動きをするのなら、なぜ self を渡さなくていいのか？」 
この疑問は、前回の「バウンドメソッドの正体」の理解が繋がると、雷に打たれたようにスッキリと
解けます！
■ 現場監督のスローモーション
プロキシの生成: super() と書くと、現場監督はコンパイラが裏側に仕込んだ
            暗黙の情報を使い、親クラスである Person の操作マニュアル
            （メソッド：method）を安全に覗き見るための「代理人（プロキシオブジェクト：
            proxy object）」を作ります。
合体（バインド）の瞬間: super().__init__ とドット（.）で繋いで取り出した瞬間、
                現場監督は親クラスの __init__ という「ただの関数
                （関数オブジェクト：function object）」に、今まさに作られようと
                している自分自身（インスタンス：instance）をガチャン！と合体させます。
バウンドメソッドの完成: この時点で、取り出されたものは 「私自身（self）がすでに束縛
                （バインド：binding）された専用の初期化ボタン（バウンドメソッド
                ：bound method）」 になっています。
すでに自分自身がボタンの中に組み込まれているため、呼び出す際（カッコの中）に改めて self を
渡す必要はありません。super().__init__(firstname, lastname) と実行するだけで、
インタプリタ現場監督が裏側で自動的に self を先頭に差し込んでくれるのです。

第3部：【完全解剖】 サンプルコードの動きと「同値性のルール」
それでは、このコード全体の動きと、なぜ p == bp も bp == p も両方 True になるのかを解剖します。
① 基底の金型（基底クラス：base class）の定義 Person クラスには、自分と相手が「等しい
（同値性：equality）」かどうかを審査する独自のルール（特殊メソッド：special method または
 ダンダーメソッド：dunder method）である __eq__ が定義されています。 
 ここでは、「相手（other）が Person の一族か？（型チェック：type checking）」を確認し
、一族であれば「名（firstname）」と「氏（lastname）」が一致するかを判定します。
② 拡張された金型（派生クラス：derived class）の定義 BusinessPerson クラスは
 Person を継承（inheritance）しています。 初期化処理（__init__）を上書き
 （オーバーライド：override）し、名前の設定は親の機能（super().__init__）に
 丸投げ（委譲：delegation）しつつ、自分専用の属性として肩書き（title）を追加しています。 
 ここで重要なのは、BusinessPerson は独自の __eq__ を定義していないため、
 親の Person の審査ルールをそのまま引き継いでいるという点です
。
③ p == bp の評価（比較演算：comparison operation）
現場監督：「p（左辺）の審査ルール __eq__ を使うぞ！ 引数 other には bp
        （部長の山田太郎）が入る！」
現場監督：「isinstance(bp, Person) のチェックだな。bp は BusinessPerson の
        実体だが、BusinessPerson の親は Person だ。つまり bp も Person の
        一族（サブクラス：subclass）とみなせる！ 合格（True）だ！」
現場監督：「名前の比較だ。どちらも『山田太郎』で一致するから True を返せ！」
④ bp == p の評価（逆順での比較）
現場監督：「今度は bp（左辺）の審査ルールを使え！ ……おっと、BusinessPerson 
        には独自の __eq__ がないから、親から引き継いだ Person の __eq__ を使うぞ！」
現場監督：「引数 other には p（ただの山田太郎）が入る。isinstance(p, Person) は
        当然 True だ！」
現場監督：「名前の比較も一致する！ したがって結果は True だ！」
■ まとめ：オブジェクト指向の「設計思想」
このコードが示しているアーキテクチャの真理は、**「肩書き（title）が違っても、名前が同じなら同一人物と
して扱う」**という業務ルール（ドメインロジック：domain logic）を、プログラムとして完璧に表現している点に
あります。
もし「名前が同じでも、部長と平社員なら別人として扱いたい」のであれば、BusinessPerson クラスの
側でも __eq__ をオーバーライドして、「title も一致するか」という条件を付け加えなければなりません。
'''

#↓ BPクラスに__eq__を追加してオーバライドした場合
#%% 派生クラスでの同値判定
class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname    
    #↓氏、 名、 共に等しければ同値とする
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.firstname == other.firstname and \
                self.lastname == other.lastname
        return False
#↓派生クラスであるBusinessPersonクラスを追加
class BusinessPerson(Person):
    def __init__(self, firstname, lastname, title):
        super().__init__(firstname, lastname)
        #titleを追加
        self.title = title
    def __eq__(self, other):
        if isinstance(other, BusinessPerson):
            return super().__eq__(other) and \
                self.title == other.title
        return False        
if __name__=='__main__'    :
    p = Person('太郎', '山田')
    bp = BusinessPerson('太郎', '山田', '部長')
    print(isinstance(p, BusinessPerson)) #False
    print(p==bp) #Flase
    print(bp==p) #Flase
    print(p.__dict__==bp.__dict__) #Flase

r'''◆なぜすべての結果が False になるのか
第1部：【解剖】 bp == p の評価（順当な挙動）
まずはわかりやすい方から解説します。
左辺が BusinessPerson のインスタンスである bp の場合です。
現場監督：「bp == p だな！ 左辺である bp の審査ルール
    （等価演算子のオーバーライド：equality operator override）である 
    bp.__eq__(p) を呼び出せ！」
現場監督：「メソッドの内部だ。isinstance(other, BusinessPerson) の
    チェックを行うぞ。引数 other には p（ただの Person）が入っているな。
    p は BusinessPerson の金型（クラス：class）から作られた一族か？」
現場監督：「いや違う！ 親（Person）は子（BusinessPerson）の機能を持っていない
    から、一族（インスタンス：instance）とは認められない！
    （型チェック：type checking が False）」
現場監督：「よし、if文を抜けて末尾の return False に到達したな。結果は False だ！」
※補足：親 p は「肩書き」を知らないから、騙されて True を出してしまう。
　     だからシステムが介入し、親を黙らせて子 bp に審査を行わせる。
  　   子 bp は「お前は型が違うからダメだ」と False を突き返す。

第2部：【真理】 p == bp が False になる「衝撃の掟」
普通に考えれば、左辺が p なので p.__eq__(bp) が呼ばれ、その中では
 isinstance(bp, Person) が True になり（子は親の一族とみなせるため）、
 名前も一致して True が返りそうに見えます。
しかし、実行結果は False です。これについて、公式ドキュメント（3.3.1. 基本的な
カスタマイズ）には、次のような「絶対の掟」が定義されています。
    「オペランドが異なる型で、右の被演算子（右辺）の型が左の被演算子（左辺）の型の
    直接または間接のサブクラスである場合、右の被演算子の反射メソッド 
    (reflected method) が優先されます」
■ 現場監督（インタプリタ）のスローモーション
現場監督：「p == bp の比較だ！ 左辺の p の審査ルール（メソッド：method）である
         p.__eq__(bp) に判定させよう……おっと待て！」
現場監督：「右辺の bp の型（BusinessPerson）は、左辺の p の型（Person）の
        子供（派生クラス：derived class または サブクラス：subclass）じゃないか！」
現場監督：「子供のクラスは、親よりも『より厳密で高度な独自の審査ルール』を持っている
        可能性がある。ここで親のルールで勝手に判定したら、子供側のルール
        （役職まで一致しているか等）が無視されてしまう！」
現場監督：「Pythonの掟に従い、順番を裏側で強制的にひっくり返し、子孫である
         bp 側に用意された逆向きの審査ルール（反射メソッド：reflected
         method）を優先して呼び出せ！」
つまり、現場監督は裏側で自動的に bp.__eq__(p) を呼び出していたのです。 
その結果、「第1部」と全く同じ処理が走り、isinstance(p, BusinessPerson) で
弾かれて False が返された、というのがこの挙動の真理です。

第3部：【解剖】 p.__dict__ == bp.__dict__ の評価
最後に、辞書（インスタンス辞書：instance dictionary）同士の比較です。 
前回の解説の通り、比較対象が辞書（マッピング型：mapping type）になると、
現場監督は「中身のペアが完全に一致しているか」を審査します。
それぞれの金庫（__dict__ 属性）の中身を見てみましょう。
p.__dict__ : {'firstname': '太郎', 'lastname': '山田'}
bp.__dict__ : {'firstname': '太郎', 'lastname': '山田', 
               'title': '部長'}
■ 現場監督の審査 「左の金庫と右の金庫の中身を比較（マッピング型の等価比較：
                equality comparison for mapping types）しろ！
                ……おっと、右の金庫（bp）には title という名札（キー：key）が
                入っているが、左の金庫（p）には入っていないぞ！ 
                完全に一致していないから結果は False だ！」
■ まとめ：オブジェクト指向の「親と子」
今回のコードは、インフラ自動化のシステム設計における非常に美しいアーキテクチャの真理を
示しています。
子のルールの尊重：「親（一般的な機器）」と「子（拡張された特定ベンダー機器）」を
比較したとき、システムは安全のために「子」の複雑な判定ロジックを優先して採用
（反射メソッドへのフォールバック：fallback to reflected method）します。
これにより、予期せぬ「親の甘い基準での誤検知（誤った同一視）」を防ぐフェイルセーフな
設計となっているのです。
'''

#%% オブジェクトのハッシュ値を取得する
#●そもそもオブジェクトのハッシュ値を取得する意味とは？
class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    #↓氏、 名、 共に等しければ同値とする
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.firstname == other.firstname and \
                self.lastname == other.lastname   
    #●↓ハッシュ値を演算する
    def __hash__(self):
        print(hash((self.firstname, self.lastname)))
        #-6636340577094744702
        #-6636340577094744702
        return hash((self.firstname, self.lastname))
        #↑hash値の計算は簡単とのこと。 オブジェクトの同値判定にかかわる情報
        #(__eq__で利用してるインスタンス変数のみでよい)をタプルとしてまとめて 
        #hash関数に渡すだけ
        #↑をコメントアウトすると、TypeError: unhashable type: 'Person'
    
if __name__=='__main__'    :
    p = Person('太郎', '山田')
    dic = {p:'男'}
    print(dic[p])
    #↑男
    #●dict型のキーとしてPersonクラスを利用できるようになったとは、つまりどういうことを意味している？
    print(p.__hash__)
    #↑<bound method Person.__hash__ of 
    #<__main__.Person object at 0x00000181A3FFD210>>
    print(p.__dict__)
    #↑{'firstname': '太郎', 'lastname': '山田'}
    p.firstname = '次郎'
    #↑インスタンス変数を書き換えると、
    print(dic[p])
    #KeyError: <__main__.Person object at 0x00000181A498EE50>
    #ハッシュ値が変化してしまったので、目的のキーを検出できなくなった。

r'''
◆第1部：【真理】 そもそもハッシュ値を取得する意味と、辞書のキーにする意味とは？
●dict型のキーとしてPersonクラスを利用できるようになったとは、つまりどういうことを意味している？
辞書（ディクショナリ：dict）や集合（セット：set）は、何百万件のデータがあっても
一瞬でデータを見つけ出すために、「ハッシュテーブル」という超高速な検索システムを使っています。
■ 現場監督のスローモーション 
現場監督は、辞書のキーとしてオブジェクトを渡されたとき、いちいち全員の中身を確認して
探すような非効率なことはしません。 
現場監督：「このオブジェクトの『整理番号（ハッシュ値：hash value）』を計算させろ！ 
    あ、-66363...番ね！ じゃあこのデータを辞書の -66363...番の棚 に入れよう！」
    と、一瞬で場所を決めます。
つまり、__hash__ を実装して「辞書のキーとして利用できるようになった」ということは、
現場監督に対して**「このPersonという箱（インスタンス：instance）には、
固定の整理番号（ハッシュ値）を発行できるから、辞書のキー（見出し）として使っていいぞ！
（ハッシュ可能：hashable）」と許可を出した**ことを意味します
。
（※デフォルトではユーザー定義クラスはID（メモリアドレス）を元にしたハッシュ値を持ちますが、
同値判定の __eq__ をオーバーライドした瞬間、
システムは安全のために自動的に __hash__ = None （ハッシュ不可）に設定します
。それを再び「ハッシュ可能」に昇格させたのが今回のコードです。）
●なぜハッシュ不可にすると安全になるのか？
※__eq__ を上書きする ➔ 
    **「中身が変わるかもしれない（ミュータブルな）危険物」とみなされ、
    システム崩壊（ハッシュバケツの崩壊）を防ぐために自動でハッシュ禁止
    （__hash__ = None）**という安全装置が働く。
__hash__ を自作してハッシュ可能にする ➔ 
    プログラマーが**「このオブジェクトの中身は絶対に変更しない（イミュータブルである）」
    とシステムに約束する**高度な設計行為。

第2部：【解剖】 なぜ __eq__ で使う変数だけをタプルにしてハッシュ化するのか？
__eq__で利用してるインスタンス変数のみでよい
公式ドキュメントには、この点に関する「絶対の掟」が記されています。
「このメソッドに必要な性質は、比較結果が等しいオブジェクトは同じハッシュ値を持つということです」
もし、年齢（age）という変数を __eq__ の比較には使っていないのに、
ハッシュ値の計算には使ってしまったらどうなるか？ 「同値（同一人物：equality）」
と判定されるのに、ハッシュ値（整理番号）が違うという矛盾が起き、
現場監督がパニックを起こして辞書が破壊されます。そのため、__eq__ の判定に使う材料と、
ハッシュ値の計算に使う材料は、完全に一致させなければならないのです。

第3部：【深淵】 なぜ値を書き換えたら KeyError になったのか？
ここが、今回の検証の最大の成果です！ なぜ p.firstname = '次郎' とした
瞬間にクラッシュしたのか。
■ 現場監督のスローモーション
登録時（dic = {p:'男'}） 
現場監督：「『山田太郎』のハッシュ値を計算しろ！ 
    -66363... だな。よし、辞書の**『-66363...番の棚』**に『男』というデータを入れろ！」
書き換え時（p.firstname = '次郎'） オブジェクトの中身がこっそり書き換わりました。しかし、辞書の棚に入っている場所は移動していません（-66363...番の棚のまま）。
検索時（print(dic[p])） 現場監督：「よし、p のデータを辞書から探すぞ！ まず p の現在のハッシュ値を再計算しろ！」 現場監督：「『山田次郎』のハッシュ値は、さっきと違う 12345... 番になったな！ よし、辞書の**『12345...番の棚』**を開けろ！」 現場監督：「……空っぽじゃないか！！（KeyError）」
【真理】 この現象について、公式ドキュメントには非常に厳しい掟が記されています。
「ハッシュ可能なオブジェクトは、その生存期間中変わらないハッシュ値を持たなければなりません」
 「クラスがミュータブルなオブジェクトを定義しており、 __eq__() メソッドを実装しているなら、 __hash__() を定義してはなりません」
つまり、本来、**後から中身（インスタンス変数）を書き換えられる（変更可能：mutable）クラスを、辞書のキーにしてはいけない（ハッシュ化してはいけない）**のです。リスト（list）が辞書のキーになれず、タプル（tuple）が辞書のキーになれる理由も全く同じです（リストは中身が変わるとハッシュ値が変わって迷子になるため）
。
■ 参謀からのまとめ（Next Action）
もし Person クラスを辞書のキーとして使いたい（ハッシュ化したい）なら、インフラアーキテクトとしては**「このクラスのインスタンス変数（firstname, lastname）は、初期化（__init__）以降、外部から二度と変更できないように（不変：immutable に）設計する」**のが正しいアーキテクチャとなります。ここで、以前学習した「プロパティ（@property）」や「カプセル化（名前マングリング）」による防弾装甲が活きてくるのです。
'''
r'''◆補足：第1部：【真理】 インスタンス変数（属性）と辞書（キー）の決定的な違い
■ 1. インスタンス変数（p.gender = '男'）にする場合
意味: そのオブジェクト自身が生まれながらに持っている「本質的な状態・性質」。
インフラの例: Router クラスなら、hostname（ホスト名）や ip_address（IPアドレス）、vendor（Cisco等のベンダー名）は、ルーター自身が知っておくべき本質的なデータなので、インスタンス変数（属性）にするのが正解です。
■ 2. 辞書のキーにする場合（dic[p] = '男'）
意味: 外側のシステム（監視サーバーや実行中のスクリプト）が、そのオブジェクトに対して勝手に紐付けて管理したい「一時的な情報や、外部の機能」。
インフラの例: 何十台ものルーターを管理する自動化スクリプトを書いているとします。それぞれのルーターに対して、「今、SSH通信の接続が開いているか（セッション情報）」や「直近のPing応答時間は何ミリ秒だったか」を記録したいとします。
ここで、Router クラスの中に p.ssh_session や p.ping_latency というインスタンス変数を追加してしまうとどうなるでしょうか？ 「ルーターの設計図」の中に、「通信用の部品」や「監視アプリ用の部品」がどんどん混ざり込み、誰も全貌を理解できない巨大で複雑なクラス（神クラス：God Class）に成り果ててしまいます（＝クラスの責務の分離原則に違反します）。
第2部：【実務】 オブジェクトをキーにする「圧倒的な有難み」
ここで、「辞書のキーにオブジェクトそのものを使える（ハッシュ可能である）」という機能が、凄まじい威力を発揮します。
現場監督のアーキテクチャ（外部からの紐付け） ルーターのクラス（設計図）は、IPとホスト名だけを持つシンプルな状態に保ちます。 そして、スクリプトの実行側（外の世界）で、以下のような**「名簿（辞書）」**を作ります。
# 1. 接続セッションを管理する名簿（辞書）
active_sessions = {}

# 2. ルーターごとにSSH接続し、その「通信の線（セッション）」を辞書に紐付ける
for router in router_list:
    # オブジェクト自体をキーにして、値にSSHセッションを保存！
    active_sessions[router] = netmiko.ConnectHandler(ip=router.ip, ...)

# 3. 後で特定のルーターにコマンドを打ちたいとき
target_router = Router('192.168.1.1', 'Tokyo-RT')
session = active_sessions[target_router] # 一瞬でそのルーター専用の通信線を取り出せる！
session.send_command('show ip int brief')
これこそが、オブジェクトを辞書のキーにする最大の有難みです！
もしオブジェクトが辞書のキーにできなかったら（ハッシュ不可だったら）、どうなるでしょうか？ わざわざ active_sessions['192.168.1.1'] = session のように「IPアドレスの文字列」をキーにするしかありません。しかし文字列で管理し始めると、「このIPアドレスの機器のホスト名は何だっけ？」となった時に、また別のリストから探し直す手間が発生し、バグの温床になります。
「オブジェクトをそのままキーにできる」からこそ、現場監督は「Tokyo-RTというホスト名を持つ、192.168.1.1のルーター（の実体）」に一瞬でアクセスし、そこに紐付いたセッション情報や監視データを取り出すことができるのです。
'''






















