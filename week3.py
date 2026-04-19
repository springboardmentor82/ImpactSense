#Basic model training with Logistic Regression and Decision Tree Classifier using scikit-learn

# Import required libraries
import pandas as pd
import numpy as np

# For uploading file in Google Colab
from google.colab import files
uploaded = files.upload()

# Machine Learning libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# Evaluation metrics
from sklearn.metrics import accuracy_score, mean_absolute_error


# ==============================
# LOAD DATASET
# ==============================

# Get uploaded file name
file_name = list(uploaded.keys())[0]

# Read Excel file into pandas dataframe
df = pd.read_excel(file_name)


# ==============================
# DATA PREPROCESSING
# ==============================

# Separate features (X) and target variable (y)
X = df.iloc[:, :-1]   # All columns except last
y = df.iloc[:, -1]    # Last column (target)

# Convert categorical columns into numerical using one-hot encoding
X = pd.get_dummies(X)

# Replace infinite values with NaN
X = X.replace([np.inf, -np.inf], np.nan)

# Fill missing values with 0
X = X.fillna(0)

# Convert target into binary classification (0 or 1)
# Values above median → 1, below → 0
y = (y > y.median()).astype(int)


# ==============================
# SPLIT DATA
# ==============================

# Split dataset into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
)


# ==============================
# MODEL TRAINING
# ==============================

# Initialize Logistic Regression model
log_model = LogisticRegression(max_iter=1000)

# Initialize Decision Tree model
dt_model = DecisionTreeClassifier()

# Train Logistic Regression model
log_model.fit(X_train, y_train)

# Train Decision Tree model
dt_model.fit(X_train, y_train)


# ==============================
# PREDICTIONS
# ==============================

# Predict using Logistic Regression
y_pred_log = log_model.predict(X_test)

# Predict using Decision Tree
y_pred_dt = dt_model.predict(X_test)


# ==============================
# MODEL EVALUATION
# ==============================

# Calculate accuracy
print("Logistic Accuracy:", accuracy_score(y_test, y_pred_log))
print("Decision Tree Accuracy:", accuracy_score(y_test, y_pred_dt))

# Calculate Mean Absolute Error (MAE)
log_mae = mean_absolute_error(y_test, y_pred_log)
dt_mae = mean_absolute_error(y_test, y_pred_dt)

print("Logistic MAE:", log_mae)
print("Decision Tree MAE:", dt_mae)