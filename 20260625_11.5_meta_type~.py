# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 10:22:47 2026

@author: iot01
"""

#%%# 11.5　メタクラス
# 11.5．1 type関数とclass命令 type関数の 
#第2構文 type(nameクラス名, bases基底クラス群※ﾀﾌﾟﾙ, discクラス定義)
#●第2構文とは？？？ これもオーバーロードの例なのだろうか？

#↓Personクラスをtype()で書き換えるサンプルコード

#クラス定義に関わるメソッド(関数)を準備
def init(self, firstname, lastname):
    self.firstname = firstname
    self.lastname = lastname
    
def show(self):
    print(f'私の名前は{self.lastname}{self.firstname}です！')

#Personクラスを定義
#type(クラス名, 基底クラス群tuple, discクラス定義)
#変数discでは 変数/メソッド名:値 の形式で、 クラス定義を表す。
#メソッド本体を予め、 関数本体として定義しておき、 その参照を引数discに渡すとのこと。
#●↓がclass命令された時に、走っている本来の動作ということ？
#●つまりclassは糖衣構文？
Person = type(
    'Person',
    #↑このクラスの名前は'Person'とする。
    #●文字列なのはなぜ？
    (object,),
    #↑基底クラスとしてobjectクラスを引き継ぐ
    {
     '__init__':init,
     'show': show,
     'show2':(lambda self: print(f'私の名前は{self.lastname}{self.firstname}です！')),
     #↑簡単な命令ならlambdaで記述してもよいとのこと。
     #●discは何の言葉の略？
     #●__dict__に保存されているものとは違うの？
     #●ここもキーが文字列なのはなぜ？辞書型のキーは文字列でないとだめなのだっけ？
     #●__getattribute__で参照するときは必ず文字列で探すように、
     # ここも文字列で探すときまっているということ？
     }
)

if __name__=="__main__":
    p = Person('太郎','山田')
    p.show()
    print(p.show)
    #<bound method show of <__main__.Person object at 0x000001C8BA93B550>>
    #私の名前は山田太郎です！
    p.show2()
    #私の名前は山田太郎です！
    print(p.show2)
    #<bound method <lambda> of <__main__.Person object at 0x000001C8BA93B550>>
    #クラス命令を記述したのと同じようにインスタンス化とメソッドの実行が出来ているとのこと。
    #↓Python世界ではクラスもオブジェクト（インスタンス）であるとのこと。
    isinstance(Person, type) #True
    type(Person) #type
    #クラスを定義するとは、 type型のインスタンスを生成することとも言えるとのこと。

#%% 11.5.2 メタクラスの基本 typeクラスを別のクラスに置き換えてクラス定義そのものを変える。
#通常：クラス→→＜インスタンス化＞→→typeクラス
#メタクラス： クラス→→>インスタンス化>→→メタクラス→→<継承>→→typeクラス

class MyMeta(type):
    #↓classmethodどんなのだったか忘れてしまった、、、。
    @classmethod
    def __prepare__(matacls, name, bases, **kwargs):
        #print(F'{metacls}:__prepare__')
        #NameError: name 'metacls' is not defined
        #↑なぜエラーに？
        
        #return super.__prepare__(name, bases, **kwargs)
        return {'hoge':'ほげ'}
    
    def __new__(metacls, name, bases, disc, **kwargs):
        print(F'{metacls}:__new__')
        return super().__new__(metacls, name, bases, disc)
    
    def __init__(cls, name, bases, disc, **kwargs):
        print(f'{cls}:__init__')
        super().__init__(name, bases, disc)
    
    def __call__(cls, *args, **kwargs):
        print(f"{cls}:__call__")
        return super().__call__(*args, **kwargs)
    
class MyClass(metaclass=MyMeta)    :
    pass

if __name__=="__main__":
    c = MyClass()
    print(MyClass.hoge)
    # <class '__main__.MyMeta'>:__new__
    # <class '__main__.MyClass'>:__init__
    # <class '__main__.MyClass'>:__call__
    # ほげ
    
    print(MyClass)
    print(dir(MyClass))
    #print(MyClass.__disc__)
    #AttributeError: type object 'MyClass' has no attribute '__disc__'
    print(MyClass.__dict__)
    
    print(MyMeta)    
    print(dir(MyMeta))
    #print(MyMeta.__disc__)
    #AttributeError: type object 'MyClass' has no attribute '__disc__'
    print(MyMeta.__dict__)

#%% 11.5.3 シングルトンパターンをメタクラスを使って書き換える。
class SingletonMeta(type):
    #
    def __init__(cls, name, bases, disc, **kwargs):
        cls.__instance = None
        
    def __call__(cls, *args, **kwargs)        :
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance

class MySingleton(metaclass=SingletonMeta):
    pass

if __name__=="__main__":
    c1 = MySingleton()
    c2 = MySingleton()
    print(c1 is c2) #True
    print(type(c1)) #<class '__main__.MySingleton'>
    print(type(SingletonMeta)) #<class 'type'>



















    






