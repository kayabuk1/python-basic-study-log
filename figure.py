# -*- coding: utf-8 -*-
"""
Created on Fri May 29 10:30:14 2026

@author: iot01
"""

#%% 9.3.1 モジュールの定義用別ファイル
import math
def get_triangle(base, height):
    return base*height/2
def get_circle(radius):
    return radius*radius*math.pi
if __name__=='__main__':
    print(f'三角形の面積：{get_triangle(10,2)}')
    print(f'円の面積:{get_circle(5)}')

