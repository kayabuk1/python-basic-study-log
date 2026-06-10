from flask import Flask
app = Flask(__name__)

@app.route("/")
#「差し込まれている関数」の正体は、**「私は / のURLを担当します！という、Webサーバー（Flask）へのジョイント登録処理」
def index():
        return'''
                <html>
                        <body>
                                <h1>Hello Flask...!!</h1>
                        </body>
                </html>'''
if __name__ == "__main__":
        app.debug = True
        app.run(host="0.0.0.0",port=80)
