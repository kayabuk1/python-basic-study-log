from flask import Flask
from flask import render_template
from flask import redirect
import RPi.GPIO as GPIO

LED25_PIN = 25
LED26_PIN = 26
LED27_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED25_PIN, GPIO.OUT)
GPIO.setup(LED26_PIN, GPIO.OUT)
GPIO.setup(LED27_PIN, GPIO.OUT)
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("04_led.html")
@app.route("/led25/off")
def led25_off():
	GPIO.output(LED25_PIN, GPIO.LOW)
	return redirect("/")
@app.route("/led26/off")
def led26_off():
        GPIO.output(LED26_PIN, GPIO.LOW)
        return redirect("/")
@app.route("/led27/off")
def led27_off():
        GPIO.output(LED27_PIN, GPIO.LOW)
        return redirect("/")
@app.route("/led25/on")
def led25_on():
        GPIO.output(LED25_PIN, GPIO.HIGH)
        return redirect("/")
@app.route("/led26/on")
def led26_on():
        GPIO.output(LED26_PIN, GPIO.HIGH)
        return redirect("/")
@app.route("/led27/on")
def led27_on():
        GPIO.output(LED27_PIN, GPIO.HIGH)
        return redirect("/")
if __name__=='__main__':
	app.debug=True
	app.run(host='0.0.0.0',port=80)
