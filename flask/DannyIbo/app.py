from flask import Flask, jsonify, make_response, render_template, request
import os
from modelselect import create_engine_load_data, process_user_input
#แค่เอา model_keras.py มาโหลดใส่ตรงนี้ได้ก็เสร็จเหมือนกัน
#from .model_keras import ....? ไม่มีฟังก์ชั่นแล้วจะอิมพอร์ทอะไรมา?
#หรือไม่ก็แค่ต่อ sqlite เข้าไปให้ได้ นอกนั้นก็เสร็จหมดแล้วของ dannyibo แต่ไม่ได้ใช้ keras, deep learning
#แต่ใช้ sklearn NMF

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('input.html')

engine, all_ratings = create_engine_load_data()

#@app.route('/testsqlite')
#def sqlite():
    #self.write(all_ratings.to_dict())

@app.route('/select')
def select():
    user_input = request.args.items()

    guesses_list = []
    for ui in user_input:
        if ui[1]:
            guesses = process_user_input(user_input=ui, all_ratings=all_ratings)
            guesses_list.append(guesses)

    return render_template(
        'select.html',
        guesses_list=guesses_list,
        user_input=user_input)

if __name__ == '__main__':
    #app.run(port=5000, debug=False)
    app.run(debug=False,host='0.0.0.0', port=5002)
