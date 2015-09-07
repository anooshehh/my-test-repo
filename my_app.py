from flask import Flask, render_template, request, redirect

from bokeh.plotting import figure, show, output_file
from bokeh.embed import components, notebook_div
from jinja2 import Template
from os import path

from numpy import *
from pandas import *

import datetime, requests

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        ticker = request.form['ticker']
        date=datetime.date.today()
        start_date=(date+DateOffset(months=-1)).date().__str__()
        end_date=date.__str__()
        quandl_url = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?'+'start_date='+start_date+'&end_date='+end_date+'&order=asc&column_index=4&collapse=daily'
        r=requests.get(quandl_url)
        if r.ok == False:
            return redirect('/Error')
        else:
            data=r.json()
            dataset=data['dataset']
            df=DataFrame.from_dict(dataset['data'])
            p = figure(x_axis_type = "datetime")
            p.line(array(df[0], 'M64'), df[1], color='#A6CEE3', legend=ticker)
            p.title = ticker+" Closing Price (Quandl WIKI Dataset)"
            p.grid.grid_line_alpha=0.3
            p.xaxis.axis_label = 'Date'
            p.yaxis.axis_label = 'Price'
            script, div = components(p)

            template = Template('''<!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="utf-8">
                <title>Stock Closing Data</title>
                <style> div{float: left;} </style>
                <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.css" type="text/css" />
                <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.js"></script>
                {{ script }}
                </head>
                <body>
                <div class=page>
                <h1>Generated graph for {{ ticker }} <br><FORM><INPUT Type="button" VALUE="Back" onClick="history.go(-1);return true;"></FORM></h1>
                {{ div }}
                </div>
                </body>
                </html>''')
        
            html_file='stocks.html'
            file_path = path.relpath("templates/"+html_file)
            with open(file_path, 'w') as textfile:
                textfile.write(template.render(script=script, div=div, ticker=ticker))
            return redirect('/stocks')

@app.route('/Error')
def Error():
    return render_template('Error.html')

@app.route('/stocks')
def stocks():
    return render_template('stocks.html')

if __name__ == '__main__':
    app.run()
