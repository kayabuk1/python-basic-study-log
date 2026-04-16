
#練習問題1－1
"""
1．データ型はint型、値は37
2．エラー
3．データ型はstr型、値は世界2か国
4．データ型はint型、値は6
"""
#練習問題1－2

def bmi_calc():
    print('体重（kg）を入力：')
    kg = float(input())
    print('身長(cm)を入力：')
    height_cm = float(input())
    height_m = height_cm/100
    bmi_value = kg / (height_m*height_m)
    print(F"BMIは{bmi_value:.2f}です")
    print(F"""
    【入力データ確認】
    体重（kg）を入力：{kg:.2f}
    身長(cm)を入力：{height_m:.2f}
    BMIは{bmi_value:.2f}です
    """)
bmi_calc()
