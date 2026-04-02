from flask import Flask, render_template
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, mean_squared_error, mean_absolute_error
import shap
import os

from model import get_model

app = Flask(__name__)

@app.route("/")
def home():
    model, X_test, y_test = get_model()

    y_pred = model.predict(X_test)

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure()
    sns.heatmap(cm, annot=True)
    plt.title("Confusion Matrix")
    plt.savefig("static/images/confusion.png")
    plt.close()

    # MSE & MAE (dummy example)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    # Plot MAE vs MSE
    plt.figure()
    plt.bar(["MAE", "MSE"], [mae, mse])
    plt.title("Error Metrics")
    plt.savefig("static/images/error.png")
    plt.close()

    # SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    shap.summary_plot(shap_values, X_test, show=False)
    plt.savefig("static/images/shap.png")
    plt.close()

    # Feature importance
    plt.figure()
    plt.bar(range(len(model.feature_importances_)), model.feature_importances_)
    plt.title("Feature Importance")
    plt.savefig("static/images/feature.png")
    plt.close()

    return render_template("index.html",
                           mse=mse,
                           mae=mae)

if __name__ == "__main__":
    app.run(debug=True)