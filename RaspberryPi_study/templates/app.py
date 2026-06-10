from flask import Flask
from flask import render_template
from flask import redirect
import RPi.GPIO as GPIO

LED_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index2.html")

@app.route("/led/off")
def led_off():
	GPIO.output(LED_PIN, GPIO.LOW)
	return redirect("/")

@app.route("/led/on")
def led_on():
	GPIO.output(LED_PIN, GPIO.HIGH)
	return redirect("/")

if __name__ =='__main__':
	app.debug=True
	app.run(host='0.0.0.0',port=80)
