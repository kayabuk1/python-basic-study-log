from flask import Flask
from flask import render_template
from flask import redirect

app = Flask(__name__)

@app.route("/")
def hello_world():
	return render_template("04_02_scamera.php")
@app.route("/scamera/off")
def scamera_onf():
	subprocess.run("killall mjpg_streamer", shell=True))
	return redirect("/")
@app.route("/scamera/on")
def scamera_off():
	subprocess.run("/home/pi/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -o '~/output_http.so -w ~/www -p 8080' -i './input_uvc.so -d /dev/video1 -r 1920x1080 -fps 30 -q 10' > /dev/null 2>&1 &",shell=True)
	return redirect("/")
if __name__=="__main__":
	app.debug=True
	app.run(host="0.0.0.0", port=8000)