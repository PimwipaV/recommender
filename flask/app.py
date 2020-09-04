from flask import Flask, render_template
from flask import Flask, request, jsonify, Response
import json
import mysql.connector
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/")
def hello():
    return "Flask inside Docker!!"

def getMysqlConnection():
    #return mysql.connector.connect(user='testing', host='0.0.0.0', port='3306', password='testing', database='test')
    return mysql.connector.connect(user='root', host='mysql2', port='3306', password='database', database='Netflix')

@app.route('/api/getMonths', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_months():
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