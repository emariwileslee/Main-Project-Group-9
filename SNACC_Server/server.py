from flask import render_template, Flask, url_for
import csv

app = Flask(__name__)


@app.route('/')

def hello():  
    data = []
    with open('..\SNACC_Mapper\Output\output.csv', newline = '') as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        i = 0
        for row in rows:
            if i != 0:
                data.append(row)
            i += 1
        return render_template('visualize.html', data=data)
