
from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route("/get-gas")
def get_csv():
    return send_file("data/excel.xlsx", as_attachment=True)


@app.route("/get-result1")
def get_csv1():
    return send_file("data/res1.xlsx", as_attachment=True)

@app.route("/get-result2")
def get_csv2():
    return send_file("data/res2.xlsx", as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)