from flask import Flask, jsonify, make_response, render_template, request
import os
from .model_try import process_user_input


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('input.html')

@app.route('/select')
def select():
    user_input = request.args.items()

    return render_template('select.html', user_input= user_input)

import json
def Table():
    all_ratings = pd.read_csv(ratings_file)
    all_ratings = all_ratings.to_json()
    data = []
    data = json.loads(all_ratings)
    context = {'d':data}
    return render('table.html', context)

def score():
    features = request.json['X']
    return make_response(jsonify({'score': features}))

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
