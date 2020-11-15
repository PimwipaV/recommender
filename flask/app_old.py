def getMysqlConnection():
    #return mysql.connector.connect(user='testing', host='0.0.0.0', port='3306', password='testing', database='test')
    return mysql.connector.connect(user='root', host='mysql2', port='3306', password='database', database='Netflix')


@app.route('/api/getTest', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_test():
    db = getMysqlConnection()
    print(db)
    try:
        sqlstr = "SELECT * FROM shows3 WHERE director = 'Brad Anderson';"
        print(sqlstr)
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return jsonify(results=output_json)
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


@app.route('/gettest')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM shows3 WHERE director = 'Brad Anderson''')
    rv = cur.fetchall()
    return str(rv)

if __name__ == '__main__':
    app.run(debug=True)

import pymysql

db = pymysql.connect("localhost", "username", "password", "database")

app = Flask(__name__)
api = Api(app)



@app.route('/mysql', methods=['GET'])
def someName():
    #cursor = db.cursor()
    connect = mysql.connect()
    cursor = connect.cursor()
    sql = " SELECT * FROM shows3 WHERE director = 'Brad Anderson'"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('index2.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
 
app.run(host='localhost', port=5000)

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

pymysql.connect(db='base', user='root', passwd='pwd', unix_socket="/tmp/mysql.sock")
pymysql.connect(db='base', user='root', passwd='pwd', host='localhost', port=XXXX)
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


    #db = pymysql.connect("mysql", "root", "database", "Netflix")
#pymysql.connect(db='base', user='root', passwd='pwd', unix_socket="/tmp/mysql.sock")
#db = pymysql.connect(host='flask_mysql_1', user='root', passwd='database', port=3306) 
#db = pymysql.connect(db= 'mysql', host='f2924b8102e9', user='root', passwd='database', port=3306) 
db = pymysql.connect(db= 'Netflix', host='flask_mysql_1', user='root', passwd='database', port=3306) 

#this works
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
#this works ends

