# WEEK 2: Preprocessing & Feature Engineering
# Encoding, Scaling, Feature Selection, Train-Test Split

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
def main():
    # 1. Load cleaned dataset
    df = pd.read_csv("../../data/earthquake_cleaned.csv")
    print("Cleaned dataset loaded successfully")

    # 2. Label Encoding (Categorical → Numeric)
    print("\nAlert values before encoding:")
    print(df['alert'].unique())
    label_encoder = LabelEncoder()
    df['alert_encoded'] = label_encoder.fit_transform(df['alert'])
    print("\nAlert Encoding Mapping:")
    for label, encoded in zip(label_encoder.classes_,
                              label_encoder.transform(label_encoder.classes_)):
        print(f"{label} -> {encoded}")

    df.to_csv("../../data/earthquake_encoded.csv", index=False)
    print("Encoded dataset saved as earthquake_encoded.csv")

    # 3. Feature Scaling (StandardScaler)
    feature_cols = ['magnitude', 'depth', 'cdi', 'mmi', 'sig']
    scaler = StandardScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    df.to_csv("../../data/earthquake_scaled.csv", index=False)
    print("Scaled dataset saved as earthquake_scaled.csv")

    # 4. Feature Selection (Correlation)

    df_numeric = df.drop(columns=['alert'])  # drop non-numeric
    corr_with_target = df_numeric.corr()['alert_encoded'].sort_values(ascending=False)
    print("\nCorrelation with target (alert_encoded):")
    print(corr_with_target)
    selected_features = corr_with_target[abs(corr_with_target) > 0.1].index.tolist()
    print("\nSelected features:")
    print(selected_features)
    df_selected = df_numeric[selected_features]
    df_selected.to_csv("../../data/earthquake_selected_features.csv", index=False)
    print("Selected features saved as earthquake_selected_features.csv")


    # 5. Train-Test Split

    X = df_selected.drop(columns=['alert_encoded'])
    y = df_selected['alert_encoded']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train.to_csv("../../data/X_train.csv", index=False)
    X_test.to_csv("../../data/X_test.csv", index=False)
    y_train.to_csv("../../data/y_train.csv", index=False)
    y_test.to_csv("../../data/y_test.csv", index=False)
    print("\nTrain-test split completed")
    print("Training shape:", X_train.shape)
    print("Testing shape:", X_test.shape)

    # Final dataset
    df_selected.to_csv("../../data/earthquake_final.csv", index=False)
    print("Final processed dataset saved as earthquake_final.csv")

if __name__ == "__main__":
    main()