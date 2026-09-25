CineMatch 🎬



CineMatch is a Python-based movie recommendation system that recommends movies based on their genres and provides average movie ratings.



Project Overview



The system uses the MovieLens dataset to analyse movie genres and user ratings. It uses TF-IDF to convert movie genres into numerical features and cosine similarity to find movies with similar genre profiles.



The project also includes a Streamlit web application that allows users to select a movie and receive 10 recommended movies.



Technologies Used



\* Python

\* Pandas

\* NumPy

\* Scikit-learn

\* Streamlit

\* TF-IDF

\* Cosine Similarity

\* MovieLens Dataset



How It Works



1\. Movie and rating datasets are loaded.

2\. Movie genres are processed.

3\. TF-IDF converts genres into numerical feature vectors.

4\. Cosine similarity calculates how similar movies are.

5\. The system identifies the most similar movies.

6\. The Streamlit application displays 10 recommendations.

7\. Average user ratings are displayed for the recommended movies.



Model Evaluation



The recommendation system was evaluated using 97,365 comparisons.



Metric	Result

Mean Squared Error (MSE)	0.1745

Precision	1.0000

Recall	0.3714

F1-Score	0.5417



Project Files



\* app.py — Streamlit web application

\* recommender.py — Movie recommendation logic

\* evaluate\_model.py — Model evaluation

\* download\_data.py — Dataset download/setup

\* data/ — Movie and rating data

\* ml-latest-small/ — MovieLens dataset files



Running the Application



Install the required packages:



pip install pandas numpy scikit-learn streamlit



Then run:



python -m streamlit run app.py



The application will open in your browser.



Example



When a user selects Toy Story (1995), CineMatch can recommend movies such as:



\* Toy Story 2 (1999)

\* Monsters, Inc. (2001)

\* Antz (1998)

\* Moana (2016)

\* The Emperor’s New Groove (2000)



Project Status



CineMatch has been successfully tested and the project has been pushed to GitHub.

