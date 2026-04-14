#week 2 - Data Preprocessing    

# -------------------- FILE UPLOAD (GOOGLE COLAB) --------------------
from google.colab import files
uploaded = files.upload()

# -------------------- IMPORT LIBRARIES --------------------
import pandas as pd

# -------------------- LOAD DATA --------------------
# Reading dataset directly from zip (initial check)
df = pd.read_csv("archive (1).zip")

# Display first few rows
print(df.head())

# Check missing values
print(df.isnull().sum())

# -------------------- DATA CLEANING --------------------

# Fill missing numerical values with mean
df.fillna(df.mean(numeric_only=True), inplace=True)

# Fill missing categorical values with mode
for col in df.select_dtypes(include="object"):
    df[col].fillna(df[col].mode()[0], inplace=True)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Remove extra spaces in text columns
for col in df.select_dtypes(include="object"):
    df[col] = df[col].str.strip()

# Convert text to lowercase for consistency
for col in df.select_dtypes(include="object"):
    df[col] = df[col].str.lower()

print("Cleaning done")
print(df.info())
print(df.head())

# -------------------- EXTRACT ZIP FILE --------------------
import zipfile

# Extract dataset from zip file
with zipfile.ZipFile("archive (1).zip", "r") as zip_ref:
    zip_ref.extractall()

# Load extracted CSV file
df = pd.read_csv("earthquake_alert_balanced_dataset.csv")

print("Original dataset loaded")
print(df.head())

# -------------------- REMOVE DUPLICATES --------------------
df.drop_duplicates(inplace=True)

print("Duplicates removed")
print(df.shape)

# -------------------- DATA SPLITTING --------------------
# Split dataset into two halves
df1 = df.iloc[:len(df)//2]
df2 = df.iloc[len(df)//2:]

print("Two datasets created")
print("df1 shape:", df1.shape)
print("df2 shape:", df2.shape)

# -------------------- DATA INTEGRATION --------------------
# Combine both datasets again
combined_df = pd.concat([df1, df2], ignore_index=True)

print("Data integration completed")
print(combined_df.shape)
print(combined_df.head())

# -------------------- FEATURE SCALING --------------------
from sklearn.preprocessing import MinMaxScaler

# Select numerical columns
num_cols = combined_df.select_dtypes(include=["int64", "float64"]).columns

# Apply Min-Max Scaling
scaler = MinMaxScaler()
combined_df[num_cols] = scaler.fit_transform(combined_df[num_cols])

# -------------------- ENCODING CATEGORICAL DATA --------------------
from sklearn.preprocessing import LabelEncoder

cat_cols = combined_df.select_dtypes(include="object").columns

le = LabelEncoder()

# Convert categorical columns into numeric
for col in cat_cols:
    combined_df[col] = le.fit_transform(combined_df[col])

# -------------------- DATA TRANSFORMATION --------------------
import numpy as np

# Apply log transformation to reduce skewness
num_cols = combined_df.select_dtypes(include=["int64", "float64"]).columns
combined_df[num_cols] = np.log1p(combined_df[num_cols])

print("Data transformation completed")
print(combined_df.head())
print(combined_df.info())

# -------------------- FEATURE SELECTION --------------------
from sklearn.feature_selection import VarianceThreshold

# Remove low variance features
selector = VarianceThreshold(threshold=0.01)
reduced_data = selector.fit_transform(combined_df)

print("Feature selection completed")
print(reduced_data.shape)

# -------------------- DIMENSIONALITY REDUCTION --------------------
from sklearn.decomposition import PCA

# Reduce dataset to 5 principal components
pca = PCA(n_components=5)
pca_data = pca.fit_transform(combined_df)

print("PCA applied")
print(pca_data.shape)

# -------------------- SAVE PROCESSED DATA --------------------
# Save final processed dataset to Excel
combined_df.to_excel("processed_data.xlsx", index=False)

print("Data saved as Excel")