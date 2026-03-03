import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load dataset
df = pd.read_csv("../data/earthquake_dataset.csv")

print("Shape:", df.shape)

print("\nColumns:\n", df.columns)
df.head()

df.isnull().sum()
df.describe()

dup_count = df.duplicated().sum()
print("Duplicate rows:", int(dup_count))




cols = ['magnitude', 'depth', 'cdi', 'mmi', 'sig']

for col in cols:
    plt.figure(figsize=(5,3))
    sns.histplot(df[col], bins=40)
    plt.title(f"Distribution of {col}")
    plt.show()



plt.figure(figsize=(8,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title("Feature Correlation Heatmap")
plt.show()
