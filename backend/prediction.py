import os
import logging
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from joblib import load


# load .env content to env vars
load_dotenv()

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT")).resolve()
MODEL_PATH = PROJECT_ROOT / os.getenv("MODEL_DIR") / os.getenv("MODEL_NAME")
LOG_PATH = PROJECT_ROOT / os.getenv("LOG_DIR") / os.getenv("LOG_NAME")

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_PATH)
    ]
)

# load the trained model only once (module-level cache)
model = load(MODEL_PATH)
logging.info("Model loaded successfully.")

movies = model['movies_df']
similarity_matrix = model['similarity_matrix']

def get_movie_recommendations(idx, cosine_sim_matrix, df, top_n=5):
    """
    Recommends top_n movies similar to the given movie index based on a cosine similarity matrix.

    Parameters:
    idx (int): The index of the movie you want recommendations for.
    cosine_sim_matrix (np.ndarray or pd.DataFrame): The precomputed cosine similarity matrix.
    df (pd.DataFrame): DataFrame containing the 'title' column.
    top_n (int): Number of recommendations to return.

    Returns:
    list: Titles of the recommended movies.
    """

    # Get the pairwise similarity scores for all movies with this movie
    # Note: If cosine_sim_matrix is a DataFrame, use .iloc[idx]
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))

    # Sort the movies based on the similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the top_n most similar movies
    # (Skip the first one since it's the movie itself, which has a similarity of 1.0)
    top_indices = [i[0] for i in sim_scores[1:top_n + 1]]

    return  top_indices


def predict(movie_name:str):

    # Check if the movie exists in the dataframe
    matching_movies = movies[movies['title'].str.lower() == movie_name.lower()]

    if matching_movies.empty:
        print(f"Error: '{movie_name}' not found in the dataset.")
        return {}
    else:
        # Get the index of the movie
        idx = matching_movies.index[0]

    
        indices = get_movie_recommendations(idx, similarity_matrix, movies, top_n=10)
        recommendations_titles = movies['title'].iloc[indices].tolist()
        recommendations_avg_ratings = movies['avg_rating'].iloc[indices].tolist()
        recommendations_year = movies['year'].iloc[indices].tolist()
        
        movie_genre = movies['genres'].iloc[idx]
        movie_year = movies['year'].iloc[idx]
        movie_avg_rating = movies['avg_rating'].iloc[idx]

        print(recommendations_titles)
        print(recommendations_year)

        return {
            'movie_name':movie_name,
            'movie_genre':movie_genre,
            'movie_year':movie_year,
            'movie_avg_rating':movie_avg_rating,
            'recommendations_titles':recommendations_titles,
            'recommendations_avg_ratings':recommendations_avg_ratings,
            'recommendations_year':recommendations_year,

        }

predict("Jumanzji")
