"""
Week 3: Baseline Model Training
ImpactSense - Earthquake Impact Prediction

This module trains baseline ML models (Logistic Regression & Decision Tree)
and evaluates their performance for earthquake risk classification.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import sys
import os

# Add parent directory to path to import week2 module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Week2-Data-Preprocessing.week2_preprocessing import main as week2_preprocessing

def split_dataset(X, y, test_size=0.2, random_state=42):
    """
    Split dataset into training and testing sets.
    
    Args:
        X: Features
        y: Target labels
        test_size: Proportion for testing
        random_state: Random seed for reproducibility
        
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    print(f"🔄 DATASET SPLITTING")
    print("=" * 50)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"Training set: {X_train.shape[0]} samples ({(1-test_size)*100:.0f}%)")
    print(f"Testing set: {X_test.shape[0]} samples ({test_size*100:.0f}%)")
    
    return X_train, X_test, y_train, y_test

def evaluate_model_performance(y_true, y_pred, model_name, label_encoder):
    """
    Evaluate and display model performance metrics.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        model_name: Name of the model
        label_encoder: LabelEncoder for class names
        
    Returns:
        float: Model accuracy
    """
    accuracy = accuracy_score(y_true, y_pred)
    print(f"\n📊 {model_name.upper()} PERFORMANCE:")
    print("-" * 40)
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    print(f"\n📋 Classification Report:")
    class_names = label_encoder.classes_
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    return accuracy

def train_logistic_regression(X_train, y_train):
    """
    Train Logistic Regression model.
    
    Args:
        X_train: Training features
        y_train: Training labels
        
    Returns:
        sklearn.linear_model.LogisticRegression: Trained model
    """
    print(f"\n🔵 TRAINING LOGISTIC REGRESSION")
    print("=" * 50)
    
    lr_model = LogisticRegression(random_state=42, max_iter=1000)
    lr_model.fit(X_train, y_train)
    
    print("✅ Logistic Regression training completed")
    return lr_model

def train_decision_tree(X_train, y_train):
    """
    Train Decision Tree Classifier.
    
    Args:
        X_train: Training features
        y_train: Training labels
        
    Returns:
        sklearn.tree.DecisionTreeClassifier: Trained model
    """
    print(f"\n🌲 TRAINING DECISION TREE CLASSIFIER")
    print("=" * 50)
    
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    
    print("✅ Decision Tree training completed")
    return dt_model

def create_confusion_matrix_plots(y_test, lr_pred, dt_pred, label_encoder):
    """
    Create confusion matrix visualizations for both models.
    
    Args:
        y_test: True test labels
        lr_pred: Logistic Regression predictions
        dt_pred: Decision Tree predictions
        label_encoder: LabelEncoder for class names
    """
    print(f"\n📊 CREATING CONFUSION MATRICES")
    print("=" * 50)
    
    try:
        class_names = label_encoder.classes_
        
        # Create subplots
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Week 3: Baseline Models - Confusion Matrices', fontsize=16, fontweight='bold')
        
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
        plt.savefig('week3_confusion_matrices.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Confusion matrices saved as 'week3_confusion_matrices.png'")
        
    except Exception as e:
        print(f"⚠️ Visualization error: {e}")

def compare_model_performance(models_performance):
    """
    Compare and display performance of all models.
    
    Args:
        models_performance: Dictionary with model names and accuracies
    """
    print(f"\n🏆 BASELINE MODELS PERFORMANCE COMPARISON")
    print("=" * 60)
    
    # Sort models by accuracy
    sorted_models = sorted(models_performance.items(), key=lambda x: x[1], reverse=True)
    
    for rank, (model_name, accuracy) in enumerate(sorted_models, 1):
        stars = "⭐" * min(rank, 3)  # Show stars for ranking
        print(f"{rank}. {model_name:20}: {accuracy:.4f} ({accuracy*100:.2f}%) {stars}")
    
    # Best model
    best_model = sorted_models[0]
    print(f"\n🥇 Best Baseline Model: {best_model[0]}")
    print(f"   Accuracy: {best_model[1]:.4f} ({best_model[1]*100:.2f}%)")

def main():
    """Main function for Week 3 baseline model training."""
    print("🌍 WEEK 3: BASELINE MODEL TRAINING")
    print("=" * 60)
    print("Training Logistic Regression & Decision Tree Classifiers")
    
    # Get preprocessed data from Week 2
    try:
        X_scaled, y_encoded, scaler, label_encoder = week2_preprocessing()
        if X_scaled is None:
            print("❌ Failed to get preprocessed data from Week 2")
            return
    except Exception as e:
        print(f"❌ Error loading Week 2 data: {e}")
        return
    
    # Split dataset
    X_train, X_test, y_train, y_test = split_dataset(X_scaled, y_encoded)
    
    # Dictionary to store model performance
    models_performance = {}
    
    # Train Logistic Regression
    lr_model = train_logistic_regression(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_accuracy = evaluate_model_performance(y_test, lr_pred, "Logistic Regression", label_encoder)
    models_performance["Logistic Regression"] = lr_accuracy
    
    # Train Decision Tree
    dt_model = train_decision_tree(X_train, y_train)
    dt_pred = dt_model.predict(X_test)
    dt_accuracy = evaluate_model_performance(y_test, dt_pred, "Decision Tree", label_encoder)
    models_performance["Decision Tree"] = dt_accuracy
    
    # Create visualizations
    create_confusion_matrix_plots(y_test, lr_pred, dt_pred, label_encoder)
    
    # Compare model performance
    compare_model_performance(models_performance)
    
    print(f"\n✅ Week 3 baseline model training completed!")
    print(f"📊 Ready for Week 4: Advanced Model Training")
    
    # Return data and models for Week 4
    return {
        'data': (X_train, X_test, y_train, y_test),
        'models': {'Logistic Regression': lr_model, 'Decision Tree': dt_model},
        'performance': models_performance,
        'encoders': (scaler, label_encoder)
    }

if __name__ == "__main__":
    main()