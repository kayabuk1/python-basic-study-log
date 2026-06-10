from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("03_form.html")
@app.route("/test", methods=["GET","POST"])
def test():
	if request.method=="GET":
		res = request.args.get("get_value")
	elif request.method=="POST":
		res = request.form["post_value"]
	return res
if __name__ == '__main__':
	app.debug=True
	app.run(host="0.0.0.0",port=80)
