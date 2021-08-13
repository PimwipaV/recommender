from sqlalchemy import create_engine
import os
import pandas as pd
import numpy as np
from fuzzywuzzy import process
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def create_engine_load_data():

    engine = create_engine('sqlite:///recommender.db', echo=False)
#engine = create_engine('sqlite:///:memory:', echo=False)

    for f in os.listdir('ml-latest-small/'):
        if f[-4:] == '.csv':
            data = pd.read_csv(f'ml-latest-small/{f}')
            data.to_sql(f[:-4], engine)
            print(f[:-4], 'loaded succesfully')

# LOAD DATA
    query = 'SELECT "userId", ratings."movieId", movies.title, rating FROM ratings JOIN movies ON ratings."movieId" = movies."movieId";'
    all_ratings = pd.read_sql(query, engine)
    return engine, all_ratings

#print(all_ratings)

def process_user_input(user_input=None, all_ratings=None):
    '''Return a tuple: key(name of input field), value(user input string), df_guess(dataframe of pre-selected movie names), guesses(fuzzywuzzy of user input and df_guess as tuple(title, scoring and index))'''
    #Extract tuple คือ key:value pair in the url after ?
    user_input_key = user_input[0]
    user_input_value = user_input[1]
    # Pre-select movies from database. Select everything that contains the first 3 letters capitalized of user input
    #print(user_input)
    df_guess = all_ratings['title']
    df_guess = all_ratings[all_ratings['title'].str.contains(user_input_value[:3].lower().capitalize())].groupby('title').first().reset_index()
    # Get ordered list of the five most similar movie titles to user input. Return a tuple of title, match score and index.
    guesses = process.extract(user_input_value, df_guess['title'])
    #print(df_guess)
    print(guesses)
    
    return user_input_key, user_input_value, df_guess, guesses

def recommend_movies(
    all_ratings=None,
    user_movie_title_list=None,
    engine=None,
    number_of_recommendations=5):

    watched_movie_id_list = []
    for mt in user_movie_title_list:
        if mt[1]:
            movie_id = all_ratings[all_ratings['title'] == mt]['movieId'].unique()[0]
            watched_movie_id_list.append(movie_id)

    #prepare x_test (movies_not_watched)
    #remove the user input movies from all_movies
    movie_id_unique = 'SELECT * FROM movies'
    all_movies = pd.read_sql(movie_id_unique, engine)

    movies_not_watched = all_movies[~all_movies['movieId'].isin(watched_movie_id_list)]
    movies_not_watched.loc[:,'fake_id'] = np.ones(len(movies_not_watched), dtype =int)

    #now prepare x_train
    #get all_ratings from sqlite
    query = 'SELECT "userId", ratings."movieId", movies.title, rating FROM ratings JOIN movies ON ratings."movieId" = movies."movieId";'
    all_ratings = pd.read_sql(query, engine)

    #remove the watched movies from all_ratings
    not_all_ratings = all_ratings[~all_ratings['movieId'].isin(watched_movie_id_list)]

    #make a sequence id list of all_ratings['movieId']
    #also to get num_movies and numbers of index
    movieindex = not_all_ratings['movieId'].unique().tolist()
    dl_movie2movie_encoded = {x: i for i, x in enumerate(movieindex)}
    dl_movie_encoded2movie = {i: x for i, x in enumerate(movieindex)}

    not_all_ratings.loc[:,"movie"] = not_all_ratings["movieId"].map(dl_movie2movie_encoded)
    not_all_ratings.loc[:,"rating"] = not_all_ratings["rating"].values.astype(np.float32)

    #give user a running number, not only index
    not_all_user_ids = not_all_ratings["userId"].unique().tolist()
    dl_user2user_encoded = {x: i for i, x in enumerate(not_all_user_ids)}
    dl_userencoded2user = {i: x for i, x in enumerate(not_all_user_ids)}

    not_all_ratings.loc[:,"user"] = not_all_ratings["userId"].map(dl_user2user_encoded)

    min_rating = min(not_all_ratings["rating"])
    max_rating = max(not_all_ratings["rating"])
    num_users = len(dl_user2user_encoded)
    num_movies = len(dl_movie_encoded2movie)
    print(
            "Number of users: {}, Number of Movies: {}, Min rating: {}, Max rating: {}".format(
                num_users, num_movies, min_rating, max_rating
            )
        )

    #define training data
    df = not_all_ratings.sample(frac=1, random_state=42)
    x = not_all_ratings[["user", "movie"]].values

        # Normalize the targets between 0 and 1. Makes it easy to train.
    y = not_all_ratings["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
        # Assuming training on 90% of the data and validating on 10%.
    train_indices = int(0.9 * df.shape[0])
    x_train, x_val, y_train, y_val = (
            x[:train_indices],
            x[train_indices:],
            y[:train_indices],
            y[train_indices:],
        )

    #inference x_test = that
    user_movie_array = movies_not_watched[['fake_id','index']]
    max_movie_index = user_movie_array['index'].max()
    that = user_movie_array.to_numpy()

    EMBEDDING_SIZE = 50

    class RecommenderNet(keras.Model):
            def __init__(self, num_users, num_movies, embedding_size, **kwargs):
                super(RecommenderNet, self).__init__(**kwargs)
                self.num_users = num_users
                self.num_movies = num_movies
                self.embedding_size = embedding_size
                self.user_embedding = layers.Embedding(
                    num_users,
                    embedding_size,
                    embeddings_initializer="he_normal",
                    embeddings_regularizer=keras.regularizers.l2(1e-6),
                )
                self.user_bias = layers.Embedding(num_users, 1)
                self.movie_embedding = layers.Embedding(
                #change this line from num_movies to max_movie_index+1
                    max_movie_index+1,
                    embedding_size,
                    embeddings_initializer="he_normal",
                    embeddings_regularizer=keras.regularizers.l2(1e-6),
                )
                #and this line (input_dim)
                self.movie_bias = layers.Embedding(max_movie_index+1, 1)

            def call(self, inputs):
                user_vector = self.user_embedding(inputs[:, 0])
                user_bias = self.user_bias(inputs[:, 0])
                movie_vector = self.movie_embedding(inputs[:, 1])
                movie_bias = self.movie_bias(inputs[:, 1])
                dot_user_movie = tf.tensordot(user_vector, movie_vector, 2)
                # Add all the components (including bias)
                x = dot_user_movie + user_bias + movie_bias
                # The sigmoid activation forces the rating to between 0 and 1
                return tf.nn.sigmoid(x)


    model = RecommenderNet(num_users, num_movies, EMBEDDING_SIZE)
    model.compile(
            loss=tf.keras.losses.BinaryCrossentropy(), optimizer=keras.optimizers.Adam(lr=0.001)
        )
    ratings = model.predict(that).flatten()

    movies_not_watched.loc[:,'prediction'] = ratings
    highest_score = ratings[ratings.argsort()[-10:]][::-1] #เอาค่ามาถึงจะถูก

    recom_movie_titles = movies_not_watched.loc[movies_not_watched.loc[:,'prediction'].isin(highest_score)] ##wuuuhuuuuwww
    return recom_movie_titles
