from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#Rohit
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
matrix = tf.fit_transform(df['overview'])
cosine_similarities = linear_kernel(matrix,matrix)
movie_title = df['original_title']
indices = pd.Series(df.index, index=df['original_title'])

def movie_recommend(original_title):

    idx = indices[original_title]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]

    return movie_title.iloc[movie_indices]

#nikita
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['description'])
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix) 

results = {}
for idx, row in ds.iterrows():
   similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
   similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices] 
   results[row['id']] = similar_items[1:]

def item(id):  
    return ds.loc[ds['id'] == id]['description'].tolist()[0].split(' - ')[0] 
  # Just reads the results out of the dictionary.def recommend(item_id, num):
    print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")   
    print("-------")    
    
    recs = results[item_id][:num]   
    for rec in recs: 
       print("Recommended: " + item(rec[1]) + " (score:" +      str(rec[0]) + ")")

#Praveen
import flask
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='templates')

df2 = pd.read_csv('./model/tmdb.csv')

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])
all_titles = [df2['title'][i] for i in range(len(df2['title']))]

def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['title'].iloc[movie_indices]
    dat = df2['release_date'].iloc[movie_indices]
    return_df = pd.DataFrame(columns=['Title','Year'])
    return_df['Title'] = tit
    return_df['Year'] = dat
    return return_df

# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
#        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
        if m_name not in all_titles:
            return(flask.render_template('negative.html',name=m_name))
        else:
            result_final = get_recommendations(m_name)
            names = []
            dates = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                dates.append(result_final.iloc[i][1])

            return flask.render_template('positive.html',movie_names=names,movie_date=dates,search_name=m_name)

if __name__ == '__main__':
    app.run()
