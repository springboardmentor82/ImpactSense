import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler

# load raw dataset
df = pd.read_csv("../data/earthquake_dataset.csv")

print("Shape:", df.shape)
df.head()

# check missing values
missing_values = df.isnull().sum().sort_values(ascending=False)
missing_values
num_cols = df.select_dtypes(include=np.number).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

cat_cols = df.select_dtypes(include="object").columns
df[cat_cols] = df[cat_cols].apply(lambda x: x.fillna(x.mode()[0]))


df.isnull().sum().sum()


# check duplicates
print("Before removing duplicates:", df.shape)

df.drop_duplicates(inplace=True)

print("After removing duplicates:", df.shape)


# Create new features based on existing ones
if "latitude" in df.columns:
    df["abs_latitude"] = df["latitude"].abs()

if "longitude" in df.columns:
    df["abs_longitude"] = df["longitude"].abs()




numeric_cols = df.select_dtypes(include=np.number).columns

scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

df.head()


# Save the processed dataset
df.to_csv("../data/earthquake_processed.csv", index=False)

print("Processed dataset saved successfully.")