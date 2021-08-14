from flask import Flask, jsonify, make_response, render_template, request
import os
from model import reg

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('input.html')

@app.route('/predict')
def predict():
    user_input = request.args.items()
    #take value froms user_input as x for training
    proposed_buying_price = reg.predict(user_input)

    #recom_movie_titles = recom_movie_titles.to_html()
    return render_template('buying_price.html', data=proposed_buying_price)
    #return render_template('recom_titles.html',
    #tables=[recom_movie_titles])
    #return render_template('chosenindex.html', data=watched_movie_id_list)
    #return render_template('recom_titles.html', data=recom_movie_titles.to_html())

if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5001))
        app.run(debug=False,host='0.0.0.0', port=port)
