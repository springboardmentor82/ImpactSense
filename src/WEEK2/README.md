# Week 2: Data Preprocessing & Feature Engineering

## Objective
The objective of Week 2 is to preprocess the cleaned dataset and prepare it for machine learning by applying encoding, scaling, feature selection, and dataset splitting.

## Tasks Performed
- Loaded the cleaned earthquake dataset
- Encoded the categorical target variable (`alert`) using Label Encoding
- Normalized numerical features using StandardScaler
- Performed correlation analysis with the target variable
- Selected relevant features based on correlation threshold
- Split the dataset into training and testing sets (80:20 ratio)
- Saved intermediate and final datasets for reproducibility

## Generated Files
- `earthquake_encoded.csv` – Dataset after label encoding
- `earthquake_scaled.csv` – Dataset after feature scaling
- `earthquake_selected_features.csv` – Dataset after feature selection
- `earthquake_final.csv` – Final processed dataset
- `X_train.csv`, `X_test.csv` – Training and testing feature sets
- `y_train.csv`, `y_test.csv` – Training and testing target labels

## Outcome
- Dataset became fully cleaned and machine-learning ready
- Important features such as magnitude, depth, cdi, mmi, and sig were selected
- Final dataset prepared for baseline model training