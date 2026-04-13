import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, mean_absolute_error, mean_squared_error
import seaborn as sns
import matplotlib.pyplot as plt
import shap
import pickle

df = pd.read_csv("preprocessed_data.csv")

# Separating features and target variable
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

# Confusion matrix
cm = confusion_matrix(y_test, y_pred_rf)

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# MAE/MSE values
mae = mean_absolute_error(y_test, y_pred_rf)
mse = mean_squared_error(y_test, y_pred_rf)

print("MAE: ", mae)
print("MSE: ", mse)

errors = [mae, mse]
labels = ["MAE", "MSE"]

plt.bar(labels, errors)
plt.title("Error Metrics")
plt.ylabel("Error Value")
plt.show()

# Feature importance
importances = rf_model.feature_importances_
features = X.columns

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
})

importance_df = importance_df.sort_values(by="Importance", ascending=False)

plt.figure(figsize=(8,5))
plt.barh(importance_df["Feature"], importance_df["Importance"])
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.gca().invert_yaxis()
plt.show()

# Shap values
explainer = shap.Explainer(rf_model, X_train)

shap_values = explainer(X_test, check_additivity=False)
shap_values_class1 = shap_values[:, :, 1]

shap.plots.beeswarm(shap_values_class1)

pickle.dump(rf_model, open("earthquake_model.pkl", "wb"))


