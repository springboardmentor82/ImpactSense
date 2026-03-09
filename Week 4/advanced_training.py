import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("preprocessed_data.csv")

X = df.drop("alert", axis=1)
y = df['alert']

#split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#Random Forest Classifier
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)
print("Random Forest Accuracy: ", accuracy_score(y_test, y_pred_rf))

# K-Fold Cross Validation for RF Classifier
scores = cross_val_score(rf_model, X, y, cv=5, scoring='accuracy')

print("Cross Validation Scores: ", scores)
print("Average Accuracy: ", scores.mean())

# Hyperparameter Tuning for RF Classifier
param_grid_rf = {
    'n_estimators': [100, 200],
    'max_depth' : [None, 10, 20],
    'min_samples_split' : [2, 5],
}
grid_search_rf = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid_rf,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid_search_rf.fit(X, y)

print("Best Parameters:", grid_search_rf.best_params_)
print()

# Gradient Boosting Classsifier
gb_model = GradientBoostingClassifier(random_state=42)
gb_model.fit(X_train, y_train)

y_pred_gb = gb_model.predict(X_test)
print("Gradient Boosting Accuracy: ", accuracy_score(y_test, y_pred_gb))

gb_scores = cross_val_score(gb_model, X, y, cv=5, scoring='accuracy')

# K-Fold Cross Validation for GB Classifier
print("Cross Validation Scores: ", gb_scores)
print("Average Accuracy: ", gb_scores.mean())

# Hyperparameter tuning for GB classifier
param_grid_gb = {
    'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1],
    'max_depth': [3, 5],
}

grid_Search_gb = GridSearchCV(
    GradientBoostingClassifier(random_state=42),
    param_grid_gb,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

grid_Search_gb.fit(X, y)

print("Best Parameters: ", grid_Search_gb.best_params_)
print()

#XGBoost
xgb = XGBClassifier(
    eval_metric = 'logloss',
)

xgb.fit(X_train, y_train)

y_pred_xgb = xgb.predict(X_test)

print("XGBoost Accuracy:", accuracy_score(y_test, y_pred_xgb))

# K-Fold Cross Validation for XG Boost
xgb_scores = cross_val_score(xgb, X, y, cv=5, scoring='accuracy')
print("XGBoost CV Accuracy: ", xgb_scores)
print("Average Accuracy: ", xgb_scores.mean())

# Hyperparameter tuning for XG Boost
param_grid_xgb = {
    'max_depth': [3, 5, 10],
    'learning_rate': [0.01, 0.1],
}

grid_search_xgb = GridSearchCV(
    xgb,
    param_grid_xgb,
    cv=5,
    scoring='accuracy',
)

grid_search_xgb.fit(X_train, y_train)

print("Best XGB Parameters: ", grid_search_xgb.best_params_)
print()

#Comparision table 
rf_basic = accuracy_score(y_test, y_pred_rf)
rf_cv = scores.mean()
rf_tuned = grid_search_rf.best_score_

gb_basic = accuracy_score(y_test, y_pred_gb)
gb_cv = gb_scores.mean()
gb_tuned = grid_Search_gb.best_score_ 

xgb_basic = accuracy_score(y_test, y_pred_xgb)
xgb_cv = xgb_scores.mean()
xgb_tuned = grid_search_xgb.best_score_

#Table Creation 
comparision = pd.DataFrame({
    "Model": ["Random Forest", "Gradient Boosting", "XGBoost"],
    "Basic Accuracy": [rf_basic, gb_basic, xgb_basic],
    "CV Accuracy": [rf_cv, gb_cv, xgb_cv],
    "Tuned Accuracy": [rf_tuned, gb_tuned, xgb_tuned]
})
print(comparision)





