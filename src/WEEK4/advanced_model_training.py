# WEEK 4: Advanced Model Training
# Random Forest & Gradient Boosting

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# STEP 2: Load Train & Test Data

X_train = pd.read_csv("../../data/X_train.csv")
X_test  = pd.read_csv("../../data/X_test.csv")
y_train = pd.read_csv("../../data/y_train.csv")
y_test  = pd.read_csv("../../data/y_test.csv")
# Convert y to 1D array
y_train = y_train.values.ravel()
y_test = y_test.values.ravel()
print("Data loaded successfully")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)


# STEP 3: Random Forest Model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, y_pred_rf)
print("\nRandom Forest Accuracy:", rf_accuracy)


## STEP 4: Gradient Boosting with tuned parameters

from sklearn.ensemble import GradientBoostingClassifier
gb_model = GradientBoostingClassifier(
    learning_rate=0.05,
    max_depth=8,
    n_estimators=300,
    random_state=42
)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)
gb_accuracy = accuracy_score(y_test, y_pred_gb)
print("\nTuned Gradient Boosting Accuracy:", gb_accuracy)


# STEP 5: Cross-Validation (Random Forest)

from sklearn.model_selection import cross_val_score
rf_cv_scores = cross_val_score(
    rf_model,
    X_train,
    y_train,
    cv=5,
    scoring="accuracy"
)
print("\nRandom Forest Cross-Validation Scores:", rf_cv_scores)
print("Mean CV Accuracy:", rf_cv_scores.mean())


# STEP 6: Hyperparameter Tuning (Random Forest)

from sklearn.model_selection import GridSearchCV
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5],
}
grid_search = GridSearchCV(
    estimator=rf_model,
    param_grid=param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)
grid_search.fit(X_train, y_train)
best_rf = grid_search.best_estimator_
print("\nBest Parameters:", grid_search.best_params_)
print("Best Cross-Validation Accuracy:", grid_search.best_score_)


# Example predicition using the trained model with sample input
import pandas as pd
# Sample test input (5 features)
sample = pd.DataFrame([[7.02, 10.0, 9.0, 8.0, 26.011]], columns=X_train.columns)
sample_pred = gb_model.predict(sample)
print("\nSample Input Prediction:", sample_pred)