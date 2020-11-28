from sqlalchemy import create_engine
import os
import pandas as pd
from sklearn.decomposition import NMF
from fuzzywuzzy import process
import numpy as np
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors

ratings_file = movielens_dir / "ratings.csv"
df = pd.read_csv(ratings_file)

"""
First, need to perform some preprocessing to encode users and movies as integer indices.
"""
user_ids = df["userId"].unique().tolist()
user2user_encoded = {x: i for i, x in enumerate(user_ids)}
userencoded2user = {i: x for i, x in enumerate(user_ids)}
movie_ids = df["movieId"].unique().tolist()
movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}
df["user"] = df["userId"].map(user2user_encoded)
df["movie"] = df["movieId"].map(movie2movie_encoded)

num_users = len(user2user_encoded)
num_movies = len(movie_encoded2movie)
df["rating"] = df["rating"].values.astype(np.float32)
# min and max ratings will be used to normalize the ratings later
min_rating = min(df["rating"])
max_rating = max(df["rating"])

print(
    "Number of users: {}, Number of Movies: {}, Min rating: {}, Max rating: {}".format(
        num_users, num_movies, min_rating, max_rating
    )
)

"""
## Prepare training and validation data
"""
df = df.sample(frac=1, random_state=42)
x = df[["user", "movie"]].values
# Normalize the targets between 0 and 1. Makes it easy to train.
y = df["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
# Assuming training on 90% of the data and validating on 10%.
train_indices = int(0.9 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:],
)

"""
## Create the model
We embed both users and movies in to 50-dimensional vectors.
The model computes a match score between user and movie embeddings via a dot product,
and adds a per-movie and per-user bias. The match score is scaled to the `[0, 1]`
interval via a sigmoid (since our ratings are normalized to this range).
"""
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
            num_movies,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.movie_bias = layers.Embedding(num_movies, 1)

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

"""
## Train the model based on the data split
"""
history = model.fit(
    x=x_train,
    y=y_train,
    batch_size=64,
    epochs=5,
    verbose=1,
    validation_data=(x_val, y_val),
)

"""
## Plot training and validation loss
"""
plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.title("model loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.legend(["train", "test"], loc="upper left")
plt.show()

"""
## Show top 10 movie recommendations to a user
"""

movie_df = pd.read_csv(movielens_dir / "movies.csv")

#user keys in their fav movies

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


def recommend_movies(
    all_ratings=None,
    user_movie_title_list=None,
    user_movie_id_ratings_matrix=None,
    genre_movie_matrix=None,
    NMF_Model=None,
    engine=None,
    number_of_recommendations=5):

    # Get movie ids for the titles that the user selected
    movie_id_list = []
    for mt in user_movie_title_list:
        movie_id = all_ratings[all_ratings['title'] == mt]['movieId'].unique()[0]
        movie_id_list.append(movie_id)

    # Get theindexes, where the movie ids are in the NMF
    movie_index_list = []
    for id_ in movie_id_list:
        index = list(user_movie_id_ratings_matrix.columns).index(id_)
        movie_index_list.append(index)

    # Setup the ratings that the user did by selecting titles and prepare prediction
    user_rating = np.zeros(user_movie_id_ratings_matrix.shape[1])
    for i in movie_index_list:
        user_rating[i] = 5
    user_rating = user_rating.reshape(-1,1)
    user_rating = user_rating.T

#here is prediction from NMF model
    # Perform prediction
    new_P = NMF_Model.transform(user_rating)
    new_user_recommendations = np.dot(new_P,genre_movie_matrix)
    list_recom_indexes = new_user_recommendations.argsort()[:,-number_of_recommendations:][0][::-1]

    #Get themovie ids for the recommended movies
    recom_movie_ids = []
    for l in list_recom_indexes:
        recom_movie_ids.append(user_movie_id_ratings_matrix.columns[l])

    # Get the titles for the recommended movie ids
    recom_movie_titles = []
    for mid in recom_movie_ids:
        title = all_ratings[all_ratings['movieId'] == mid]['title'].unique()[0]
        recom_movie_titles.append(title)

    return recom_movie_titles

#here is another prediction by neural network model

#here is the number_of_recommendations how many movies am I recommending 5 or 10
#if i only input 1 movie can it also give 10 recommendations?
top_ratings_indices = ratings.argsort()[-10:][::-1]
recommended_movie_ids = [
    movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_ratings_indices
]

#display this in flask putting in recommend.html
print("Showing recommendations for user: {}".format(user_id))
print("====" * 9)
print("Movies with high ratings from user")
print("----" * 8)
top_movies_user = (
    movies_watched_by_user.sort_values(by="rating", ascending=False)
    .head(5)
    .movieId.values
)
movie_df_rows = movie_df[movie_df["movieId"].isin(top_movies_user)]
for row in movie_df_rows.itertuples():
    print(row.title, ":", row.genres)

print("----" * 8)
print("Top 10 movie recommendations")
print("----" * 8)
recommended_movies = movie_df[movie_df["movieId"].isin(recommended_movie_ids)]
for row in recommended_movies.itertuples():
    print(row.title, ":", row.genres)