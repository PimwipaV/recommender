from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('input.html')

if __name__ == '__main__':
    #app.run(port=5000, debug=False)
    app.run(debug=True,host='0.0.0.0', port=5004)
