# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 11:34:10 2026

@author: iot01
"""
#%% 11.2.8 アトリビュートの取得/挙動の設定をカスタマイズする。
class MyInfo:
    #↓アトリビュート格納の為の辞書を準備
    def __init__(self):
        super().__setattr__('__data', {})
        #objectクラスの初期化処理__init__を実施して、
        #アトリビュートを設定するメソッド__setattr__(self,name)を実行して、
        #空の辞書と,_Myinfo__dataと？
        #●あれなぜ__dataは文字列なんだっけ？
        
    #↓指定されたアトリビュートを__dataから取得
    def __getattr__(self, name):
        try:
            return super().__getattribute__('__data')[name]
        except KeyError as ex:
            return None
        
    #↓指定されたアトリビュートを__dataに格納
    def __setattr__(self, name, value):
        super().__getattribute__('__data')[name] = value
        
if __name__=='__main__'        :
    i = MyInfo()
    i.score = 58
    i.hobbey = '卓球'
    print(i.hobbey) #卓球
    print(i.__dict__)
    #{'__data': {'score': 58, 'hobbey': '卓球'}}

#%% 11.2.9 ディスクリプター discripter 記述子
class LogProp:
    #対象のアトリビュート名(name)を設定
    def __init__(self, name):
        self.name = name
    
    #アトリビュート取得時の処理        
    def __get__(self, obj, type):
            print(f'{self.name}: get')
            return obj.__dict__[self.name]
        
    #アトリビュート設定時の処理
    def __set__(self, obj, value):
        print(F'{self.name}: set {value}')
        obj.__dict__[self.name] = value
        
class App
    #ディスクリプターを定義
    title         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    