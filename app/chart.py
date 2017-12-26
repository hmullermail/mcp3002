from flask import Flask
from flask import render_template
from init import db, Reading, count_logs, reading_logs

app = Flask(__name__)
#nopts = 8

@app.route('/')
def hello_world():
    return 'Hello World!'

# @app.route("/")
# def chart():
#     labels = ["January","February","March","April","May","June","July","August"]
    
#     for i in range(0,nopts-1):
#     values[i] = i**2
#     #values[i] = reading_logs(count_logs-nopts)
#     return render_template('chart2.html', values=values, labels=labels)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)