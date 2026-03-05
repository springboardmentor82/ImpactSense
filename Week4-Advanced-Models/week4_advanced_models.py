"""
Week 4: Advanced Model Training
ImpactSense - Earthquake Impact Prediction

This module trains advanced ML models (Random Forest & Gradient Boosting)
with cross-validation and comprehensive evaluation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix
import sys
import os

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Week3-Baseline-Models.week3_baseline_models import main as week3_baseline

def perform_cross_validation(model, X_train, y_train, cv_folds=5):
    """
    Perform cross-validation for a model.
    
    Args:
        model: ML model to evaluate
        X_train: Training features
        y_train: Training labels
        cv_folds: Number of CV folds
        
    Returns:
        numpy.ndarray: Cross-validation scores
    """
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv_folds)
    print(f"  Cross-validation scores: {cv_scores}")
    print(f"  Mean CV accuracy: {cv_scores.mean():.4f} (±{cv_scores.std()*2:.4f})")
    
    return cv_scores

def train_random_forest(X_train, y_train, X_test, y_test, label_encoder):
    """
    Train Random Forest Classifier with cross-validation.
    
    Args:
        X_train, X_test: Training and testing features
        y_train, y_test: Training and testing labels
        label_encoder: LabelEncoder for class names
        
    Returns:
        tuple: (model, predictions, accuracy, cv_scores)
    """
    print(f"\n🌳 TRAINING RANDOM FOREST CLASSIFIER")
    print("=" * 60)
    
    # Create and train model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Make predictions
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)
    
    print(f"✅ Random Forest training completed")
    print(f"📊 Test Accuracy: {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
    
    # Perform cross-validation
    print(f"\n🔄 Performing 5-Fold Cross-Validation:")
    rf_cv_scores = perform_cross_validation(rf_model, X_train, y_train)
    
    return rf_model, rf_pred, rf_accuracy, rf_cv_scores

def train_gradient_boosting(X_train, y_train, X_test, y_test, label_encoder):
    """
    Train Gradient Boosting Classifier with cross-validation.
    
    Args:
        X_train, X_test: Training and testing features
        y_train, y_test: Training and testing labels
        label_encoder: LabelEncoder for class names
        
    Returns:
        tuple: (model, predictions, accuracy, cv_scores)
    """
    print(f"\n🚀 TRAINING GRADIENT BOOSTING CLASSIFIER")
    print("=" * 60)
    
    # Create and train model
    gb_model = GradientBoostingClassifier(random_state=42)
    gb_model.fit(X_train, y_train)
    
    # Make predictions
    gb_pred = gb_model.predict(X_test)
    gb_accuracy = accuracy_score(y_test, gb_pred)
    
    print(f"✅ Gradient Boosting training completed")
    print(f"📊 Test Accuracy: {gb_accuracy:.4f} ({gb_accuracy*100:.2f}%)")
    
    # Perform cross-validation
    print(f"\n🔄 Performing 5-Fold Cross-Validation:")
    gb_cv_scores = perform_cross_validation(gb_model, X_train, y_train)
    
    return gb_model, gb_pred, gb_accuracy, gb_cv_scores

def analyze_feature_importance(rf_model, feature_names):
    """
    Analyze and display feature importance from Random Forest.
    
    Args:
        rf_model: Trained Random Forest model
        feature_names: List of feature names
    """
    print(f"\n📊 FEATURE IMPORTANCE ANALYSIS")
    print("=" * 50)
    
    importances = rf_model.feature_importances_
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    print("Feature Importance Rankings:")
    for idx, row in importance_df.iterrows():
        print(f"  {row['Feature']:12}: {row['Importance']:.4f}")
    
    return importance_df

def create_advanced_visualizations(models_data, cv_scores_data, baseline_performance):
    """
    Create comprehensive visualizations for advanced models.
    
    Args:
        models_data: Dictionary containing model data
        cv_scores_data: Dictionary containing CV scores
        baseline_performance: Baseline model performance data
    """
    print(f"\n📊 CREATING ADVANCED VISUALIZATIONS")
    print("=" * 50)
    
    try:
        # Extract data
        X_test = models_data['X_test']
        y_test = models_data['y_test']
        rf_model = models_data['rf_model']
        gb_model = models_data['gb_model']
        rf_pred = models_data['rf_pred']
        gb_pred = models_data['gb_pred']
        label_encoder = models_data['label_encoder']
        
        # Create comprehensive visualization
        fig = plt.figure(figsize=(18, 12))
        fig.suptitle('Week 4: Advanced Models - Comprehensive Analysis', fontsize=16, fontweight='bold')
        
        # 1. Model Accuracy Comparison (All models)
        ax1 = plt.subplot(2, 3, 1)
        all_models = ['Logistic Regression', 'Decision Tree', 'Random Forest', 'Gradient Boosting']
        all_accuracies = [
            baseline_performance.get('Logistic Regression', 0),
            baseline_performance.get('Decision Tree', 0),
            models_data['rf_accuracy'],
            models_data['gb_accuracy']
        ]
        
        colors = ['#FFB6C1', '#98FB98', '#87CEEB', '#DDA0DD']
        bars = plt.bar(all_models, all_accuracies, color=colors, alpha=0.8)
        plt.title('All Models Accuracy Comparison')
        plt.xlabel('Models')
        plt.ylabel('Test Accuracy')
        plt.xticks(rotation=45)
        plt.ylim(0, 1)
        
        # Add value labels on bars
        for bar, acc in zip(bars, all_accuracies):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Cross-Validation Scores Comparison
        ax2 = plt.subplot(2, 3, 2)
        cv_models = list(cv_scores_data.keys())
        cv_means = [scores.mean() for scores in cv_scores_data.values()]
        cv_stds = [scores.std() for scores in cv_scores_data.values()]
        
        x_pos = np.arange(len(cv_models))
        bars = plt.bar(x_pos, cv_means, yerr=cv_stds, capsize=5, 
                       color=['#FF9999', '#66B2FF'], alpha=0.8)
        plt.title('5-Fold Cross-Validation\nAccuracy Comparison')
        plt.xlabel('Models')
        plt.ylabel('CV Accuracy')
        plt.xticks(x_pos, cv_models, rotation=15)
        plt.ylim(0, 1)
        
        # Add value labels
        for i, (bar, mean, std) in enumerate(zip(bars, cv_means, cv_stds)):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + std + 0.02,
                    f'{mean:.3f}±{std:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 3. Feature Importance (Random Forest)
        ax3 = plt.subplot(2, 3, 3)
        feature_names = ['Latitude', 'Longitude', 'Depth', 'Magnitude']
        importances = rf_model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        bars = plt.bar(range(len(importances)), importances[indices], color=colors)
        plt.title('Random Forest\nFeature Importance')
        plt.xlabel('Features')
        plt.ylabel('Importance Score')
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
        
        # Add value labels
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Random Forest Confusion Matrix
        ax4 = plt.subplot(2, 3, 4)
        class_names = label_encoder.classes_
        cm_rf = confusion_matrix(y_test, rf_pred)
        sns.heatmap(cm_rf, annot=True, fmt='d', cmap='viridis',
                    xticklabels=class_names, yticklabels=class_names, ax=ax4)
        plt.title('Random Forest\nConfusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # 5. Gradient Boosting Confusion Matrix
        ax5 = plt.subplot(2, 3, 5)
        cm_gb = confusion_matrix(y_test, gb_pred)
        sns.heatmap(cm_gb, annot=True, fmt='d', cmap='plasma',
                    xticklabels=class_names, yticklabels=class_names, ax=ax5)
        plt.title('Gradient Boosting\nConfusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # 6. Risk Level Distribution
        ax6 = plt.subplot(2, 3, 6)
        y_test_decoded = label_encoder.inverse_transform(y_test)
        risk_counts = pd.Series(y_test_decoded).value_counts()
        
        colors = ['#FF6B6B', '#FFD93D', '#6BCF7F']
        wedges, texts, autotexts = plt.pie(risk_counts.values, labels=risk_counts.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Test Set Risk Level\nDistribution')
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        plt.savefig('week4_advanced_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Advanced visualizations saved as 'week4_advanced_analysis.png'")
        
    except Exception as e:
        print(f"⚠️ Visualization error: {e}")

def compare_all_models(baseline_performance, advanced_performance, cv_scores_data):
    """
    Compare performance of all models (baseline + advanced).
    
    Args:
        baseline_performance: Dictionary with baseline model performance
        advanced_performance: Dictionary with advanced model performance
        cv_scores_data: Dictionary with CV scores
    """
    print(f"\n🏆 FINAL MODEL PERFORMANCE RANKING")
    print("=" * 70)
    
    # Combine all results
    all_results = {**baseline_performance, **advanced_performance}
    sorted_results = sorted(all_results.items(), key=lambda x: x[1], reverse=True)
    
    print("📊 Test Accuracy Rankings:")
    for rank, (model_name, accuracy) in enumerate(sorted_results, 1):
        stars = "⭐" * min(rank, 3)  # Show stars for top 3
        print(f"  {rank}. {model_name:20}: {accuracy:.4f} ({accuracy*100:.2f}%) {stars}")
    
    print(f"\n🥇 Best Overall Model: {sorted_results[0][0]}")
    print(f"   Test Accuracy: {sorted_results[0][1]:.4f} ({sorted_results[0][1]*100:.2f}%)")
    
    # Cross-validation summary
    if cv_scores_data:
        print(f"\n📈 Cross-Validation Summary:")
        for model_name, scores in cv_scores_data.items():
            print(f"  {model_name:15}: {scores.mean():.4f} (±{scores.std()*2:.4f})")

def main():
    """Main function for Week 4 advanced model training."""
    print("🌍 WEEK 4: ADVANCED MODEL TRAINING")
    print("=" * 60)
    print("Training Random Forest & Gradient Boosting with Cross-Validation")
    
    # Get data from Week 3
    try:
        week3_results = week3_baseline()
        if not week3_results:
            print("❌ Failed to get results from Week 3")
            return
        
        # Extract data
        X_train, X_test, y_train, y_test = week3_results['data']
        baseline_performance = week3_results['performance']
        scaler, label_encoder = week3_results['encoders']
        
    except Exception as e:
        print(f"❌ Error loading Week 3 data: {e}")
        return
    
    # Train Random Forest
    rf_model, rf_pred, rf_accuracy, rf_cv_scores = train_random_forest(
        X_train, y_train, X_test, y_test, label_encoder
    )
    
    # Train Gradient Boosting
    gb_model, gb_pred, gb_accuracy, gb_cv_scores = train_gradient_boosting(
        X_train, y_train, X_test, y_test, label_encoder
    )
    
    # Analyze feature importance
    feature_names = ['latitude', 'longitude', 'depth', 'magnitude']
    importance_df = analyze_feature_importance(rf_model, feature_names)
    
    # Prepare data for visualizations
    models_data = {
        'X_test': X_test,
        'y_test': y_test,
        'rf_model': rf_model,
        'gb_model': gb_model,
        'rf_pred': rf_pred,
        'gb_pred': gb_pred,
        'rf_accuracy': rf_accuracy,
        'gb_accuracy': gb_accuracy,
        'label_encoder': label_encoder
    }
    
    cv_scores_data = {
        'Random Forest': rf_cv_scores,
        'Gradient Boosting': gb_cv_scores
    }
    
    # Create visualizations
    create_advanced_visualizations(models_data, cv_scores_data, baseline_performance)
    
    # Advanced model performance
    advanced_performance = {
        'Random Forest': rf_accuracy,
        'Gradient Boosting': gb_accuracy
    }
    
    # Final comparison
    compare_all_models(baseline_performance, advanced_performance, cv_scores_data)
    
    print(f"\n✅ Week 4 advanced model training completed!")
    print(f"🎉 ImpactSense Project Successfully Completed!")
    
    return {
        'advanced_models': {'Random Forest': rf_model, 'Gradient Boosting': gb_model},
        'performance': advanced_performance,
        'cv_scores': cv_scores_data,
        'feature_importance': importance_df
    }

if __name__ == "__main__":
    main()