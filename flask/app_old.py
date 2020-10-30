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