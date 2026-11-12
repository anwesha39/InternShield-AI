
# ==========================================
# INTERNSHIELD AI
# EXPLORATORY DATA ANALYSIS
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("../dataset/fake_job_postings.csv")

# Display first five records
print("\nFIRST FIVE RECORDS")
print(df.head())

# Dataset dimensions
print("\nDATASET SHAPE")
print(df.shape)

# Column names
print("\nCOLUMN NAMES")
print(df.columns.tolist())

# Dataset information
print("\nDATASET INFORMATION")
df.info()

# Statistical summary
print("\nSTATISTICAL SUMMARY")
print(df.describe(include="all").T)

# Missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# Duplicate records
print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

# Target variable distribution
print("\nFAKE VS REAL JOB POSTINGS")
print(df["fraudulent"].value_counts())

print("\nPERCENTAGE DISTRIBUTION")
print(df["fraudulent"].value_counts(normalize=True) * 100)

# ==========================================
# END OF INITIAL EDA
# ==========================================

# ==========================================
# DATA VISUALIZATION
# ==========================================

import os

os.makedirs("../reports", exist_ok=True)

sns.set_theme(style="whitegrid")

# 1. Fake vs Genuine Job Postings
plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="fraudulent",
    hue="fraudulent",
    palette="Set2",
    legend=False
)

plt.title("Fake vs Genuine Job Postings")
plt.xlabel("Job Type (0 = Genuine, 1 = Fake)")
plt.ylabel("Number of Postings")
plt.xticks([0, 1], ["Genuine", "Fake"])

plt.tight_layout()
plt.savefig("../reports/job_distribution.png")
plt.show()


# 2. Missing Values
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=missing.values,
    y=missing.index,
    color="steelblue"
)

plt.title("Missing Values by Column")
plt.xlabel("Number of Missing Values")
plt.ylabel("Columns")

plt.tight_layout()
plt.savefig("../reports/missing_values.png")
plt.show()


# 3. Fraud Percentage
fraud_percentage = (
    df["fraudulent"].value_counts(normalize=True) * 100
)

plt.figure(figsize=(7, 7))

plt.pie(
    fraud_percentage,
    labels=["Genuine Jobs", "Fake Jobs"],
    autopct="%1.2f%%",
    startangle=90
)

plt.title("Percentage of Fake and Genuine Jobs")
plt.savefig("../reports/fraud_percentage.png")
plt.show()


# 4. Fraudulent Jobs by Employment Type
employment = df.groupby(
    "employment_type"
)["fraudulent"].mean().dropna() * 100

employment = employment.sort_values(ascending=False)

plt.figure(figsize=(10, 5))

sns.barplot(
    x=employment.index,
    y=employment.values,
    color="mediumpurple"
)

plt.title("Fraud Percentage by Employment Type")
plt.xlabel("Employment Type")
plt.ylabel("Fraudulent Postings (%)")
plt.xticks(rotation=30)

plt.tight_layout()
plt.savefig("../reports/employment_fraud.png")
plt.show()


# 5. Fraudulent Jobs by Company Logo
logo_fraud = df.groupby(
    "has_company_logo"
)["fraudulent"].mean() * 100

plt.figure(figsize=(8, 5))

sns.barplot(
    x=logo_fraud.index,
    y=logo_fraud.values,
    color="coral"
)

plt.title("Fraud Percentage by Company Logo")
plt.xlabel("Company Logo (0 = No, 1 = Yes)")
plt.ylabel("Fraudulent Postings (%)")

plt.tight_layout()
plt.savefig("../reports/logo_fraud.png")
plt.show()


print("\nALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
