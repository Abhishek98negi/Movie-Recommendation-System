from fastapi import FastAPI
from pydantic import BaseModel

from backend.prediction import predict


app = FastAPI(
    title= "Movie Recommendation system",
    version="1.0.0"
)

# input schema matching training features
class Movie_input(BaseModel):
    movie_name:str


@app.get("/movie-input")
def movie_name():
    return {"status": "ok"}

@app.post("/predict-movies")
def predict_movies(input_data: Movie_input):
    input_data = input_data.model_dump()
    result = predict(input_data['movie_name'])
    if not result:
        return {}
    return {
        'movie_name':result['movie_name'],
        'movie_genre':result['movie_genre'],
        'movie_year':result['movie_year'],
        'movie_avg_rating':result['movie_avg_rating'],
        'recommendations_titles':result['recommendations_titles'],
        'recommendations_avg_ratings':result['recommendations_avg_ratings'],
        'recommendations_year':result['recommendations_year'],

    }


# uvicorn backend.main:app --reload
# http://127.0.0.1:8000/docs