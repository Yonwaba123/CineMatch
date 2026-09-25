import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error, precision_score, recall_score, f1_score
import numpy as np

print("Loading movie dataset...")

movies = pd.read_csv("data/movies.csv")

# Replace missing genres
movies["genres"] = movies["genres"].fillna("")

print("Preparing movie features...")

# Convert genres into numerical TF-IDF features
tfidf = TfidfVectorizer(stop_words="english")

tfidf_matrix = tfidf.fit_transform(movies["genres"])

# Calculate similarity between movies
similarity_matrix = cosine_similarity(tfidf_matrix)

print("Calculating evaluation results...")

# We use similarity scores as the predicted values.
# For evaluation, movies with the same genre are treated as relevant.
actual = []
predicted = []

for i in range(len(movies)):
    for j in range(i + 1, min(i + 11, len(movies))):

        # Actual relationship:
        # 1 = movies share at least one genre
        # 0 = they do not
        genres_i = set(movies.iloc[i]["genres"].split("|"))
        genres_j = set(movies.iloc[j]["genres"].split("|"))

        if genres_i.intersection(genres_j):
            actual.append(1)
        else:
            actual.append(0)

        # Predicted similarity
        predicted.append(similarity_matrix[i][j])

# Calculate Mean Squared Error
mse = mean_squared_error(actual, predicted)
# Convert similarity scores into predictions
predicted_labels = [1 if score >= 0.5 else 0 for score in predicted]

# Calculate classification metrics
precision = precision_score(actual, predicted_labels, zero_division=0)
recall = recall_score(actual, predicted_labels, zero_division=0)
f1 = f1_score(actual, predicted_labels, zero_division=0)

print()
print("====================================")
print("CINEMATCH MODEL EVALUATION")
print("====================================")
print(f"Number of comparisons: {len(actual)}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print("====================================")

print()
print("Evaluation completed successfully!")