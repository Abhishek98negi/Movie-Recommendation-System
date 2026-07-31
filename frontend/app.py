import os
import requests
import streamlit as st
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from streamlit_searchbox import st_searchbox
from joblib import load

# load .env to env vars
load_dotenv()

API_URL = os.getenv("API_URL")

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT")).resolve()
MOVIE_TITLES_PATH = PROJECT_ROOT / os.getenv("MODEL_DIR") / os.getenv("MOVIE_TITLES_NAME")

model = load(MOVIE_TITLES_PATH)
movies = model.tolist()
# print(movies[:10])

filtered_list = [item for item in movies if isinstance(item, str)]
# print(all(isinstance(x, str) for x in filtered_list))
movies = [word.lower() for word in filtered_list]

st.set_page_config(
    page_title="Predict movies",
    page_icon="🎬",
    layout="centered"
)


st.title("Movie Recommendation System 🎬")
st.write("An ML model to recommend movies for you.")

# Define a function that returns list of strings based on current search term
def search_fruits(search_term: str):
    if not search_term:
        return []

    return [f for f in movies if search_term.lower() in f]

# Render the search box
selected_value = st_searchbox(
    search_fruits,
    placeholder="Search Movies",
)


if selected_value!=None:
    input_data = {
        "movie_name": selected_value
    }

    response = requests.post(API_URL, json=input_data)
    if response.status_code != 200:
        st.error("Something went wrong. Try again later...")

    else:
        result = response.json()
        if result:
            movie_name = result['movie_name']
            movie_genre = result['movie_genre']
            movie_year = result['movie_year']
            movie_avg_rating = result['movie_avg_rating'],
            recommendations_titles = result['recommendations_titles'],
            recommendations_avg_ratings = result['recommendations_avg_ratings'],
            recommendations_year = result['recommendations_year'],

            st.write(f'{movie_name} ({movie_year})')
            st.write(f'Genre: {movie_genre}')
            st.write(f'⭐{movie_avg_rating[0]}/5')
            st.divider()


            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f'{recommendations_titles[0][0]} ({recommendations_year[0][0]})')
                st.write(f'⭐{recommendations_avg_ratings[0][0]}/5')
                st.divider()
                st.write(f'{recommendations_titles[0][1]} ({recommendations_year[0][1]})')
                st.write(f'⭐{recommendations_avg_ratings[0][1]}/5')

            with col2:
                st.write(f'{recommendations_titles[0][2]} ({recommendations_year[0][2]})')
                st.write(f'⭐{recommendations_avg_ratings[0][2]}/5')
                st.divider()
                st.write(f'{recommendations_titles[0][3]} ({recommendations_year[0][3]})')
                st.write(f'⭐{recommendations_avg_ratings[0][3]}/5')
            
            with col3:
                st.write(f'{recommendations_titles[0][4]} ({recommendations_year[0][4]})')
                st.write(f'⭐{recommendations_avg_ratings[0][4]}/5')
                st.divider()
                st.write(f'{recommendations_titles[0][5]} ({recommendations_year[0][5]})')
                st.write(f'⭐{recommendations_avg_ratings[0][5]}/5')


        else:
            st.error("Movie name not present in our database")

# streamlit run frontend/app.py