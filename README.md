# 🌍 Earthquake Predictor (Seismic Analytics Terminal)

🚀 **Live Demo:** [Launch Earthquake Predictor](https://impactsense-ehybijupu4cu9apppr6weqk.streamlit.app/)

## 📌 Project Overview
**Earthquake Predictor** is an enterprise-grade machine learning dashboard designed to assess the risk of catastrophic seismic events. By analyzing geospatial telemetry and historical fault line data, the system calculates an AI-driven threat confidence score, allowing operators to visualize earthquake danger in real-time.

This project was built to demonstrate the integration of machine learning models with interactive data visualization and custom frontend routing.

## 💻 Tech Stack
* **Language:** Python 3.x
* **Frontend Framework:** Streamlit (with custom Glassmorphism CSS)
* **Machine Learning:** Scikit-Learn (Random Forest Classifier)
* **Data Visualization:** Plotly Graph Objects (3D rendering & Radar charts)
* **Geospatial Intelligence:** Geopy (Nominatim API)
* **Data Handling:** Pandas & NumPy

## ✨ Core Features
* 🧠 **AI Predictive Engine:** Utilizes a heavily tuned Random Forest model (100 estimators) to evaluate Subterranean Depth and Regional Hazard Coefficients, outputting a live safety probability.
* 🛰️ **3D Interactive Globe:** A fully interactive, spinning 3D orthographic projection that visually locks onto the target coordinates.
* 📍 **Live Reverse Geocoding:** Automatically translates raw Latitude and Longitude inputs into readable, English-translated city and country names.
*📊 **Seismic Threat Matrix:** Strips away confusing scientific jargon and visualizes the exact danger breakdown (Fault Line Proximity, Surface Shake, Area     History, and Quake Depth) using an intuitive, color-coded dashboard.
* 🎨 **Locked Dark Theme UI:** Features a custom-coded, responsive Glassmorphism design configured to permanently display in high-contrast dark mode for optimal readability in emergency command center environments.

## ⚙️ How It Works
1. **Input Telemetry:** The operator inputs target coordinates (Lat/Lon) alongside the normalized depth (Z-Score) and historical regional risk.
2. **Reverse Geocoding:** The system pings the Nominatim API to identify the real-world location (e.g., "Tokyo, Japan").
3. **AI Processing:** The data is pushed through the Random Forest model to calculate a threat probability score.
4. **Visual Render:** The UI dynamically renders the diagnostic output, sounds an audio alarm if the threat is critical, plots the Seismic Threat Matrix, and spins the 3D globe to the exact target location.
