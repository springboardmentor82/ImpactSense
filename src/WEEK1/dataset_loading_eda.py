# WEEK 1: Project Setup & Dataset Understanding
# Dataset Loading, Cleaning, EDA, Correlation Analysis

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def main():
    # 1. Load dataset
    df = pd.read_csv("../../data/earthquake.csv")
    print("Dataset loaded successfully")

    # 2. Basic understanding
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nDataset shape (rows, columns):")
    print(df.shape)
    print("\nColumn names:")
    print(df.columns)

    # 3. Dataset information & missing values
    print("\nDataset information:")
    print(df.info())
    print("\nMissing values in each column:")
    print(df.isnull().sum())

    # 4. Data cleaning (remove duplicates)
    print("\nOriginal dataset shape:", df.shape)
    df_cleaned = df.drop_duplicates()
    print("After removing duplicates:", df_cleaned.shape)

    # Save cleaned dataset
    df_cleaned.to_csv("../../data/earthquake_cleaned.csv", index=False)
    print("Cleaned dataset saved as earthquake_cleaned.csv")

    # 5. Exploratory Data Analysis (EDA)
    # Magnitude distribution
    plt.figure()
    sns.histplot(df_cleaned['magnitude'], bins=20)
    plt.title("Magnitude Distribution")
    plt.xlabel("Magnitude")
    plt.ylabel("Count")
    plt.show()

    # Depth distribution
    plt.figure()
    sns.histplot(df_cleaned['depth'], bins=20)
    plt.title("Depth Distribution")
    plt.xlabel("Depth")
    plt.ylabel("Count")
    plt.show()

    # Alert level distribution
    plt.figure()
    sns.countplot(x='alert', data=df_cleaned)
    plt.title("Alert Level Distribution")
    plt.xlabel("Alert")
    plt.ylabel("Count")
    plt.show()

    # 6. Correlation Analysis
    numeric_df = df_cleaned.select_dtypes(include=['float64', 'int64'])
    corr_matrix = numeric_df.corr()
    print("\nCorrelation Matrix:")
    print(corr_matrix)
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap of Earthquake Features")
    plt.show()

if __name__ == "__main__":
    main()