##3.1演算子～

#3.1.3-3.1.4除算、浮動小数点の演算
print(5/3)
    #1.6666666666666667
print(5//3)
    #1
print(0.2*3)
    #0.6000000000000001
print(0.2*6)
    #1.2000000000000002
print(0.2*3==0.6)
    #False

import decimal
"""
Decimal 型を使うには、標準ライブラリの decimal モジュールからインポートして使います。
from decimal import Decimal
# OK（正しい使い方）：文字列として渡す
a = Decimal('0.1')
b = Decimal('0.1')
c = Decimal('0.1')
print(a + b + c == Decimal('0.3'))  # True になる！
# NG（やってはいけない使い方）：float型をそのまま渡す
d = Decimal(0.1) 

＃なぜ''で囲って文字列として渡すのか？
システムは、括弧の中の 0.1 という数値リテラルを見た瞬間、まずハードウェアの仕様に従って float 型として
2進数で近似（0.10000000000000000555111...）してしまいます。
その「すでに誤差を含んでしまったゴミ入りのデータ」を Decimal の厳密な箱に入れても、
手遅れなのです。 そのため、正確な10進数を表現するには、必ず「文字列（ '0.1' ）」として
システムに渡し、ソフトウェア側で初めから正確な10進数として解釈させる必要があります。

！注意
＊Decimal 型の計算は、Pythonのプログラム（ソフトウェア）が裏側で桁上がりなどを1つずつシミュレートして
計算するため、float に比べて計算速度が圧倒的に遅く、メモリ容量も多く消費します。
＊Decimal型として生成された数値は、組み込みのint型やfloat型とは全く異なる「Decimalデータ型」という
専用のオブジェクトとして扱われます。
それを忘れて int 型と足し算しようとしたらどうなる？
エラーにはならず、正常に計算されて、結果も Decimal 型として返ってきます。
＊ただし誤差を含んだ float オブジェクト」を直接足し算（または引き算・掛け算・割り算）しようとすると、
システムは「厳密なデータと曖昧なデータを混ぜて計算することはできない！」
と判断し、TypeError を出してプログラムを強制停止させます。
"""

d1 = decimal.Decimal('0.2')
d2 = decimal.Decimal('3')
d3 = decimal.Decimal('0.6')
print(d1*d2)
    #0.6
print(d1*d2==d3)
    #True
    
#3.2.2[=]演算子による代入＝参照の引き渡し（つまりポインタ操作？）   
num1 = 20
num2 =num1
print(num1 is num2)
    #True
print(id(num1))
    #140718361093512
print(id(num2))
    #140718361093512
"""
id() 関数が返してくる「1407...」という数値自体もまた、ただの文字ではなく「
新しい整数オブジェクト（int型）」としてその場にポロッと生成される
"""
print(id(num1) is id(num2))
    #False
print(id(num1) == id(num2))
    #True

#3.2.3 mutabletとimmutable
data1 = [1,2,3]
data2 = data1
data1[0] = 100
print(data1)
print(data2)
x = 1
y = x
x += 10
print(x)    
print(y)
    
data1 = [1,2,3]
data2 = data1
data1 = [4,5,6]
print(data1)
print(data2)
print(id(data1))
print(id(data2))
print()
x = 1
print(str(id(x)))
y = x
print(str(id(x)))
print(str(id(y)))
x += 10
print(str(id(x)))

#3.2.4アンパック代入
data = [1,2,3,4,5,]
a,b,c,d,e = data
print(a)
print(b)
print(c)
print(d)    
print(e)
print(data)
m,n,*o = data    
print(m)
print(n)
print(o)
print(*o)
print(data)    
data = [1,2]
a,b,*c = data
print(c)
data = [1,2,3,4,5]
a,a,a,a,c = data
print(a)
print(c)

log_data = [
    'GigabitEthernet0/1', '192.168.10.1',
    '255.255.255.0', 'up', 'up']
interface_name,ip_address,*status_info = log_data
print(F'''
interface_name:{interface_name}
ip_address:{ip_address}      
''')
print('status_info:',end='')
print(*status_info)
    
    
    
    
    
    