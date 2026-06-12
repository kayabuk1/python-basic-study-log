from flask import Flask
from flask import render_template
from flask import redirect
import RPi.GPIO as GPIO
from grove.adc import ADC
from time import sleep

app = Flask(__name__)
adc = ADC()
sensor_configs = [
    ("A0ボリューム", 0),
    ("A2光センサー", 2)
]

@app.route("/")
def index():
	results = list() 
	for name, pin in sensor_configs:
		val = adc.read(pin)
		results.append(f"{name}: {val}") 
		print(" | ".join(results))
		status = results	
	return render_template("index4.html",sensor_status=status)

if __name__=='__main__':
	try:
		app.debug = True
		app.run(host='0.0.0.0', port=80)
	finally:
		GPIO.cleanup()
