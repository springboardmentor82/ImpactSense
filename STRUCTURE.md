# ImpactSense - Earthquake Impact Prediction System

## Project Overview

A comprehensive machine learning solution for real-time earthquake impact prediction with a professional Streamlit web interface.

**Mentor Repository:** https://github.com/springboardmentor82/ImpactSense

---

## 📁 Project Structure

```
ImpactSense/
├── Week_1/           # Data Exploration & Loading
├── Week_2/           # Preprocessing & Feature Engineering
├── Week_3/           # Baseline Models
├── Week_4/           # Advanced Models & Hyperparameter Tuning
├── Week_5/           # Model Evaluation & Explainability
├── Week_6/           # UI Prototype Development
├── Week_7/           # Final Implementation, Testing & Deployment
│   ├── earthquake_ui.py        # Streamlit Web Application
│   ├── ImpactSense.ipynb       # Complete ML Pipeline (All Weeks)
│   └── requirements.txt        # Python Dependencies
└── README.md         # Project Overview
```

---

## 🎯 Week Details

### Week 1: Data Exploration & Loading
- Load earthquake dataset (1,300 records)
- Explore data structure and features
- Identify missing values and data quality issues

### Week 2: Preprocessing & Feature Engineering
- Clean data (remove 44 duplicates)
- Handle missing values
- Create 3 engineered features:
  - Is Shallow (depth < 70km)
  - Intensity Score (average of CDI & MMI)
  - Risk Score (Magnitude × Intensity Score)
- Scale features with StandardScaler
- Split data 80/20 for training/testing

### Week 3: Baseline Models
- Logistic Regression: 59.13% accuracy
- Decision Tree: 78.57% accuracy
- Evaluate and compare baseline models

### Week 4: Advanced Models & Tuning
- Random Forest: 86.11% → 88.89% (tuned)
- Gradient Boosting: 90.08% accuracy ✅ **BEST**
- Apply GridSearchCV for hyperparameter optimization
- Cross-validation (5-fold)

### Week 5: Model Evaluation & Explainability
- Confusion matrices and detailed metrics
- Feature importance analysis
- Error analysis and visualization
- Model decision surfaces

### Week 6: UI Prototype Development
- Streamlit web application
- Interactive prediction interface
- Scenario-based testing
- Real-time risk assessment

### Week 7: Final Implementation, Testing & Deployment
- Edge case testing (8/8 tests passed)
- Model validation and stability checks
- Comprehensive testing suite
- Production-ready deployment

---

## 🚀 How to Run

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Setup & Run

```bash
# 1. Navigate to Week_7
cd Week_7

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run earthquake_ui.py

# 4. Open browser at http://localhost:8501
```

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Best Model** | Gradient Boosting |
| **Test Accuracy** | 90.08% |
| **Cross-Validation** | 87.05% ± 2.05% |
| **Red Alert Recall** | 96.67% (Critical!) |
| **Training Samples** | 1,256 |
| **Features** | 8 (5 raw + 3 engineered) |
| **Alert Classes** | 4 levels (Green, Yellow, Orange, Red) |

---

## 🎨 Streamlit UI Features

### 4-Page Interface

1. **🔮 Prediction Page** - Real-time earthquake risk analysis
2. **📊 Analysis Page** - Feature importance and model metrics
3. **📈 Scenarios Page** - Pre-configured earthquake scenarios
4. **ℹ️ About Page** - Model documentation and help

---

## 📦 Dependencies

- scikit-learn (1.6.1) - Machine Learning
- pandas (2.2.3) - Data Processing
- numpy (2.2.3) - Numerical Computing
- matplotlib (3.9.0) - Visualization
- seaborn (0.13.2) - Statistical Visualization
- streamlit (1.40.0) - Web Interface

---

## 🎯 Alert Levels

| Level | Color | Risk | Action |
|-------|-------|------|--------|
| 🟢 Green | #00b050 | Low | Monitor |
| 🟡 Yellow | #ffc000 | Moderate | Prepare |
| 🟠 Orange | #ff7f00 | High | Alert |
| 🔴 Red | #c41e3a | Critical | Evacuate |

---

## ✅ Testing & Validation

- ✓ 8/8 Edge case tests passed
- ✓ 3/3 Model validation tests passed
- ✓ 100% prediction consistency
- ✓ Cross-validation robust (87.05%)
- ✓ Red alert detection reliable (96.67% recall)

---

## 📈 Key Features

- **Real-time Predictions** - Instant earthquake risk assessment
- **Feature Engineering** - 3 derived features for better predictions
- **Model Optimization** - GridSearchCV hyperparameter tuning
- **Explainability** - Feature importance analysis
- **Validation** - Cross-validation and edge case testing
- **UI/UX** - Professional Streamlit interface
- **Production Ready** - Clean, tested, deployable code

---

## 👨‍💼 Mentor

**Springboard Mentor:** springboardmentor82  
**Mentor Repository:** https://github.com/springboardmentor82/ImpactSense

---

## 📄 File Descriptions

### earthquake_ui.py
Main Streamlit web application featuring:
- Interactive parameter input with sliders
- Real-time risk prediction
- Probability distribution visualization
- Scenario-based testing
- Model analytics and documentation

### ImpactSense.ipynb
Complete Jupyter notebook containing:
- All 93 cells across Weeks 1-7
- Data loading and exploration
- Preprocessing pipeline
- Model training and evaluation
- Feature engineering
- Visualization and analysis

### requirements.txt
Python package dependencies for running the project

---

## 🔄 Development Workflow

Each week builds upon the previous one:

```
Week 1-2: Data     → Week 3: Baseline Models
    ↓
Week 4: Advanced Models → Week 5: Evaluation
    ↓
Week 6-7: UI & Deployment
```

---

## 🌐 Deployment

The Streamlit app is production-ready and can be deployed to:
- Streamlit Cloud (free)
- AWS/Azure/GCP
- Docker containers
- Local servers

---

## 📝 Last Updated

**Date:** March 30, 2026  
**Status:** ✅ Complete & Ready for Review

---

**Ready for Pull Request Submission!** 🚀
