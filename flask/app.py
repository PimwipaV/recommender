from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

db = pymysql.connect(db= 'Netflix', host='flask_mysql_1', user='root', passwd='database', port=3306) 

@app.route('/mysql', methods=['GET'])
def someName():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM shows3 WHERE director = 'Brad Anderson';")
    results = cursor.fetchall()
    cursor.close()
    return render_template('index2.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')