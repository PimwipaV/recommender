from sqlalchemy import create_engine
import os
import pandas as pd
from sklearn.decomposition import NMF
from fuzzywuzzy import process
import numpy as np
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors

def create_engine_load_data():
    '''Load data into memory and return an engine and data as a dataframe.'''
    # Load and fill database
    engine = create_engine('sqlite:///recommender3.db', echo=False)

    for f in os.listdir('data/movies/ml-latest-small/'):
        if f[-4:] == '.csv':
            data = pd.read_csv(f'data/movies/ml-latest-small/{f}')
            data.to_sql(f[:-4], engine)
            print(f[:-4], 'loaded succesfully')

    # LOAD DATA
    query = 'SELECT "userId", ratings."movieId", movies.title, rating FROM ratings JOIN movies ON ratings."movieId" = movies."movieId";'
    all_ratings = pd.read_sql(query, engine)

    return engine, all_ratings


def process_user_input(user_input=None, all_ratings=None):
    '''Return a tuple: key(name of input field), value(user input string), df_guess(dataframe of pre-selected movie names), guesses(fuzzywuzzy of user input and df_guess as tuple(title, scoring and index))'''
    # Extract tuple
    user_input_key = user_input[0]
    user_input_value = user_input[1]
    # Pre-select movies from database. Select everything that contains the first 3 letters capitalized of user input
    df_guess = all_ratings[all_ratings['title'].str.contains(user_input_value[:3].lower().capitalize())].groupby('title').first().reset_index()
    # Get ordered list of the five most similar movie titles to user input. Return a tuple of title, match score and index.
    guesses = process.extract(user_input_value, df_guess['title'])

    return user_input_key, user_input_value, df_guess, guesses