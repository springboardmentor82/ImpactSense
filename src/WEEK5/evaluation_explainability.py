# Week 5: Evaluation & Explainability

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, mean_absolute_error, mean_squared_error
from sklearn.ensemble import GradientBoostingClassifier  

## Load datasets
X_train = pd.read_csv("../../data/X_train.csv")
X_test = pd.read_csv("../../data/X_test.csv")
y_train = pd.read_csv("../../data/y_train.csv")
y_test = pd.read_csv("../../data/y_test.csv")
y_train = y_train.values.ravel()
y_test = y_test.values.ravel()
print("Data loaded successfully")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)


## Train Gradient Boosting Model
gb_model = GradientBoostingClassifier(
    learning_rate=0.05,
    max_depth=8,
    n_estimators=300,
    random_state=42
)
gb_model.fit(X_train, y_train)
y_pred = gb_model.predict(X_test)
print("Model trained successfully")


## Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.savefig("../../outputs/WEEK5/confusion_matrix.png")
plt.show()
print("Confusion matrix generated")


## Error Metrics (MAE & MSE)
from sklearn.metrics import mean_absolute_error, mean_squared_error
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("MAE:", mae)
print("MSE:", mse)


## Import matplotlib to plot MAE and MSE error metrics
import matplotlib.pyplot as plt
values = [mae, mse]
labels = ["MAE", "MSE"]
plt.figure(figsize=(5,5))
plt.bar(labels, values)
plt.title("Error Metrics")
plt.ylabel("Value")

plt.savefig("../../outputs/WEEK5/error_metrics.png")
plt.show()
print("MAE/MSE plot generated")


## Feature Importance Analysis
import pandas as pd
importances = gb_model.feature_importances_
feature_names = X_train.columns
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})
importance_df = importance_df.sort_values(by="Importance", ascending=False)
plt.figure(figsize=(8,5))
plt.barh(importance_df["Feature"], importance_df["Importance"])
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Feature")

plt.savefig("../../outputs/WEEK5/feature_importance.png")
plt.show()

print("Feature importance plot generated")


## SHAP Explainability Analysis
import shap
import numpy as np
background = X_train.sample(50)
explainer = shap.KernelExplainer(gb_model.predict, background)
shap_values = explainer.shap_values(X_test[:50])
shap.summary_plot(shap_values, X_test[:50], show=False)

plt.savefig("../../outputs/WEEK5/shap_summary.png")
plt.show()
print("SHAP explainability plot generated")