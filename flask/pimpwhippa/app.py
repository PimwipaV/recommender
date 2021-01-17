from flask import Flask, jsonify, make_response, render_template, request
import os
from modelselect import (
    create_engine_load_data, 
    process_user_input,
    recommend_movies
)

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

    user_movie_title_list = request.args.values()

    recom_movie_titles = recommend_movies(
        all_ratings=all_ratings,
        user_movie_title_list=user_movie_title_list,
        engine=engine,
        number_of_recommendations=10
    )

    #return render_template('chosenindex.html', data=watched_movie_id_list)
    return render_template('chosenindex.html', data=recom_movie_titles)


if __name__ == '__main__':
    #app.run(port=5000, debug=False)
    app.run(debug=False,host='0.0.0.0', port=5002)
