import os
import logging
import requests
import json
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from joblib import load


# load .env content to env vars
load_dotenv()
API_KEY = os.getenv("API_KEY")
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

def get_movie_recommendations(idx, cosine_sim_matrix, movies, top_n):
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
    # sim_scores: A sorted list of tuples (index, score)

    # Get the scores of the top_n most similar movies
    # (Skip the first one since it's the movie itself, which has a similarity of 1.0)
    top_indices = []
    i=0
    while len(top_indices)!=top_n:
        idx1 = sim_scores[i][0]
        if  movies['title'].iloc[idx] != movies['title'].iloc[idx1]:
            top_indices.append(idx1)
        i+=1

    # top_indices = [i[0] for i in sim_scores[0:top_n + 1]]
    # print(top_indices)
    return  top_indices



def get_poster_url(id, movie_name):
    # Pad a string with leading zeros to a total width of 8
    id = str(id).zfill(8)

    url = "http://www.omdbapi.com/?i=tt"+id+"&apikey="+API_KEY    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["Poster"], data['Title']

    return "",movie_name


from concurrent.futures import ThreadPoolExecutor
session = requests.Session()
def fetch_poster(imdb_id):
    imdb_id = str(imdb_id).zfill(8)
    url = f"http://www.omdbapi.com/?i=tt{imdb_id}&apikey={API_KEY}"

    try:
        response = session.get(url, timeout=5)
        data = response.json()
        return data.get("Poster")
    except Exception:
        return None


def predict(movie_name:str):

    # Check if the movie exists in the dataframe
    matching_movies = movies[movies['title'].str.lower() == movie_name.lower()]

    if matching_movies.empty:
        print(f"Error: '{movie_name}' not found in the dataset.")
        return {}
    else:
        # Get the index of the movie
        idx = matching_movies.index[0]

        indices = get_movie_recommendations(idx, similarity_matrix, movies, top_n=4)
        recommendations_titles = movies['title'].iloc[indices].tolist()
        recommendations_avg_ratings = movies['avg_rating'].iloc[indices].tolist()
        recommendations_year = movies['year'].iloc[indices].tolist()

        movie_name =  movies['title'].iloc[idx]
        imdb_id = int(movies['imdbId'].iloc[idx])       
        movie_genre = movies['genres'].iloc[idx]
        movie_year = movies['year'].iloc[idx]
        movie_avg_rating = movies['avg_rating'].iloc[idx]
        movie_poster = ""

        imdb_ids = movies['imdbId'].iloc[indices].tolist()
        imdb_ids.append(imdb_id)
        with ThreadPoolExecutor(max_workers=5) as executor:
            posters = list(executor.map(fetch_poster, imdb_ids))

        # print(posters)


        if movie_poster == "":
            movie_poster = "D:/My Learning/ML projects/Movie-Recommendation-System/frontend/default_image.jpeg"


        return {
            'movie_name':movie_name,
            'movie_posters':posters,
            'movie_genre':movie_genre,
            'movie_year':movie_year,
            'movie_avg_rating':movie_avg_rating,
            'recommendations_titles':recommendations_titles,
            'recommendations_avg_ratings':recommendations_avg_ratings,
            'recommendations_year':recommendations_year,

        }

# predict("Jumanji")
