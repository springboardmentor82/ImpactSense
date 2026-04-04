# WEEK 3: Baseline Model Training
# Logistic Regression & Decision Tree

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
def main():

    # 1. Load train-test datasets
    X_train = pd.read_csv("../../data/X_train.csv")
    X_test  = pd.read_csv("../../data/X_test.csv")
    y_train = pd.read_csv("../../data/y_train.csv")
    y_test  = pd.read_csv("../../data/y_test.csv")
    print("Train-test data loaded successfully")

    # Convert target to 1D array
    y_train = y_train.values.ravel()
    y_test = y_test.values.ravel()

    # 2. Logistic Regression
    print("\n--- Logistic Regression Model ---")
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred_lr))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_lr))
    print("Classification Report:\n", classification_report(y_test, y_pred_lr))

    # 3. Decision Tree
    print("\n--- Decision Tree Model ---")
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    y_pred_dt = dt_model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred_dt))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_dt))
    print("Classification Report:\n", classification_report(y_test, y_pred_dt))

if __name__ == "__main__":
    main()