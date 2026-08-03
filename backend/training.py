import os
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from joblib import dump

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def train_model():
    try:    
        load_dotenv()

        PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT")).resolve()

        MOVIES_DATASET_PATH = PROJECT_ROOT / os.getenv("DATASET_DIR") / os.getenv("MOVIES_DATASET_NAME")
        RATINGS_DATASET_PATH = PROJECT_ROOT / os.getenv("DATASET_DIR") / os.getenv("RATINGS_DATASET_NAME")
        LINKS_DATASET_PATH = PROJECT_ROOT / os.getenv("DATASET_DIR") / os.getenv("LINKS_DATASET_NAME")

        MODEL_PATH = PROJECT_ROOT / os.getenv("MODEL_DIR") / os.getenv("MODEL_NAME")
        MOVIE_TITLES_PATH = PROJECT_ROOT / os.getenv("MODEL_DIR") / os.getenv("MOVIE_TITLES_NAME")
        LOG_PATH = PROJECT_ROOT / os.getenv("LOG_DIR") / os.getenv("LOG_NAME")


        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        MOVIE_TITLES_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(LOG_PATH)
            ]
        )

        movies = pd.read_csv(MOVIES_DATASET_PATH)
        ratings = pd.read_csv(RATINGS_DATASET_PATH)
        links = pd.read_csv(LINKS_DATASET_PATH)

        logging.info("Dataset loaded successfully")  

        # remove tmdbId from links
        links = links.drop(columns=['tmdbId'])

        movies['genres'] = movies['genres'].fillna('')
        movies['genres'] = movies['genres'].str.replace('|', ' ', regex=False)

        # Drop duplicates based on title
        movies = movies.drop_duplicates(subset=['title'])

        # Compute average rating upto one decimal place and reset index
        average_ratings = ratings.groupby('movieId')['rating'].mean().reset_index().round(1)

        # Optional: Rename column for clarity
        average_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)

        # Merge on 'movieId' to add the 'avg_rating' column
        # 'how="left"' ensures you keep all rows from your original movies dataframe
        movies = pd.merge(movies, average_ratings[['movieId', 'avg_rating']], on='movieId', how='left')

        # Extract movie name and year into separate columns
        movies[['title', 'year']] = movies['title'].str.extract(r'^(.*?)\s*\((\d{4})\)$')

        # Clean up whitespace if needed
        movies['title'] = movies['title'].str.strip()

        # Merge the imdbId column from links into movies based on 'movieId'
        movies = pd.merge(movies, links[['movieId', 'imdbId']], on='movieId', how='left')

        # save only movies names model
        dump(movies['title'], MOVIE_TITLES_PATH)
        logging.info(f"Model saved to: {MOVIE_TITLES_PATH}")
        
        # Convert text to vectors
        vectorizer = CountVectorizer()
        vector_matrix = vectorizer.fit_transform(movies['genres'])

        similarity_matrix = cosine_similarity(vector_matrix)

        bundle = {
            "movies_df":movies,
            "similarity_matrix": similarity_matrix
        }

    
        # save trained model
        dump(bundle, MODEL_PATH)
        logging.info(f"Model saved to: {MODEL_PATH}")

        logging.info("Training Script Completed")


    except Exception as e:
        print(f"Training failed: {e}")
        logging.exception(f"Training Script Failed: {e}")
        raise


if __name__ == "__main__":
    train_model()