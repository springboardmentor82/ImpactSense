#WEEK1-EXPLORATORY DATA ANALYSIS


# Import file upload module from Google Colab
from google.colab import files

# Upload dataset file manually
uploaded = files.upload()

# Import pandas for data handling
import pandas as pd

# Read the dataset (ZIP file containing CSV)
df = pd.read_csv("archive (1).zip")

# Display first 5 rows of dataset
print(df.head())

# Print number of rows and columns
print("Shape of dataset:", df.shape)

# Show column names
print("\nColumn names:")
print(df.columns)

# Show data types of each column
print("\nData types:")
print(df.dtypes)

# Again display first 5 rows (redundant but okay for verification)
print("\nFirst 5 rows:")
print(df.head())

# Check missing values in each column
print("Missing values in each column:")
print(df.isnull().sum())

# Get statistical summary of numerical columns
print(df.describe())

# Count values in 'alert' column (target variable)
print(df['alert'].value_counts())

# Plot bar graph of alert distribution
df['alert'].value_counts().plot(kind='bar')

# Import matplotlib for plotting
import matplotlib.pyplot as plt

# Add title and labels
plt.title("Alert Distribution")
plt.xlabel("Alert")
plt.ylabel("Count")

# Show the plot
plt.show()

# Import numpy for numerical operations
import numpy as np

# Create boxplots for all numerical columns
for col in df.select_dtypes(include=np.number):
    plt.figure()  # Create new figure for each column
    df.boxplot(column=col)
    plt.title(f"Boxplot of {col}")
    plt.show()

# Calculate correlation matrix (only numeric columns)
corr = df.corr(numeric_only=True)

# Print correlation values
print(corr)

# Visualize correlation matrix as heatmap
plt.imshow(corr)
plt.colorbar()

# Set x and y axis labels
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)

# Title of heatmap
plt.title("Correlation Heatmap")

# Show heatmap
plt.show()

# Create scatter matrix (pairwise relationships between features)
import pandas as pd
pd.plotting.scatter_matrix(df, figsize=(10,8))

# Show scatter plots
plt.show()