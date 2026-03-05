import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, mean_absolute_error, classification_report


# Load the processed dataset
df = pd.read_csv("../data/earthquake_processed.csv")
print("Shape:", df.shape)
df.head()


# Check target variable distribution
df["alert"].value_counts()


# Encode Target
le = LabelEncoder()
df["alert_encoded"] = le.fit_transform(df["alert"])

df[["alert", "alert_encoded"]].head()

# Prepare Features (X) and Target (y)
X = df.drop(columns=["alert", "alert_encoded"])
y = df["alert_encoded"]

print("X shape:", X.shape)
print("y shape:", y.shape)


# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)


# feature scaling
num_cols = X_train.select_dtypes(include=np.number).columns

scaler = StandardScaler()

X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])


# Logistic Regression Model
log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)

y_pred_log = log_model.predict(X_test)

# Logistic Evaluation
log_acc = accuracy_score(y_test, y_pred_log)
log_mae = mean_absolute_error(y_test, y_pred_log)

print("Logistic Regression Accuracy:", log_acc)
print("Logistic Regression MAE:", log_mae)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred_log))


#Decision Tree Model
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

y_pred_dt = dt_model.predict(X_test)

# Decision Tree Evaluation
dt_acc = accuracy_score(y_test, y_pred_dt)
dt_mae = mean_absolute_error(y_test, y_pred_dt)

print("Decision Tree Accuracy:", dt_acc)
print("Decision Tree MAE:", dt_mae)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred_dt))


# Comparison of Models
comparison = pd.DataFrame({
    "Model": ["Logistic Regression", "Decision Tree"],
    "Accuracy (%)": [round(log_acc*100, 2), round(dt_acc*100, 2)],
    "MAE": [log_mae, dt_mae]
})

comparison