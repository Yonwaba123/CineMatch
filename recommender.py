import os
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# File locations
# -----------------------------
MOVIES_FILE = os.path.join("data", "movies.csv")
RATINGS_FILE = os.path.join("data", "ratings.csv")


# -----------------------------
# Load MovieLens data
# -----------------------------
def load_data():
    if not os.path.exists(MOVIES_FILE):
        raise FileNotFoundError(
            "movies.csv was not found. Please download the MovieLens dataset first."
        )

    if not os.path.exists(RATINGS_FILE):
        raise FileNotFoundError(
            "ratings.csv was not found. Please download the MovieLens dataset first."
        )

    movies = pd.read_csv(MOVIES_FILE)
    ratings = pd.read_csv(RATINGS_FILE)

    return movies, ratings


# -----------------------------
# Prepare recommendation model
# -----------------------------
def prepare_model():
    movies, ratings = load_data()

    # Clean genre information
    movies["genres"] = movies["genres"].fillna(
        "Unknown"
    ).str.replace("|", " ", regex=False)

    # Create TF-IDF representation of movie genres
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        movies["genres"]
    )

    # Calculate similarity between movies
    similarity_matrix = cosine_similarity(
        tfidf_matrix,
        tfidf_matrix
    )

    # Calculate average rating and number of ratings
    rating_stats = (
        ratings.groupby("movieId")["rating"]
        .agg(["mean", "count"])
        .reset_index()
    )

    rating_stats.columns = [
        "movieId",
        "avg_rating",
        "rating_count"
    ]

    movies = movies.merge(
        rating_stats,
        on="movieId",
        how="left"
    )

    movies["avg_rating"] = movies[
        "avg_rating"
    ].fillna(0)

    movies["rating_count"] = movies[
        "rating_count"
    ].fillna(0)

    # Weighted rating
    minimum_ratings = 20
    global_average = ratings["rating"].mean()

    movies["weighted_rating"] = (
        (
            movies["rating_count"]
            / (
                movies["rating_count"]
                + minimum_ratings
            )
        )
        * movies["avg_rating"]
        +
        (
            minimum_ratings
            / (
                movies["rating_count"]
                + minimum_ratings
            )
        )
        * global_average
    )

    return movies, similarity_matrix


# -----------------------------
# Get movie titles
# -----------------------------
def get_movie_titles():
    movies, _ = load_data()

    return sorted(
        movies["title"].dropna().tolist()
    )


# -----------------------------
# Get available genres
# -----------------------------
def get_genres():
    movies, _ = load_data()

    genres = set()

    for genre_list in movies["genres"].fillna(""):
        for genre in genre_list.split("|"):
            if genre and genre != "(no genres listed)":
                genres.add(genre)

    return sorted(genres)


# -----------------------------
# Recommend similar movies
# -----------------------------
def recommend_by_movie(
    movie_title,
    number_of_recommendations=10
):
    movies, similarity_matrix = prepare_model()

    matches = movies[
        movies["title"] == movie_title
    ]

    if matches.empty:
        return pd.DataFrame()

    movie_index = matches.index[0]

    similarity_scores = list(
        enumerate(
            similarity_matrix[movie_index]
        )
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for index, similarity_score in similarity_scores[1:]:
        movie = movies.iloc[index]

        recommendations.append({
            "title": movie["title"],
            "genres": movie["genres"],
            "avg_rating": movie["avg_rating"],
            "rating_count": movie["rating_count"],
            "similarity": similarity_score
        })

    recommendations = pd.DataFrame(
        recommendations
    )

    if recommendations.empty:
        return recommendations

    # Normalize scores
    max_rating = recommendations[
        "avg_rating"
    ].max()

    if max_rating > 0:
        rating_score = (
            recommendations["avg_rating"]
            / max_rating
        )
    else:
        rating_score = 0

    # Combine similarity and rating quality
    recommendations["score"] = (
        0.80
        * recommendations["similarity"]
        + 0.20
        * rating_score
    )

    recommendations = recommendations.sort_values(
        "score",
        ascending=False
    )

    return recommendations.head(
        number_of_recommendations
    )


# -----------------------------
# Recommend movies by genre
# -----------------------------
def recommend_by_genre(
    genre,
    number_of_recommendations=10
):
    movies, _ = prepare_model()

    genre_movies = movies[
        movies["genres"].str.contains(
            genre,
            case=False,
            na=False
        )
    ].copy()

    if genre_movies.empty:
        return pd.DataFrame()

    genre_movies = genre_movies.sort_values(
        by=[
            "weighted_rating",
            "avg_rating",
            "rating_count"
        ],
        ascending=False
    )

    return genre_movies[
        [
            "title",
            "genres",
            "avg_rating",
            "rating_count"
        ]
    ].head(
        number_of_recommendations
    )