# ImpactSense - Project Document

## 1. The Problem
Earthquake event data contains multiple technical parameters, but emergency operators and public-facing teams need clear and immediate impact interpretation. Existing raw reports can delay decisions because they are not directly mapped to operational risk categories.

## 2. Project Name
ImpactSense: Earthquake Impact Prediction System

## 3. Goal
Build an accurate and user-friendly system that predicts earthquake alert class and impact severity from seismic inputs, and serves results through a deployable web application.

## 4. Proposed Solution (Small Description)
Use supervised machine learning models trained on processed earthquake data to classify risk into Green, Yellow, Orange, and Red categories. Deploy the best-performing model in a web app that accepts seismic parameters, validates input, computes engineered features, and returns class probabilities, impact score, and risk level.

## 5. Implementation (Weekly Tasks)

### 5.1 Week 1
- Problem framing and requirement definition.
- Data source selection and project setup.

### 5.2 Week 2
- Exploratory Data Analysis using earthquake_eda.ipynb.
- Distribution checks, feature understanding, and label analysis.

### 5.3 Week 3
- Data preprocessing and feature engineering in earthquake_preprocessing.ipynb.
- Created model-ready dataset earthquake_processed.csv.

### 5.4 Week 4
- Baseline and advanced model training.
- Tuned Random Forest, Gradient Boosting, and XGBoost.
- Added custom Gradient Boosting model.
- Saved model artifacts to saved_models.

### 5.5 Week 5
- Model evaluation and explainability in earthquake_week5_evaluation_explainability.ipynb.
- Added confusion matrices, metrics, feature importance, and SHAP analysis.
- Updated workflow to load saved models instead of retraining.

### 5.6 Week 6
- Built web interface with landing, login, and predictor experience.
- Added visual risk outputs, class-color badge, and score rendering.

### 5.7 Week 7
- Added robustness and edge-case testing.
- Implemented serverless deployment structure for Vercel.
- Added API health check, tests endpoint, and improved deployment route handling.

## 6. Tech Stack Used
- Frontend: HTML, CSS, JavaScript (UI/public).
- Backend Local: Flask (UI/app.py).
- Backend Deployment: Vercel Serverless Python (UI/api).
- Data and Modeling: Python, pandas, numpy, scikit-learn, xgboost, shap, joblib.
- Model Artifacts: Pickle files in saved_models.
- Deployment: Vercel with vercel.json routing.

## 7. Conclusion
ImpactSense successfully delivers a complete ML lifecycle from data analysis to real-world deployment. The system provides fast, interpretable earthquake impact predictions and a practical user interface suitable for decision-support workflows. Its modular structure allows future expansion for improved model performance and broader hazard intelligence integration.

Live Website Link: https://impact-sense-nine.vercel.app/
