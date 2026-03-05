import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("earthquake_alert_balanced_dataset.csv")

print(df.head())
print()
df.info()
print()

print("Rows and Columns: ", df.shape)
print()
print("Column Names: ", df.columns)
print()
print(df.describe())
print()

# Earthquake Magnitude distribution
sns.histplot(df['magnitude'], bins=30)
plt.title("Earthquake Magnitude Distribution")
plt.show()

# Earthquake Depth distribution
sns.histplot(df['depth'], bins=30)
plt.title("Earthquake Depth Distribution")
plt.show()

# Magnitude Vs Depth 
plt.figure(figsize=(8, 6))
plt.scatter(df['depth'], df['magnitude'])
plt.xlabel('Depth')
plt.ylabel('Magnitude')
plt.title("Magnitude vs Depth")
plt.show()

#Box plot to show the range of values in all columns
df.boxplot(column=['magnitude','depth','cdi','mmi','sig'])
plt.title("Box plot")
plt.show()










