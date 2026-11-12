
# ==========================================
# INTERNSHIELD AI
# DATA PREPROCESSING
# ==========================================

import pandas as pd
import re
import html
from pathlib import Path

# 1. Define dataset paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "dataset" / "fake_job_postings.csv"
OUTPUT_FILE = BASE_DIR / "dataset" / "processed_jobs.csv"

# 2. Load original dataset
print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print("Original dataset shape:", df.shape)

# 3. Remove duplicate records
print("\nRemoving duplicate records...")

duplicates = df.duplicated().sum()
df = df.drop_duplicates()

print("Duplicates removed:", duplicates)

# 4. Handle missing values in text columns
text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna("")

# 5. Handle missing categorical values
categorical_columns = [
    "location",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function"
]

for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].fillna("Not Specified")

# 6. Handle binary indicator columns
binary_columns = [
    "telecommuting",
    "has_company_logo",
    "has_questions"
]

for col in binary_columns:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# 7. Clean text data
def clean_text(text):

    text = html.unescape(str(text))

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Replace URLs and email addresses with indicators
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " URL ",
        text
    )

    text = re.sub(
        r"\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b",
        " EMAIL ",
        text
    )

    # Convert to lowercase
    text = text.lower()

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# 8. Create combined text column
print("\nCombining job information...")

feature_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "location",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function",
    "telecommuting",
    "has_company_logo",
    "has_questions"
]

available_columns = [
    col for col in feature_columns if col in df.columns
]

def combine_features(row):

    parts = []

    for col in available_columns:

        value = row[col]

        # Make column information explicit
        parts.append(f"{col}: {value}")

    combined = " ".join(parts)

    return clean_text(combined)


df["combined_text"] = df.apply(
    combine_features,
    axis=1
)

# 9. Validate target variable
print("\nValidating target variable...")

df["fraudulent"] = pd.to_numeric(
    df["fraudulent"],
    errors="coerce"
)

df = df.dropna(subset=["fraudulent"])

df["fraudulent"] = df["fraudulent"].astype(int)

# 10. Check processed data
print("\nPROCESSED DATASET INFORMATION")

print("Final shape:", df.shape)

print("\nTarget distribution:")
print(df["fraudulent"].value_counts())

print("\nMissing values in combined text:")
print(df["combined_text"].isnull().sum())

print("\nEmpty combined text records:")
print((df["combined_text"].str.len() == 0).sum())

# 11. Save processed dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nProcessed dataset saved successfully!")
print("Saved location:", OUTPUT_FILE)

print("\nDATA PREPROCESSING COMPLETED!")
