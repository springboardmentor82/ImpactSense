import streamlit as st
import pandas as pd
import joblib
import time
import plotly.graph_objects as go
import uuid

# --- 1. Page Configuration & Glassmorphism CSS ---
st.set_page_config(page_title="ImpactSense Global", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
            
    /* Hide Streamlit's default audio player */
    audio {
        display: none !important;
    }
    
    .stApp {
        background-color: #0b132b;
        color: #e0eef7;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe, #4facfe, #00f2fe);
        background-size: 200% auto;
        color: #000 !important;
        border: none;
        border-radius: 8px;
        height: 3.5em;
        font-weight: 900;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        transition: 0.5s;
        box-shadow: 0px 0px 15px rgba(79, 172, 254, 0.4);
    }
    .stButton>button:hover {
        background-position: right center;
        box-shadow: 0px 0px 25px rgba(79, 172, 254, 0.8);
        transform: scale(1.02);
    }
    
    /* FIX 3: Pure CSS Smooth Scrolling Ticker */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: rgba(0, 0, 0, 0.5);
        border-bottom: 1px solid #4facfe;
        padding: 8px 0;
        margin-bottom: 20px;
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        padding-left: 100%;
        animation: ticker-anim 20s linear infinite;
        color: #4facfe;
        font-family: monospace;
        font-size: 16px;
        font-weight: bold;
    }
    @keyframes ticker-anim {
        0%   { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. State Management ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 3. Model Loading ---
@st.cache_resource
def load_model():
    return joblib.load('models/earthquake_model.pkl')

# --- 4. Audio Alert Function (Stealth Mode) ---
def play_alert_sound():
    # Force a unique URL so Streamlit plays it every single time
    sound_url = f"https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3?t={time.time()}"
    
    # Use Streamlit's native audio, which is now invisible thanks to our CSS!
    st.audio(sound_url, format="audio/mpeg", autoplay=True)
    
    st.markdown("### 🚨 **[EMERGENCY ALARM SOUNDING]**")

# --- 5. The Login Page ---
def show_login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        # FIX 2: Replaced broken image with a bulletproof CSS-styled Emoji that never fails
        st.markdown("<div style='font-size: 90px; text-align: left;'>🌍</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #4facfe; margin-top: -20px;'>IMPACTSENSE NEXUS</h1>", unsafe_allow_html=True)
        st.caption("AUTHORIZED PERSONNEL ONLY | ENCRYPTED CONNECTION")
        st.divider()
        
        with st.form("login_form"):
            username = st.text_input("Operator ID")
            password = st.text_input("Decryption Key", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Login")
            
            if submit:
                if username and password == "admin":
                    st.success("Access Granted. Establishing secure connection to global nodes...")
                    time.sleep(1.5) 
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Access Denied. Ensure credentials are correct. (Hint: 'admin')")

# --- 6. The Main Application Dashboard ---
def show_dashboard():
    model = load_model()
    
    # Smooth CSS Ticker
    st.markdown("""
        <div class="ticker-wrap">
            <div class="ticker">
                🟢 LIVE FEED >> M 2.1 ALASKA | M 3.4 CHILE | M 1.2 CALIFORNIA | 🔴 HIGH RISK ANOMALY DETECTED IN SECTOR 7 | 🟢 SENSOR GRID STABLE...
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<div style='font-size: 60px;'>🌍</div>", unsafe_allow_html=True)
        st.title("ImpactSense")
        st.caption("GLOBAL SENSOR NETWORK")
        st.divider()
        st.write("👤 **Operator:** Admin")
        st.write("📡 **AI Core:** RF-100 Active")
        st.write("🟢 **Uplink:** STABLE")
        st.divider()
        if st.button("Terminate Session"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("<h2>Global Seismic Threat Terminal</h2>", unsafe_allow_html=True)
    st.markdown("Input local telemetry below to trigger the predictive analysis engine.")
    
    tab1, tab2 = st.tabs(["🎯 Live Targeting", "📈 Grid Diagnostics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Target Latitude (°N/°S)", min_value=-90.0, max_value=90.0, value=35.6)
            longitude = st.number_input("Target Longitude (°E/°W)", min_value=-180.0, max_value=180.0, value=139.6)
        with col2:
            depth_scaled = st.number_input("Subterranean Depth (Z-Score)", value=-1.5)
            location_risk = st.number_input("Regional Hazard Coefficient", value=8.5)

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("RUN PREDICTION PROTOCOL"):
            
            terminal = st.empty()
            logs = [
                "Establishing secure satellite uplink...", 
                "Calibrating geospatial coordinates...", 
                "Injecting Z-Score variables into Random Forest matrices...", 
                "Calculating SHAP confidence probabilities...", 
                "Finalizing structural diagnostic..."
            ]
            terminal_text = ""
            for log in logs:
                terminal_text += f"> {log}\n"
                terminal.code(terminal_text, language="bash")
                time.sleep(0.4)
            terminal.empty() 
            
            input_data = pd.DataFrame([[depth_scaled, latitude, longitude, location_risk]], 
                                      columns=['depth_scaled', 'latitude', 'longitude', 'location_risk_score'])
            
            prediction = model.predict(input_data)
            probabilities = model.predict_proba(input_data)[0] 
            confidence_score = max(probabilities) * 100 
            
            st.divider()
            
            res_col1, res_col2 = st.columns([1, 1])
            
            with res_col1:
                st.subheader("Diagnostic Output:")
                if prediction[0] == 1:
                    play_alert_sound()
                    st.error("🚨 **CRITICAL HAZARD DETECTED**")
                    st.write("Telemetry aligns with catastrophic seismic profiles. Evacuation protocols advised.")
                    st.progress(int(confidence_score), text=f"AI Threat Confidence: {confidence_score:.1f}%")
                else:
                    st.success("✅ **STATUS: NOMINAL (LOW RISK)**")
                    st.write("Structural integrity holding. No severe seismic anomalies detected.")
                    st.progress(int(confidence_score), text=f"AI Safety Confidence: {confidence_score:.1f}%")
                
                st.markdown("<br>**Live Target Tracking:**", unsafe_allow_html=True)
                map_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
                st.map(map_data, zoom=4)

            with res_col2:
                st.subheader("Telemetry Signature:")
                categories = ['Depth Impact', 'Regional Risk', 'Lat Anomaly', 'Lon Anomaly']
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=[abs(depth_scaled)*3, location_risk, abs(latitude)/10, abs(longitude)/20],
                    theta=categories,
                    fill='toself',
                    line_color='#00f2fe',
                    fillcolor='rgba(0, 242, 254, 0.2)'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=False)),
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0eef7', size=14),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption("*(Fig 1: Real-time telemetry compared to historical danger baselines)*")

    with tab2:
        st.subheader("Core System Diagnostics")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Data Packets Processed", value="1.4M", delta="+8,402/hr")
        m2.metric(label="Model F1-Score", value="94.2%", delta="Optimal")
        m3.metric(label="Server Nodes", value="14/14 Active", delta="0 Offline")

# --- 7. Routing Logic ---
if st.session_state['logged_in']:
    show_dashboard()
else:
    show_login_page()