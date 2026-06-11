from flask import Flask
from flask import render_template
from flask import redirect
import RPi.GPIO as GPIO

LED_SW = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_SW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
app = Flask(__name__)

@app.route("/")
def index():
	if GPIO.input(LED_SW)==GPIO.HIGH:
		status = "ON(スイッチを押している)"
	else:
		status = "OFF(スイッチ押されてない)"
	return render_template("index3.html",button_status=status)
if __name__=='__main__':
	try:
		app.debug = True
		app.run(host='0.0.0.0', port=80)
	finally:
		GPIO.cleanup()
