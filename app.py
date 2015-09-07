from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/index_asnwer', methods='post')
def index_asnwer():
    ticker=request.form['ticker']
    return ticker

if __name__ == '__main__':
  app.run(port=33507)
