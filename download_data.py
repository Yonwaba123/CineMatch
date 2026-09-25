import os
import zipfile
import urllib.request


URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

DATA_FOLDER = "data"
ZIP_FILE = "movielens.zip"


print("Downloading MovieLens dataset...")

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

urllib.request.urlretrieve(URL, ZIP_FILE)

print("Download complete.")

os.makedirs(DATA_FOLDER, exist_ok=True)

print("Extracting dataset...")

with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
    zip_ref.extractall(".")

source_folder = os.path.join(
    "ml-latest-small"
)

movies_source = os.path.join(
    source_folder,
    "movies.csv"
)

ratings_source = os.path.join(
    source_folder,
    "ratings.csv"
)

os.replace(
    movies_source,
    os.path.join(DATA_FOLDER, "movies.csv")
)

os.replace(
    ratings_source,
    os.path.join(DATA_FOLDER, "ratings.csv")
)

# Remove downloaded ZIP file
os.remove(ZIP_FILE)

print("MovieLens dataset is ready.")

print("Movies file:", "data/movies.csv")
print("Ratings file:", "data/ratings.csv")