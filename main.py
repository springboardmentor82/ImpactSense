"""
ImpactSense – Earthquake Impact Prediction
Machine Learning Project for Earthquake Risk Assessment

This project implements earthquake impact prediction using machine learning
algorithms to classify earthquakes into risk levels based on their characteristics.

Author: Earthquake Impact Prediction Team
Date: February 2026
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

def print_section_header(title):
    """Print a formatted section header for better readability."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def load_data():
    """
    Load the earthquake dataset from CSV file.
    
    Returns:
        pandas.DataFrame: Raw earthquake data
    """
    try:
        print("📂 Loading earthquake dataset...")
        data = pd.read_csv('data/earthquakes_2023_global.csv')
        print(f"✅ Dataset loaded successfully! Shape: {data.shape}")
        return data
    except FileNotFoundError:
        print("❌ Error: Dataset file not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

def preprocess_data(data):
    """
    Perform comprehensive data preprocessing and feature engineering.
    
    Args:
        data (pandas.DataFrame): Raw earthquake data
        
    Returns:
        tuple: Processed features (X) and target labels (y)
    """
    print_section_header("📌 WEEK 2 – DATA PREPROCESSING & FEATURE ENGINEERING")
    
    # Dataset Inspection
    print("🔍 Dataset Inspection:")
    print("\n📊 First 5 rows:")
    print(data.head())
    
    print("\n📋 Dataset Info:")
    print(f"Dataset shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    
    print("\n📈 Statistical Summary:")
    print(data.describe())
    
    # Select important features
    important_features = ['latitude', 'longitude', 'depth', 'mag']
    print(f"\n🎯 Selected features: {important_features}")
    
    # Check if all required columns exist
    missing_cols = [col for col in important_features if col not in data.columns]
    if missing_cols:
        print(f"❌ Missing columns: {missing_cols}")
        return None, None
    
    # Extract features
    df = data[important_features].copy()
    
    # Handle missing values
    print("\n🔧 Handling Missing Values:")
    missing_before = df.isnull().sum()
    print("Missing values before cleaning:")
    print(missing_before[missing_before > 0])
    
    # Fill missing values with median for numeric columns
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                print(f"  ✅ Filled {col} missing values with median: {median_val:.2f}")
    
    # Drop rows with remaining missing values if any
    df_clean = df.dropna()
    print(f"📊 Final dataset shape after cleaning: {df_clean.shape}")
    
    # Create risk_level target column
    print("\n🎯 Creating Risk Level Target:")
    def create_risk_level(magnitude):
        if magnitude < 4:
            return 'Low'
        elif magnitude < 6:
            return 'Medium'
        else:
            return 'High'
    
    df_clean['risk_level'] = df_clean['mag'].apply(create_risk_level)
    
    # Display risk level distribution
    risk_distribution = df_clean['risk_level'].value_counts()
    print("Risk Level Distribution:")
    for level, count in risk_distribution.items():
        percentage = (count / len(df_clean)) * 100
        print(f"  {level}: {count} samples ({percentage:.1f}%)")
    
    # Encode risk_level using LabelEncoder
    label_encoder = LabelEncoder()
    df_clean['risk_level_encoded'] = label_encoder.fit_transform(df_clean['risk_level'])
    
    print("\n🔤 Label Encoding Mapping:")
    for i, label in enumerate(label_encoder.classes_):
        print(f"  {label} → {i}")
    
    # Prepare features and target
    feature_columns = ['latitude', 'longitude', 'depth', 'mag']
    X = df_clean[feature_columns]
    y = df_clean['risk_level_encoded']
    
    # Scale numeric features using StandardScaler
    print("\n⚖️ Feature Scaling:")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=feature_columns, index=X.index)
    
    print("✅ Features scaled using StandardScaler")
    print("\nScaled feature statistics:")
    print(X_scaled.describe().round(3))
    
    # Store scaler and encoder for later use
    preprocess_data.scaler = scaler
    preprocess_data.label_encoder = label_encoder
    
    return X_scaled, y

def evaluate_model(y_true, y_pred, model_name):
    """
    Evaluate model performance with comprehensive metrics.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        model_name (str): Name of the model for display
    """
    accuracy = accuracy_score(y_true, y_pred)
    print(f"\n📊 {model_name} Performance:")
    print(f"  Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    print(f"\n📋 Classification Report for {model_name}:")
    class_names = preprocess_data.label_encoder.classes_
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    return accuracy

def train_baseline_models(X_train, X_test, y_train, y_test):
    """
    Train and evaluate baseline machine learning models.
    
    Args:
        X_train, X_test: Training and testing features
        y_train, y_test: Training and testing labels
        
    Returns:
        dict: Dictionary containing trained models and their accuracies
    """
    print_section_header("📌 WEEK 3 – BASELINE MODEL TRAINING")
    
    models = {}
    accuracies = {}
    
    # 1. Logistic Regression
    print("\n🔵 Training Logistic Regression...")
    lr_model = LogisticRegression(random_state=42, max_iter=1000)
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_accuracy = evaluate_model(y_test, lr_pred, "Logistic Regression")
    
    models['Logistic Regression'] = lr_model
    accuracies['Logistic Regression'] = lr_accuracy
    
    # 2. Decision Tree Classifier
    print("\n🌲 Training Decision Tree Classifier...")
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    dt_pred = dt_model.predict(X_test)
    dt_accuracy = evaluate_model(y_test, dt_pred, "Decision Tree")
    
    models['Decision Tree'] = dt_model
    accuracies['Decision Tree'] = dt_accuracy
    
    # Display confusion matrices for baseline models
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    class_names = preprocess_data.label_encoder.classes_
    
    # Logistic Regression Confusion Matrix
    cm_lr = confusion_matrix(y_test, lr_pred)
    sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names, ax=axes[0])
    axes[0].set_title('Logistic Regression\nConfusion Matrix')
    axes[0].set_ylabel('True Label')
    axes[0].set_xlabel('Predicted Label')
    
    # Decision Tree Confusion Matrix  
    cm_dt = confusion_matrix(y_test, dt_pred)
    sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Greens',
                xticklabels=class_names, yticklabels=class_names, ax=axes[1])
    axes[1].set_title('Decision Tree\nConfusion Matrix')
    axes[1].set_ylabel('True Label')
    axes[1].set_xlabel('Predicted Label')
    
    plt.tight_layout()
    plt.savefig('baseline_models_confusion_matrices.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Performance Comparison
    print("\n📈 BASELINE MODELS PERFORMANCE COMPARISON:")
    print("-" * 50)
    for model_name, accuracy in accuracies.items():
        print(f"{model_name:20}: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    return models, accuracies

def train_advanced_models(X_train, X_test, y_train, y_test):
    """
    Train and evaluate advanced machine learning models with cross-validation.
    
    Args:
        X_train, X_test: Training and testing features
        y_train, y_test: Training and testing labels
        
    Returns:
        dict: Dictionary containing trained models and their performance metrics
    """
    print_section_header("📌 WEEK 4 – ADVANCED MODEL TRAINING")
    
    advanced_models = {}
    advanced_accuracies = {}
    cv_scores = {}
    
    # 1. Random Forest Classifier
    print("\n🌳 Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = evaluate_model(y_test, rf_pred, "Random Forest")
    
    # Cross-validation for Random Forest
    rf_cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5)
    cv_scores['Random Forest'] = rf_cv_scores
    print(f"  Cross-validation scores: {rf_cv_scores}")
    print(f"  Mean CV accuracy: {rf_cv_scores.mean():.4f} (±{rf_cv_scores.std()*2:.4f})")
    
    advanced_models['Random Forest'] = rf_model
    advanced_accuracies['Random Forest'] = rf_accuracy
    
    # 2. Gradient Boosting Classifier
    print("\n🚀 Training Gradient Boosting Classifier...")
    gb_model = GradientBoostingClassifier(random_state=42)
    gb_model.fit(X_train, y_train)
    gb_pred = gb_model.predict(X_test)
    gb_accuracy = evaluate_model(y_test, gb_pred, "Gradient Boosting")
    
    # Cross-validation for Gradient Boosting
    gb_cv_scores = cross_val_score(gb_model, X_train, y_train, cv=5)
    cv_scores['Gradient Boosting'] = gb_cv_scores
    print(f"  Cross-validation scores: {gb_cv_scores}")
    print(f"  Mean CV accuracy: {gb_cv_scores.mean():.4f} (±{gb_cv_scores.std()*2:.4f})")
    
    advanced_models['Gradient Boosting'] = gb_model
    advanced_accuracies['Gradient Boosting'] = gb_accuracy
    
    # Find best performing model
    best_model_name = max(advanced_accuracies, key=advanced_accuracies.get)
    best_model = advanced_models[best_model_name]
    best_accuracy = advanced_accuracies[best_model_name]
    
    print(f"\n🏆 Best performing model: {best_model_name} (Accuracy: {best_accuracy:.4f})")
    
    # Visualizations
    create_advanced_visualizations(X_test, y_test, rf_model, gb_model, 
                                 best_model_name, advanced_models, cv_scores)
    
    return advanced_models, advanced_accuracies, cv_scores

def create_advanced_visualizations(X_test, y_test, rf_model, gb_model, 
                                 best_model_name, models, cv_scores):
    """
    Create comprehensive visualizations for advanced models.
    
    Args:
        X_test: Test features
        y_test: Test labels  
        rf_model: Trained Random Forest model
        gb_model: Trained Gradient Boosting model
        best_model_name: Name of best performing model
        models: Dictionary of trained models
        cv_scores: Cross-validation scores
    """
    class_names = preprocess_data.label_encoder.classes_
    
    # Create subplot figure
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Confusion Matrix for Best Model
    ax1 = plt.subplot(2, 3, 1)
    best_model = models[best_model_name]
    best_pred = best_model.predict(X_test)
    cm_best = confusion_matrix(y_test, best_pred)
    sns.heatmap(cm_best, annot=True, fmt='d', cmap='viridis',
                xticklabels=class_names, yticklabels=class_names)
    plt.title(f'{best_model_name}\nConfusion Matrix (Best Model)')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    # 2. Feature Importance (Random Forest)
    ax2 = plt.subplot(2, 3, 2)
    feature_names = ['Latitude', 'Longitude', 'Depth', 'Magnitude']
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    bars = plt.bar(range(len(importances)), importances[indices], color=colors)
    plt.title('Random Forest\nFeature Importance')
    plt.xlabel('Features')
    plt.ylabel('Importance Score')
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    # 3. Cross-Validation Scores Comparison
    ax3 = plt.subplot(2, 3, 3)
    cv_means = [scores.mean() for scores in cv_scores.values()]
    cv_stds = [scores.std() for scores in cv_scores.values()]
    model_names = list(cv_scores.keys())
    
    x_pos = np.arange(len(model_names))
    bars = plt.bar(x_pos, cv_means, yerr=cv_stds, capsize=5, 
                   color=['#FF9999', '#66B2FF'], alpha=0.8)
    plt.title('5-Fold Cross-Validation\nAccuracy Comparison')
    plt.xlabel('Models')
    plt.ylabel('CV Accuracy')
    plt.xticks(x_pos, model_names, rotation=15)
    plt.ylim(0, 1)
    
    # Add value labels on bars
    for i, (bar, mean, std) in enumerate(zip(bars, cv_means, cv_stds)):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + std + 0.02,
                f'{mean:.3f}±{std:.3f}', ha='center', va='bottom', fontsize=9)
    
    # 4. Model Accuracy Comparison (All models)
    ax4 = plt.subplot(2, 3, 4)
    all_models = ['Logistic Regression', 'Decision Tree', 'Random Forest', 'Gradient Boosting']
    
    # Get accuracies from both baseline and advanced models
    lr_acc = train_baseline_models.baseline_accuracies.get('Logistic Regression', 0)
    dt_acc = train_baseline_models.baseline_accuracies.get('Decision Tree', 0)
    rf_acc = accuracy_score(y_test, rf_model.predict(X_test))
    gb_acc = accuracy_score(y_test, gb_model.predict(X_test))
    
    all_accuracies = [lr_acc, dt_acc, rf_acc, gb_acc]
    colors = ['#FFB6C1', '#98FB98', '#87CEEB', '#DDA0DD']
    
    bars = plt.bar(all_models, all_accuracies, color=colors, alpha=0.8)
    plt.title('All Models Accuracy\nComparison')
    plt.xlabel('Models')
    plt.ylabel('Test Accuracy')
    plt.xticks(rotation=45)
    plt.ylim(0, 1)
    
    # Add value labels on bars
    for bar, acc in zip(bars, all_accuracies):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{acc:.3f}', ha='center', va='bottom')
    
    # 5. Risk Level Distribution
    ax5 = plt.subplot(2, 3, 5)
    class_names = preprocess_data.label_encoder.classes_
    y_test_decoded = preprocess_data.label_encoder.inverse_transform(y_test)
    risk_counts = pd.Series(y_test_decoded).value_counts()
    
    colors = ['#FF6B6B', '#FFD93D', '#6BCF7F']
    wedges, texts, autotexts = plt.pie(risk_counts.values, labels=risk_counts.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Test Set Risk Level\nDistribution')
    
    # 6. Learning Curves (Training vs Validation Accuracy)
    ax6 = plt.subplot(2, 3, 6)
    
    # Simulate learning curves by training on different data sizes
    train_sizes = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    rf_train_scores = []
    rf_val_scores = []
    
    from sklearn.model_selection import train_test_split
    
    for size in train_sizes:
        if size == 1.0:
            X_temp, y_temp = X_test.iloc[:int(len(X_test) * 0.8)], y_test.iloc[:int(len(y_test) * 0.8)]
        else:
            X_temp, _, y_temp, _ = train_test_split(X_test.iloc[:int(len(X_test) * 0.8)], 
                                                   y_test.iloc[:int(len(y_test) * 0.8)], 
                                                   train_size=size, random_state=42)
        
        # Train model on subset
        temp_model = RandomForestClassifier(n_estimators=50, random_state=42)
        temp_model.fit(X_temp, y_temp)
        
        # Calculate scores
        train_score = temp_model.score(X_temp, y_temp)
        val_score = temp_model.score(X_test.iloc[int(len(X_test) * 0.8):], 
                                   y_test.iloc[int(len(y_test) * 0.8):])
        
        rf_train_scores.append(train_score)
        rf_val_scores.append(val_score)
    
    plt.plot(train_sizes, rf_train_scores, 'o-', color='#FF6B6B', 
             label='Training Accuracy', linewidth=2, markersize=6)
    plt.plot(train_sizes, rf_val_scores, 's-', color='#4ECDC4', 
             label='Validation Accuracy', linewidth=2, markersize=6)
    plt.title('Learning Curves\n(Random Forest)')
    plt.xlabel('Training Set Size')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0.5, 1.0)
    
    plt.tight_layout()
    plt.savefig('advanced_models_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """
    Main function to execute the complete earthquake impact prediction pipeline.
    """
    print("🌍 ImpactSense – Earthquake Impact Prediction")
    print("=" * 60)
    print("Machine Learning Project for Earthquake Risk Assessment")
    print("Implemented: Week 2, Week 3, Week 4 modules")
    
    # Load data
    data = load_data()
    if data is None:
        return
    
    # Preprocess data
    X, y = preprocess_data(data)
    if X is None or y is None:
        print("❌ Data preprocessing failed. Please check your dataset.")
        return
    
    # Split dataset into training and testing sets (80-20 split)
    print(f"\n🔄 Splitting dataset: 80% training, 20% testing")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Testing set: {X_test.shape[0]} samples")
    
    # Train baseline models (Week 3)
    baseline_models, baseline_accuracies = train_baseline_models(X_train, X_test, y_train, y_test)
    
    # Store baseline accuracies for later use in visualizations
    train_baseline_models.baseline_accuracies = baseline_accuracies
    
    # Train advanced models (Week 4)  
    advanced_models, advanced_accuracies, cv_scores = train_advanced_models(X_train, X_test, y_train, y_test)
    
    # Final Summary
    print_section_header("📊 FINAL RESULTS SUMMARY")
    
    print("\n🏆 ALL MODELS PERFORMANCE RANKING:")
    print("-" * 50)
    
    # Combine all accuracies
    all_results = {**baseline_accuracies, **advanced_accuracies}
    sorted_results = sorted(all_results.items(), key=lambda x: x[1], reverse=True)
    
    for rank, (model_name, accuracy) in enumerate(sorted_results, 1):
        stars = "⭐" * min(rank, 3)  # Show stars for top 3
        print(f"{rank}. {model_name:20}: {accuracy:.4f} ({accuracy*100:.2f}%) {stars}")
    
    print(f"\n🎯 Best Model: {sorted_results[0][0]}")
    print(f"   Final Accuracy: {sorted_results[0][1]:.4f} ({sorted_results[0][1]*100:.2f}%)")
    
    # Cross-validation summary
    print(f"\n📈 Cross-Validation Results:")
    for model_name, scores in cv_scores.items():
        print(f"  {model_name}: {scores.mean():.4f} (±{scores.std()*2:.4f})")
    
    print(f"\n✅ Analysis complete! Check generated visualization files:")
    print(f"   📊 baseline_models_confusion_matrices.png")
    print(f"   📊 advanced_models_analysis.png")
    
    print(f"\n🎉 ImpactSense Earthquake Impact Prediction - Successfully Completed!")

# Execute the main function when script is run directly
if __name__ == "__main__":
    main()