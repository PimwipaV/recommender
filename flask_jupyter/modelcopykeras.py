
import pandas as pd
import numpy as np
from zipfile import ZipFile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt

"""
## First, load the data and apply preprocessing
"""

# Download the actual data from http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
# Use the ratings.csv file

def recommend():

    movielens_data_file_url = (
        "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    )
    movielens_zipped_file = keras.utils.get_file(
        "ml-latest-small.zip", movielens_data_file_url, extract=False
    )
    keras_datasets_path = Path(movielens_zipped_file).parents[0]
    movielens_dir = keras_datasets_path / "ml-latest-small"

    # Only extract the data the first time the script is run.
    if not movielens_dir.exists():
        with ZipFile(movielens_zipped_file, "r") as zip:
            # Extract files
            print("Extracting all the files now...")
            zip.extractall(path=keras_datasets_path)
            print("Done!")

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
    ratings = model.predict(user_movie_array).flatten()

    return model
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

    #return history
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

    #return movie_df

def process_user_input(user_input=None):
    '''Return a tuple: key(name of input field), value(user input string), 
    df_guess(dataframe of pre-selected movie names), guesses(fuzzywuzzy of user input 
    and df_guess as tuple(title, scoring and index))'''
    # Extract tuple
    user_input_key = user_input[0]
    user_input_value = user_input[1]
    df_guess = all_ratings[all_ratings['title'].str.contains(user_input_value[:3].lower().capitalize())].groupby('title').first().reset_index()
    guesses = process.extract(user_input_value, df_guess['title'])

    return user_input_key, user_input_value, df_guess, guesses

