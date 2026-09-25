import streamlit as st
from recommender import recommend_by_movie, recommend_by_genre, get_movie_titles, get_genres


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)


# -----------------------------
# Header
# -----------------------------
st.title("🎬 CineMatch")
st.subheader("Movie Recommendation System")

st.write(
    "Discover movies you may enjoy using a content-based "
    "recommendation system powered by MovieLens data."
)

st.divider()


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("🎯 Recommendation Options")

option = st.sidebar.radio(
    "Choose how you want to discover movies:",
    ["Similar Movies", "Browse by Genre"]
)


# -----------------------------
# Similar Movies
# -----------------------------
if option == "Similar Movies":

    st.header("🍿 Find Similar Movies")

    movie_titles = get_movie_titles()

    selected_movie = st.selectbox(
        "Select a movie:",
        movie_titles
    )

    number_of_recommendations = st.slider(
        "Number of recommendations:",
        min_value=5,
        max_value=10,
        value=10
    )

    if st.button("🎬 Recommend Movies"):

        recommendations = recommend_by_movie(
            selected_movie,
            number_of_recommendations
        )

        st.subheader("Recommended Movies")

        if recommendations.empty:
            st.warning("No recommendations were found.")
        else:
            for _, movie in recommendations.iterrows():

                st.markdown(
                    f"### 🎥 {movie['title']}"
                )

                st.write(
                    f"Genre: {movie['genres']}"
                )

                st.write(
                    f"Average rating: ⭐ {movie['avg_rating']:.2f}"
                )

                st.divider()


# -----------------------------
# Browse by Genre
# -----------------------------
else:

    st.header("🎭 Browse Movies by Genre")

    genres = get_genres()

    selected_genre = st.selectbox(
        "Choose a genre:",
        genres
    )

    number_of_recommendations = st.slider(
        "Number of movies:",
        min_value=5,
        max_value=10,
        value=10
    )

    if st.button("🔎 Find Movies"):

        recommendations = recommend_by_genre(
            selected_genre,
            number_of_recommendations
        )

        st.subheader(
            f"Top {selected_genre} Movies"
        )

        if recommendations.empty:
            st.warning("No movies were found for this genre.")
        else:
            for _, movie in recommendations.iterrows():

                st.markdown(
                    f"### 🎥 {movie['title']}"
                )

                st.write(
                    f"Average rating: ⭐ {movie['avg_rating']:.2f}"
                )

                st.write(
                    f"Number of ratings: {movie['rating_count']}"
                )

                st.divider()


# -----------------------------
# Footer
# -----------------------------
st.caption(
    "CineMatch | BICT242 Data Scalability and Analytics Project"
)