from flask import Flask, request, render_template
import pymysql
#from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

db = pymysql.connect("mysql", "root", "database", "Netflix")
#mysql = MySQL(app)
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'database'
#app.config['MYSQL_DB'] = 'mysql'
 
@app.route('/mysql', methods=['GET'])
def someName():
    #cursor = mysql.connection.cursor()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM shows3 WHERE director = 'Brad Anderson';")
    results = cursor.fetchall()
    cursor.close()
    #return render_template('index2.html', results=results[0])
    return render_template('index2.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)