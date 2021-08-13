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