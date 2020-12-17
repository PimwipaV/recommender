from sqlalchemy import create_engine
import os
import pandas as pd
from fuzzywuzzy import process
import numpy as np
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors

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

#def get_chosen_index(all_ratings=None, user_movie_title_list=None):
    #'''Return index of movie titles from guesses that user selected'''
    #user_movie_id_ratings_matrix=None,
    #genre_movie_matrix=None,
    #NMF_Model=None,
    #engine=None,
    #number_of_recommendations=5):
    #arai_key = user_movie_title_list[0]
    #arai_value = user_movie_title_list[1]
    # Get movie ids for the titles that the user selected
    #movie_id_list = []
    #for mt in user_movie_title_list:
    #for ind in guesses:
        #movie_id = all_ratings[all_ratings['title'] == mt]['movieId'].unique()[0]
        #movie_id_list.append(movie_id)

    #print(movie_id_list)
    #return movie_id_list