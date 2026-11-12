
# ==========================================
# INTERNSHIELD AI
# CONSISTENT TEXT FEATURE EXTRACTION
# ==========================================

import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "dataset" / "processed_jobs.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

# Use only the description field because
# the website currently accepts free text.
# This makes training and inference consistent.

X = df["description"].fillna("").astype(str)
y = df["fraudulent"].astype(int)

# Remove empty descriptions

valid = X.str.strip().ne("")

X = X[valid]
y = y[valid]

print("Valid records:", len(X))
print("\nClass distribution:")
print(y.value_counts())

# Stratified split

X_train_text, X_test_text, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train_text))
print("Testing records:", len(X_test_text))

# TF-IDF

vectorizer = TfidfVectorizer(
    max_features=30000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    dtype="float32"
)

X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)

print("\nTraining matrix:", X_train.shape)
print("Testing matrix:", X_test.shape)

# Save vectorizer

joblib.dump(
    vectorizer,
    MODEL_DIR / "tfidf_vectorizer.joblib"
)

# Save data

feature_data = {
    "X_train": X_train,
    "X_test": X_test,
    "y_train": y_train.to_numpy(),
    "y_test": y_test.to_numpy()
}

joblib.dump(
    feature_data,
    MODEL_DIR / "tfidf_features.joblib",
    compress=3
)

print("\nFeature extraction completed!")
