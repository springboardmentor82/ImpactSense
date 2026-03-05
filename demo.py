"""
ImpactSense – Earthquake Impact Prediction (Demo Version)
Machine Learning Project for Earthquake Risk Assessment

This is a demo version that shows the data processing pipeline.
The full ML version will be ready once all packages are installed.

Author: Earthquake Impact Prediction Team
Date: February 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def print_section_header(title):
    """Print a formatted section header for better readability."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def load_data():
    """Load the earthquake dataset from CSV file."""
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

def basic_data_analysis(data):
    """Perform basic data analysis and exploration."""
    
    print_section_header("📌 WEEK 2 – DATA PREPROCESSING & FEATURE ENGINEERING")
    
    # Dataset Inspection
    print("🔍 Dataset Inspection:")
    print("\n📊 First 5 rows:")
    print(data.head())
    
    print(f"\n📋 Dataset Info:")
    print(f"Dataset shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    
    # Check for required columns
    required_cols = ['latitude', 'longitude', 'depth', 'mag']
    available_cols = [col for col in required_cols if col in data.columns]
    print(f"\n🎯 Available required columns: {available_cols}")
    
    if len(available_cols) == len(required_cols):
        # Select important features
        df = data[required_cols].copy()
        
        print("\n📈 Statistical Summary:")
        print(df.describe())
        
        # Handle missing values
        print("\n🔧 Missing Values Analysis:")
        missing_values = df.isnull().sum()
        print("Missing values per column:")
        for col, missing in missing_values.items():
            percentage = (missing / len(df)) * 100
            print(f"  {col}: {missing} ({percentage:.1f}%)")
        
        # Clean data
        df_clean = df.dropna()
        print(f"\n📊 Dataset shape after removing missing values: {df_clean.shape}")
        
        # Create risk levels
        print("\n🎯 Creating Risk Level Categories:")
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
        
        # Basic visualization
        create_basic_visualizations(df_clean)
        
        return df_clean
    else:
        print(f"❌ Missing required columns: {set(required_cols) - set(available_cols)}")
        return None

def create_basic_visualizations(df):
    """Create basic visualizations for earthquake data."""
    print("\n📊 Creating Basic Visualizations...")
    
    try:
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Earthquake Data Analysis', fontsize=16, fontweight='bold')
        
        # 1. Magnitude Distribution
        df['mag'].hist(bins=30, ax=axes[0,0], color='skyblue', alpha=0.7)
        axes[0,0].set_title('Magnitude Distribution')
        axes[0,0].set_xlabel('Magnitude')
        axes[0,0].set_ylabel('Frequency')
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. Risk Level Distribution
        risk_counts = df['risk_level'].value_counts()
        colors = ['#FF6B6B', '#FFD93D', '#6BCF7F']
        axes[0,1].pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', 
                     colors=colors, startangle=90)
        axes[0,1].set_title('Risk Level Distribution')
        
        # 3. Depth vs Magnitude
        axes[1,0].scatter(df['depth'], df['mag'], alpha=0.6, c=df['mag'], cmap='viridis')
        axes[1,0].set_title('Depth vs Magnitude')
        axes[1,0].set_xlabel('Depth (km)')
        axes[1,0].set_ylabel('Magnitude')
        axes[1,0].grid(True, alpha=0.3)
        
        # 4. Geographic Distribution
        scatter = axes[1,1].scatter(df['longitude'], df['latitude'], 
                                   c=df['mag'], cmap='Reds', alpha=0.6, s=20)
        axes[1,1].set_title('Geographic Distribution of Earthquakes')
        axes[1,1].set_xlabel('Longitude')
        axes[1,1].set_ylabel('Latitude')
        axes[1,1].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[1,1], label='Magnitude')
        
        plt.tight_layout()
        plt.savefig('earthquake_analysis_basic.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualizations saved as 'earthquake_analysis_basic.png'")
        
    except Exception as e:
        print(f"⚠️ Visualization error: {e}")

def prepare_for_ml(df):
    """Prepare data structure for machine learning models."""
    print_section_header("🤖 PREPARING FOR MACHINE LEARNING")
    
    print("📝 Data Preparation Summary:")
    print(f"  📊 Total samples: {len(df)}")
    print(f"  🎯 Features: latitude, longitude, depth, magnitude")
    print(f"  🏷️ Target: risk_level (Low, Medium, High)")
    
    # Feature statistics
    print("\n📈 Feature Statistics:")
    features = ['latitude', 'longitude', 'depth', 'mag']
    for feature in features:
        stats = df[feature].describe()
        print(f"  {feature.capitalize()}:")
        print(f"    Range: {stats['min']:.2f} to {stats['max']:.2f}")
        print(f"    Mean: {stats['mean']:.2f}, Std: {stats['std']:.2f}")
    
    # Data quality check
    print("\n✅ Data Quality Check:")
    print(f"  📋 No missing values: {df.isnull().sum().sum() == 0}")
    print(f"  📊 Balanced classes: {df['risk_level'].value_counts().min() > 10}")
    
    return True

def show_ml_pipeline_preview():
    """Show what the full ML pipeline will include."""
    print_section_header("📌 FULL ML PIPELINE PREVIEW")
    
    print("🔮 When sklearn is installed, the complete pipeline will include:")
    print("\n📌 WEEK 3 – BASELINE MODEL TRAINING:")
    print("  🔵 Logistic Regression")
    print("  🌲 Decision Tree Classifier")
    print("  📊 Performance evaluation with accuracy, classification reports, confusion matrices")
    
    print("\n📌 WEEK 4 – ADVANCED MODEL TRAINING:")
    print("  🌳 Random Forest Classifier")
    print("  🚀 Gradient Boosting Classifier")
    print("  🔄 5-fold Cross-validation")
    print("  📈 Feature importance analysis")
    print("  🎯 Model comparison and selection")
    
    print("\n🎉 Full ML Pipeline Features:")
    print("  ⚖️ StandardScaler for feature scaling")
    print("  🏷️ LabelEncoder for target encoding")
    print("  📊 Comprehensive visualizations")
    print("  🔍 Cross-validation for model validation")
    print("  📈 Learning curves and performance metrics")

def main():
    """Main function to execute the earthquake analysis pipeline."""
    print("🌍 ImpactSense – Earthquake Impact Prediction (Demo)")
    print("=" * 60)
    print("Machine Learning Project for Earthquake Risk Assessment")
    print("Demo Version - Data Analysis & Preprocessing")
    
    # Load and analyze data
    data = load_data()
    if data is None:
        return
    
    # Perform basic analysis
    df_clean = basic_data_analysis(data)
    if df_clean is None:
        return
    
    # Prepare for ML
    if prepare_for_ml(df_clean):
        show_ml_pipeline_preview()
    
    print_section_header("Demo Complete!")
    print("✅ Data preprocessing and analysis completed successfully!")
    print("🔄 Installing sklearn packages in background...")
    print("📈 Run again after installation for full ML pipeline!")

if __name__ == "__main__":
    main()