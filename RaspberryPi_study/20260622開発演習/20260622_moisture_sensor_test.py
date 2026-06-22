import time
from grove.adc import ADC

#水分センサーの刺さっているA0を指定
 #⇒修正A0ではなく、0でOK
  #でもなぜ0だけで良いのだろうか？
  #⇒A0は人間向けの親切な表示
  #  PythonのADCシステムではただの「チャンネル0」として処理されているから
MOI_SENSOR_PIN = 0

#BaseHatのADC(ｱﾅﾛｸﾞﾃﾞｼﾞﾀﾙｺﾝﾊﾞｰﾀｰ(翻訳機))操作用オブジェクトを生成
adc = ADC()

print('水分センサーの値測定を開始します(Ctrl+Cで終了)...')

try:
	while True:
		#A0ピンのアナログ電圧値を読み取る。
		moisture_value = adc.read(MOI_SENSOR_PIN)
		print(F'現在の水分量(ｱﾅﾛｸﾞ値)：{moisture_value}')
		time.sleep(1)
except KeyboardInterrupt:
	print('水分測定を終了します。')		
	
'''2026年6月22日13時30分測定結果（空中）
水分センサーの値測定を開始します(Ctrl+Cで終了)...
現在の水分量(ｱﾅﾛｸﾞ値)：0
現在の水分量(ｱﾅﾛｸﾞ値)：0
現在の水分量(ｱﾅﾛｸﾞ値)：2 ←素手でセンサーを抑えた。
現在の水分量(ｱﾅﾛｸﾞ値)：0
^Z
[1]+  停止
'''
'''
Deep Researchで抽出した先人たちのデータ（目安)
以下のような数値（12ビットADCの生データ）
空気中（完全乾燥）： 0
乾燥した土壌： 0 ～ 300
湿った土壌： 300 ～ 700
水中（ドブ漬け）： 700 ～ 950
'''
