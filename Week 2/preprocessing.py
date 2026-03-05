import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

df = pd.read_csv("earthquake_alert_balanced_dataset.csv")

# Checking & Dropping duplicates
print("Number of duplicated values: ", df.duplicated().sum())
print()
df = df.drop_duplicates()
print("After Dropping duplicates: ", df.shape)
print()

# checking null values
print(df.isnull().sum())
print()

# Label Encoding
print("Before Label Encoding: ", df['alert'].unique())
print()
le = LabelEncoder()
df['alert'] = le.fit_transform(df['alert'])
print("After Label Encoding: ",df['alert'].unique())
print()
print(df.head())
print()

# Separating features and target variable
x = df.drop('alert', axis=1)
y = df['alert']

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(x)
print(X_scaled[:5])
print()
print("Mean: ", X_scaled.mean())
print("Standard deviation: ", X_scaled.std())
print()

# Checking class Imbalance
print(y.value_counts())

# Creating final preprocessed dataset and saving to CSV
X_scaled_df = pd.DataFrame(X_scaled, columns=x.columns)

processed_df = X_scaled_df.copy()
processed_df['alert'] = y.values

processed_df.to_csv("preprocessed_data.csv", index=False)
