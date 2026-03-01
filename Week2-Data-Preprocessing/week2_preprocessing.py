"""
Week 2: Data Preprocessing & Feature Engineering
ImpactSense - Earthquake Impact Prediction

This module handles data loading, preprocessing, and feature engineering
for the earthquake impact prediction project.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_earthquake_data(file_path='../data/earthquakes_2023_global.csv'):
    """
    Load earthquake dataset from CSV file.
    
    Args:
        file_path (str): Path to the earthquake dataset
        
    Returns:
        pandas.DataFrame: Loaded earthquake data
    """
    print("📂 Loading earthquake dataset...")
    try:
        data = pd.read_csv(file_path)
        print(f"✅ Dataset loaded successfully! Shape: {data.shape}")
        return data
    except FileNotFoundError:
        print("❌ Error: Dataset file not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

def inspect_dataset(data):
    """
    Perform comprehensive dataset inspection.
    
    Args:
        data (pandas.DataFrame): Raw earthquake data
    """
    print("\n🔍 DATASET INSPECTION")
    print("=" * 50)
    
    print("\n📊 First 5 rows:")
    print(data.head())
    
    print(f"\n📋 Dataset Info:")
    print(f"Shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    
    print("\n📈 Statistical Summary:")
    print(data.describe())
    
    return True

def preprocess_features(data):
    """
    Extract and preprocess important features for earthquake prediction.
    
    Args:
        data (pandas.DataFrame): Raw earthquake data
        
    Returns:
        pandas.DataFrame: Processed features dataframe
    """
    print("\n🎯 FEATURE SELECTION & PREPROCESSING")
    print("=" * 50)
    
    # Select important features
    important_features = ['latitude', 'longitude', 'depth', 'mag']
    print(f"Selected features: {important_features}")
    
    # Check if all required columns exist
    missing_cols = [col for col in important_features if col not in data.columns]
    if missing_cols:
        print(f"❌ Missing columns: {missing_cols}")
        return None
    
    # Extract features
    df = data[important_features].copy()
    
    # Handle missing values
    print(f"\n🔧 Handling Missing Values:")
    missing_before = df.isnull().sum()
    print("Missing values before cleaning:")
    print(missing_before[missing_before > 0] if missing_before.sum() > 0 else "No missing values found")
    
    # Fill missing values with median for numeric columns (if any)
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                print(f"  ✅ Filled {col} missing values with median: {median_val:.2f}")
    
    # Drop rows with remaining missing values
    df_clean = df.dropna()
    print(f"📊 Final dataset shape after cleaning: {df_clean.shape}")
    
    return df_clean

def create_risk_levels(data):
    """
    Create risk level target variable based on earthquake magnitude.
    
    Args:
        data (pandas.DataFrame): Cleaned earthquake data
        
    Returns:
        pandas.DataFrame: Data with risk levels added
    """
    print(f"\n🎯 CREATING RISK LEVEL TARGET")
    print("=" * 50)
    
    def classify_risk(magnitude):
        """Classify earthquake risk based on magnitude."""
        if magnitude < 4:
            return 'Low'
        elif magnitude < 6:
            return 'Medium'
        else:
            return 'High'
    
    # Create risk level column
    data_with_risk = data.copy()
    data_with_risk['risk_level'] = data_with_risk['mag'].apply(classify_risk)
    
    # Display risk level distribution
    risk_distribution = data_with_risk['risk_level'].value_counts()
    print("Risk Level Distribution:")
    for level, count in risk_distribution.items():
        percentage = (count / len(data_with_risk)) * 100
        print(f"  {level}: {count} samples ({percentage:.1f}%)")
    
    return data_with_risk

def encode_and_scale_features(data):
    """
    Encode categorical variables and scale numerical features.
    
    Args:
        data (pandas.DataFrame): Data with risk levels
        
    Returns:
        tuple: (X_scaled, y_encoded, scaler, label_encoder)
    """
    print(f"\n⚖️ FEATURE ENCODING & SCALING")
    print("=" * 50)
    
    # Encode risk_level using LabelEncoder
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(data['risk_level'])
    
    print("🔤 Label Encoding Mapping:")
    for i, label in enumerate(label_encoder.classes_):
        print(f"  {label} → {i}")
    
    # Prepare features for scaling
    feature_columns = ['latitude', 'longitude', 'depth', 'mag']
    X = data[feature_columns]
    
    # Scale features using StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=feature_columns, index=X.index)
    
    print("✅ Features scaled using StandardScaler")
    print("\nScaled feature statistics:")
    print(X_scaled_df.describe().round(3))
    
    return X_scaled_df, y_encoded, scaler, label_encoder

def create_data_visualizations(data_with_risk):
    """
    Create visualizations for earthquake data analysis.
    
    Args:
        data_with_risk (pandas.DataFrame): Data with risk levels
    """
    print(f"\n📊 CREATING DATA VISUALIZATIONS")
    print("=" * 50)
    
    try:
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Week 2: Earthquake Data Analysis & Preprocessing', fontsize=16, fontweight='bold')
        
        # 1. Magnitude Distribution
        data_with_risk['mag'].hist(bins=30, ax=axes[0,0], color='skyblue', alpha=0.7, edgecolor='black')
        axes[0,0].set_title('Magnitude Distribution')
        axes[0,0].set_xlabel('Magnitude')
        axes[0,0].set_ylabel('Frequency')
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. Risk Level Distribution
        risk_counts = data_with_risk['risk_level'].value_counts()
        colors = ['#FF6B6B', '#FFD93D', '#6BCF7F']
        axes[0,1].pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', 
                     colors=colors, startangle=90)
        axes[0,1].set_title('Risk Level Distribution')
        
        # 3. Depth vs Magnitude
        scatter = axes[1,0].scatter(data_with_risk['depth'], data_with_risk['mag'], 
                                  alpha=0.6, c=data_with_risk['mag'], cmap='viridis', s=20)
        axes[1,0].set_title('Depth vs Magnitude')
        axes[1,0].set_xlabel('Depth (km)')
        axes[1,0].set_ylabel('Magnitude')
        axes[1,0].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[1,0], label='Magnitude')
        
        # 4. Geographic Distribution
        scatter2 = axes[1,1].scatter(data_with_risk['longitude'], data_with_risk['latitude'], 
                                    c=data_with_risk['mag'], cmap='Reds', alpha=0.6, s=20)
        axes[1,1].set_title('Geographic Distribution of Earthquakes')
        axes[1,1].set_xlabel('Longitude')
        axes[1,1].set_ylabel('Latitude')
        axes[1,1].grid(True, alpha=0.3)
        plt.colorbar(scatter2, ax=axes[1,1], label='Magnitude')
        
        plt.tight_layout()
        plt.savefig('week2_data_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualizations saved as 'week2_data_analysis.png'")
        
    except Exception as e:
        print(f"⚠️ Visualization error: {e}")

def main():
    """Main function for Week 2 tasks."""
    print("🌍 WEEK 2: DATA PREPROCESSING & FEATURE ENGINEERING")
    print("=" * 60)
    
    # Step 1: Load dataset
    data = load_earthquake_data()
    if data is None:
        return
    
    # Step 2: Inspect dataset
    inspect_dataset(data)
    
    # Step 3: Preprocess features
    df_clean = preprocess_features(data)
    if df_clean is None:
        return
    
    # Step 4: Create risk levels
    data_with_risk = create_risk_levels(df_clean)
    
    # Step 5: Encode and scale features
    X_scaled, y_encoded, scaler, label_encoder = encode_and_scale_features(data_with_risk)
    
    # Step 6: Create visualizations
    create_data_visualizations(data_with_risk)
    
    print(f"\n✅ Week 2 preprocessing completed successfully!")
    print(f"📊 Ready for Week 3: Baseline Model Training")
    
    # Return processed data for next weeks
    return X_scaled, y_encoded, scaler, label_encoder

if __name__ == "__main__":
    main()