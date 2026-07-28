import os
import requests
import streamlit as st
from dotenv import load_dotenv

# load .env to env vars
load_dotenv()
API_URL = os.getenv("API_URL")

# st.markdown('<style>.stApp {background-color: #26282A;}</style>',unsafe_allow_html=True)
# st.markdown('<span style="color: #F5F5F5;">Custom Coral Text</span>', unsafe_allow_html=True)
# st.markdown('<p style="color: purple; font-size: 24px;">Large Purple Paragraph</p>', unsafe_allow_html=True)
st.set_page_config(
    page_title="Predict movies",
    page_icon="🎬",
    layout="centered"
)


st.title("Movie Recommendation System 🎬")
st.write("An ML model to recommend movies for you.")

import pandas as pd


# Search bar
search_query = st.text_input("Search a movie name", value="")


if st.button("🔍"):
    input_data = {
        "movie_name": search_query
    }

    response = requests.post(API_URL, json=input_data)
    if response.status_code != 200:
        st.error("Something went wrong. Try again later...")

    else:
        result = response.json()
        if result:
            movie_name = result['movie_name']
            st.write(movie_name)
        else:
            st.error("Movie name not present in our database")

# streamlit run frontend/app.py