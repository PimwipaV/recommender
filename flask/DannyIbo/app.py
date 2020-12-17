from flask import Flask, jsonify, make_response, render_template, request
import os
from modelselect import create_engine_load_data, process_user_input

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('input.html')

engine, all_ratings = create_engine_load_data()

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


@app.route('/recommend')
def recommend():
#ตอนนี้นึกว่า method = ['GET', 'POST] คือสิ่งที่ทำให้มันแตกต่างระหว่างเสนอ guesses ไป
#กับตอนที่ user เลือกกลับมา แต่ไม่เห็นมีตรงไหนเป็นแบบนี้เลยหนิ แล้วมันเอาการเลือกนั้นมายังไง
    user_movie_title_list = request.args.values()
    #chosen_index = user_movie_title_list.index()
    movie_id_list = []
    for mt in user_movie_title_list:
        if mt[1]:
            #movieindex = get_chosen_index(user_movie_title_list=mt, all_ratings=all_ratings)
            movie_id = all_ratings[all_ratings['title'] == mt]['movieId'].unique()[0]
            movie_id_list.append(movie_id)

    return render_template('chosenindex.html', data=movie_id_list)
    #return render_template('chosenindex.html', data=chosen_index)


if __name__ == '__main__':
    #app.run(port=5000, debug=False)
    app.run(debug=False,host='0.0.0.0', port=5002)
