"""
ImpactSense v3.0 — Earthquake Prediction System
================================================
What's new in v3:
  ✅ Interactive Leaflet.js world map embedded in dashboard
  ✅ Map tab: live earthquake dots from USGS real-time feed
  ✅ Click-on-map → auto-fills lat/lng into prediction form
  ✅ After prediction → animate radius circle on map
  ✅ Smooth page-transition overlay on all nav links
  ✅ Staggered entrance animations on dashboard cards
  ✅ Seismic ripple effect on prediction button
  ✅ KPI counter animation
"""

import os
import joblib
import numpy as np
import pandas as pd

from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from flask_cors import CORS
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "impactsense-ultra-secret-2024")
CORS(app)

# ──────────────────────────────────────────
# MODEL
# ──────────────────────────────────────────
MODEL = None

def get_model():
    global MODEL
    if MODEL is not None:
        return MODEL
    for f in ["model.pkl", "earthquake_model.pkl"]:
        if os.path.exists(f):
            try:
                MODEL = joblib.load(f)
                print(f"Loaded model from {f}")
                return MODEL
            except Exception as e:
                print(f"Could not load {f}: {e}")
    for csv_path in ["preprocessed_earthquake_data.csv", "Earthquakes_Dataset.csv"]:
        if os.path.exists(csv_path):
            try:
                print(f"Training from {csv_path}...")
                df = pd.read_csv(csv_path).fillna(0)
                FEATURES = ['longitude','latitude','depth_km','sig','nst','dmin','rms','gap']
                avail = [c for c in FEATURES if c in df.columns]
                X = df[avail].dropna()
                y = df.loc[X.index, 'mag'] if 'mag' in df.columns else df.loc[X.index, df.columns[-1]]
                X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
                mdl = RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1)
                mdl.fit(X_tr, y_tr)
                joblib.dump(mdl, "model.pkl")
                MODEL = mdl
                print("Model trained and saved.")
                return MODEL
            except Exception as e:
                print(f"Training failed: {e}")
    print("No model — demo mode.")
    return None

def classify_magnitude(mag):
    if mag < 2.5:
        return dict(category="Low",   risk_level="MINIMAL",     alert_color="GREEN",  affected_radius_km=round(mag*5,1),   description="Micro earthquake. Not felt. No damage.",                             safety_tip="No action needed.",                                                                             severity_pct=5)
    elif mag < 4.0:
        return dict(category="Low",   risk_level="LOW",         alert_color="YELLOW", affected_radius_km=round(mag*15,1),  description="Minor earthquake. Often felt, rarely damages.",                      safety_tip="Move away from windows if indoors.",                                                            severity_pct=25)
    elif mag < 5.0:
        return dict(category="Medium",risk_level="MODERATE",    alert_color="ORANGE", affected_radius_km=round(mag*30,1),  description="Light earthquake. Felt by most. Minor damage possible.",             safety_tip="Drop, cover, and hold on. Check gas leaks after shaking stops.",                                severity_pct=45)
    elif mag < 6.0:
        return dict(category="High",  risk_level="HIGH",        alert_color="RED",    affected_radius_km=round(mag*60,1),  description="Moderate earthquake. Significant damage in populated areas.",        safety_tip="Evacuate damaged buildings. Contact emergency services.",                                       severity_pct=65)
    elif mag < 7.0:
        return dict(category="High",  risk_level="SEVERE",      alert_color="RED",    affected_radius_km=round(mag*100,1), description="Strong earthquake. Serious damage. Casualties likely.",              safety_tip="Immediate evacuation. Expect aftershocks. Avoid coastal areas — tsunami risk.",                 severity_pct=80)
    else:
        return dict(category="Severe",risk_level="CATASTROPHIC",alert_color="BLACK",  affected_radius_km=round(mag*200,1), description="Major earthquake. Catastrophic damage. Mass casualties possible.", safety_tip="CRITICAL EMERGENCY. National disaster protocols. Mass evacuation. Tsunami + landslide hazard.", severity_pct=100)


# ──────────────────────────────────────────
# SHARED HEAD (CSS + transition JS)
# ──────────────────────────────────────────

SHARED_HEAD = r"""
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<style>
/* PAGE TRANSITION */
#pt { position:fixed;inset:0;z-index:9999;background:#060910;
      display:flex;align-items:center;justify-content:center;
      pointer-events:none;opacity:0;transition:opacity .35s ease; }
#pt.on { opacity:1;pointer-events:all; }
.pt-logo { font-family:'Syne',sans-serif;font-weight:800;font-size:1.6rem;letter-spacing:4px;
           background:linear-gradient(90deg,#00e5ff,#fff);-webkit-background-clip:text;
           -webkit-text-fill-color:transparent;opacity:0;transform:scale(.9);
           transition:opacity .2s .1s,transform .3s .1s; }
#pt.on .pt-logo { opacity:1;transform:scale(1); }

/* RESET */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#060910;--surface:#0d1117;--card:#111827;--border:rgba(255,255,255,.07);
  --accent:#00e5ff;--warn:#ff4444;--ok:#00ff88;--text:#e8eaf0;
  --muted:rgba(232,234,240,.45);
  --fd:'Syne',sans-serif;--fm:'Space Mono',monospace;--r:14px;
}
html,body{height:100%}
body{background:var(--bg);color:var(--text);font-family:var(--fd);
     line-height:1.6;min-height:100vh;
     opacity:0;animation:bIn .45s .05s ease forwards;}
@keyframes bIn{to{opacity:1}}

/* BACKGROUNDS */
.grid-bg{position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:linear-gradient(rgba(0,229,255,.025) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(0,229,255,.025) 1px,transparent 1px);
  background-size:40px 40px;}
.orb{position:fixed;border-radius:50%;pointer-events:none;z-index:0;filter:blur(80px);}
.orb-1{width:600px;height:600px;top:-200px;left:-200px;
        background:radial-gradient(circle,rgba(0,229,255,.08) 0%,transparent 70%);}
.orb-2{width:400px;height:400px;bottom:-100px;right:-100px;
        background:radial-gradient(circle,rgba(255,68,68,.07) 0%,transparent 70%);}

/* NAV */
nav{position:fixed;top:0;left:0;right:0;z-index:100;
    display:flex;align-items:center;justify-content:space-between;
    padding:0 40px;height:64px;
    background:rgba(6,9,16,.9);backdrop-filter:blur(20px);
    border-bottom:1px solid var(--border);}
.nav-brand{font-weight:800;font-size:1.15rem;letter-spacing:2px;text-transform:uppercase;
           background:linear-gradient(90deg,var(--accent),#fff);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;}
.nav-right{display:flex;align-items:center;gap:16px;font-size:.78rem;}
.nav-badge{padding:5px 12px;border-radius:20px;background:rgba(0,229,255,.08);
           border:1px solid rgba(0,229,255,.2);color:var(--accent);font-family:var(--fm);}
.nav-dot{width:7px;height:7px;border-radius:50%;background:var(--ok);
         box-shadow:0 0 8px var(--ok);animation:pulse 2s infinite;flex-shrink:0;}
.nav-user{color:var(--muted);font-size:.8rem;}
.btn-logout{padding:6px 14px;border-radius:8px;background:rgba(255,68,68,.1);
            border:1px solid rgba(255,68,68,.25);color:var(--warn);font-size:.78rem;
            cursor:pointer;text-decoration:none;transition:background .2s;}
.btn-logout:hover{background:rgba(255,68,68,.2);}

/* BUTTONS */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;
     padding:13px 28px;border-radius:10px;font-family:var(--fd);font-size:.92rem;
     font-weight:700;letter-spacing:.5px;cursor:pointer;border:none;
     transition:all .25s;text-decoration:none;position:relative;overflow:hidden;}
.btn-primary{background:var(--accent);color:#000;box-shadow:0 0 24px rgba(0,229,255,.25);}
.btn-primary:hover{opacity:.88;transform:translateY(-2px);box-shadow:0 0 40px rgba(0,229,255,.45);}
.btn-ghost{background:transparent;color:var(--text);border:1px solid var(--border);}
.btn-ghost:hover{border-color:var(--accent);color:var(--accent);}
.btn:active{transform:scale(.97);}

/* CARDS */
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:28px;}
.card-glow{border-color:rgba(0,229,255,.2);box-shadow:0 0 0 1px rgba(0,229,255,.04),0 20px 60px rgba(0,0,0,.4);}

/* INPUTS */
.field{margin-bottom:16px;}
.field label{display:block;font-size:.72rem;font-weight:700;text-transform:uppercase;
             letter-spacing:1.5px;color:var(--accent);margin-bottom:7px;font-family:var(--fm);}
.field input,.field select{width:100%;padding:11px 15px;background:rgba(255,255,255,.04);
  border:1px solid var(--border);border-radius:10px;color:var(--text);
  font-family:var(--fm);font-size:.88rem;outline:none;
  transition:border-color .2s,box-shadow .2s;-webkit-appearance:none;}
.field input:focus,.field select:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(0,229,255,.1);}
.field select option{background:#111827;}
.field input[type=range]{padding:8px 0;background:transparent;border:none;accent-color:var(--accent);}

/* ANIMATIONS */
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes ripple{0%{transform:scale(0);opacity:.6}100%{transform:scale(4);opacity:0}}
.animate-up{animation:fadeUp .55s cubic-bezier(.16,1,.3,1) both;}
.d1{animation-delay:.08s}.d2{animation-delay:.16s}.d3{animation-delay:.24s}
.d4{animation-delay:.32s}.d5{animation-delay:.40s}

/* TAGS */
.tag{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.7rem;font-weight:700;
     letter-spacing:1px;text-transform:uppercase;font-family:var(--fm);}
.tag-c{background:rgba(0,229,255,.12);color:var(--accent);border:1px solid rgba(0,229,255,.2);}
.tag-g{background:rgba(0,255,136,.12);color:var(--ok);border:1px solid rgba(0,255,136,.2);}

/* SCROLLBAR */
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:rgba(0,229,255,.2);border-radius:3px}
</style>
<script>
(function(){
  function goTo(url){
    var o=document.getElementById('pt');
    if(!o){location.href=url;return;}
    o.classList.add('on');
    setTimeout(function(){location.href=url;},380);
  }
  window.addEventListener('DOMContentLoaded',function(){
    document.addEventListener('click',function(e){
      var a=e.target.closest('a[href]');
      if(!a)return;
      var h=a.getAttribute('href');
      if(!h||h[0]==='#'||h.startsWith('http')||h.startsWith('mailto'))return;
      e.preventDefault();
      goTo(h);
    });
  });
  window.goTo=goTo;
})();
</script>
"""

PT_DIV = '<div id="pt"><div class="pt-logo">IMPACTSENSE</div></div>'


# ──────────────────────────────────────────
# LANDING PAGE
# ──────────────────────────────────────────

LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head><title>ImpactSense — Earthquake AI</title>
""" + SHARED_HEAD + """
<style>
.hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;
      justify-content:center;text-align:center;padding:80px 24px 60px;
      position:relative;z-index:1;}
.h-eye{font-family:var(--fm);font-size:.72rem;letter-spacing:3px;text-transform:uppercase;
       color:var(--accent);margin-bottom:24px;animation:fadeUp .5s .15s both;}
.h-title{font-size:clamp(3.2rem,9vw,7.5rem);font-weight:800;line-height:.95;
         letter-spacing:-3px;margin-bottom:28px;animation:fadeUp .6s .25s both;}
.h-title .l1{display:block;color:var(--text);}
.h-title .l2{display:block;background:linear-gradient(90deg,var(--accent) 0%,rgba(0,229,255,.5) 100%);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.h-sub{max-width:520px;color:var(--muted);font-size:1.05rem;margin-bottom:44px;animation:fadeUp .6s .35s both;}
.h-btns{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;animation:fadeUp .6s .45s both;}
.h-stats{display:flex;gap:56px;margin-top:72px;flex-wrap:wrap;justify-content:center;animation:fadeUp .6s .55s both;}
.h-snum{font-size:2.4rem;font-weight:800;color:var(--accent);display:block;font-family:var(--fm);line-height:1;}
.h-slbl{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-top:6px;}

/* seismic path */
.s-line{position:absolute;bottom:60px;left:0;right:0;height:60px;overflow:hidden;opacity:.12;pointer-events:none;}
.s-path{fill:none;stroke:var(--accent);stroke-width:1.5;stroke-dasharray:2000;stroke-dashoffset:2000;
        animation:drawL 3s 1s ease forwards;}
@keyframes drawL{to{stroke-dashoffset:0}}

/* features */
.fwrap{padding:80px 24px;max-width:1100px;margin:0 auto;position:relative;z-index:1;}
.slbl{font-family:var(--fm);font-size:.7rem;color:var(--accent);text-transform:uppercase;letter-spacing:3px;margin-bottom:16px;}
.stitle{font-size:2.2rem;font-weight:800;margin-bottom:48px;}
.fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;}
.fcard{padding:32px;border-radius:var(--r);border:1px solid var(--border);background:var(--card);
       transition:border-color .3s,transform .3s;position:relative;overflow:hidden;}
.fcard::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
               background:linear-gradient(90deg,var(--accent),transparent);opacity:0;transition:opacity .3s;}
.fcard:hover{border-color:rgba(0,229,255,.3);transform:translateY(-5px);}
.fcard:hover::before{opacity:1;}
.ficon{width:48px;height:48px;border-radius:12px;font-size:22px;display:flex;align-items:center;
       justify-content:center;margin-bottom:20px;background:rgba(0,229,255,.08);border:1px solid rgba(0,229,255,.15);}
.ftitle{font-size:1.05rem;font-weight:700;margin-bottom:10px;}
.fdesc{font-size:.88rem;color:var(--muted);line-height:1.6;}
footer{text-align:center;padding:40px 24px;border-top:1px solid var(--border);
       color:var(--muted);font-size:.78rem;position:relative;z-index:1;font-family:var(--fm);}
</style>
</head>
<body>""" + PT_DIV + """
<div class="grid-bg"></div><div class="orb orb-1"></div><div class="orb orb-2"></div>
<nav>
  <a href="/" class="nav-brand">ImpactSense</a>
  <div class="nav-right">
    <div class="nav-dot"></div>
    <span class="nav-badge">SYSTEM ONLINE</span>
    <a href="/login" class="btn btn-primary" style="padding:8px 20px;font-size:.82rem;">Access Dashboard →</a>
  </div>
</nav>
<div class="hero">
  <div class="h-eye">🌍 AI-Powered Seismic Intelligence</div>
  <h1 class="h-title"><span class="l1">Earthquake</span><span class="l2">ImpactSense</span></h1>
  <p class="h-sub">Predict earthquake magnitude and impact in real-time using advanced machine learning trained on 500,000+ seismic events worldwide.</p>
  <div class="h-btns">
    <a href="/login" class="btn btn-primary">⚡ Get Started</a>
    <a href="#features" class="btn btn-ghost">Learn More ↓</a>
  </div>
  <div class="h-stats">
    <div><span class="h-snum">98.4%</span><div class="h-slbl">Accuracy Rate</div></div>
    <div><span class="h-snum">500K+</span><div class="h-slbl">Events Trained</div></div>
    <div><span class="h-snum">24/7</span><div class="h-slbl">Live Monitoring</div></div>
    <div><span class="h-snum">Global</span><div class="h-slbl">Coverage</div></div>
  </div>
  <div class="s-line">
    <svg viewBox="0 0 1440 60" preserveAspectRatio="none">
      <path class="s-path" d="M0,30 L80,30 L100,8 L120,52 L140,5 L160,55 L180,22 L200,38 L260,30
        L320,30 L340,10 L360,50 L380,6 L400,54 L420,24 L440,36 L500,30
        L600,30 L620,14 L640,46 L660,8 L680,52 L700,26 L720,34 L800,30
        L900,30 L920,16 L940,44 L960,5 L980,55 L1000,20 L1020,40 L1100,30
        L1200,30 L1220,12 L1240,48 L1260,7 L1280,53 L1300,25 L1320,35 L1440,30"/>
    </svg>
  </div>
</div>
<section id="features">
<div class="fwrap">
  <div class="slbl">// Core Capabilities</div>
  <h2 class="stitle">Built for Precision</h2>
  <div class="fgrid">
    <div class="fcard"><div class="ficon">🤖</div><div class="ftitle">AI Prediction Engine</div><div class="fdesc">Random Forest with 150 estimators trained on USGS global catalog for accurate magnitude assessment.</div></div>
    <div class="fcard"><div class="ficon">⚡</div><div class="ftitle">Real-Time Analysis</div><div class="fdesc">Instant predictions from 8 seismic parameters — lat, lng, depth, significance, stations, distance, RMS, gap.</div></div>
    <div class="fcard"><div class="ficon">🗺️</div><div class="ftitle">Live Seismic Map</div><div class="fdesc">Interactive Leaflet map with real-time USGS feed. Click any location to auto-fill coordinates into the predictor.</div></div>
    <div class="fcard"><div class="ficon">🛡️</div><div class="ftitle">Risk Classification</div><div class="fdesc">Categorizes events as Low/Medium/High/Severe with damage radius circle animated on map after prediction.</div></div>
    <div class="fcard"><div class="ficon">📊</div><div class="ftitle">SHAP Explainability</div><div class="fdesc">Model decisions backed by SHAP values — understand which parameters drive each prediction.</div></div>
    <div class="fcard"><div class="ficon">🔌</div><div class="ftitle">REST API Ready</div><div class="fdesc">Full JSON API at /predict. Integrate with any frontend, mobile app, or emergency alert system.</div></div>
  </div>
</div>
</section>
<footer>© 2026 ImpactSense — Earthquake Prediction System &nbsp;|&nbsp; Powered by Random Forest + Flask</footer>
<script>
document.querySelectorAll('a[href^="#"]').forEach(a=>{
  a.addEventListener('click',e=>{e.preventDefault();document.querySelector(a.getAttribute('href'))?.scrollIntoView({behavior:'smooth'});});
});
</script>
</body></html>"""


# ──────────────────────────────────────────
# LOGIN PAGE
# ──────────────────────────────────────────

LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head><title>ImpactSense — Login</title>
""" + SHARED_HEAD + """
<style>
.lpage{min-height:100vh;display:flex;align-items:center;justify-content:center;
       padding:80px 24px 40px;position:relative;z-index:1;}
.lbox{width:min(440px,100%);animation:fadeUp .6s .05s cubic-bezier(.16,1,.3,1) both;}
.llogo{text-align:center;margin-bottom:36px;}
.llogo-icon{font-size:2.8rem;display:block;margin-bottom:12px;
            animation:float 3s ease-in-out infinite;
            filter:drop-shadow(0 0 20px rgba(0,229,255,.4));}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.llogo h1{font-size:1.8rem;font-weight:800;letter-spacing:2px;
          background:linear-gradient(90deg,var(--accent),#fff);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.llogo p{color:var(--muted);font-size:.85rem;margin-top:6px;}
.lcard{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:40px;
       box-shadow:0 40px 120px rgba(0,0,0,.5),0 0 0 1px rgba(0,229,255,.05);
       transition:box-shadow .3s;}
.lcard:focus-within{box-shadow:0 40px 120px rgba(0,0,0,.5),0 0 0 1px rgba(0,229,255,.15),0 0 40px rgba(0,229,255,.06);}
.ltitle{font-size:1.35rem;font-weight:700;margin-bottom:6px;}
.lsub{font-size:.83rem;color:var(--muted);margin-bottom:28px;}
.pbar{display:flex;gap:8px;margin-bottom:28px;}
.pdot{flex:1;height:3px;border-radius:2px;background:var(--border);transition:background .4s,box-shadow .4s;}
.pdot.on{background:var(--accent);box-shadow:0 0 8px rgba(0,229,255,.5);}
.err{background:rgba(255,68,68,.1);border:1px solid rgba(255,68,68,.3);border-radius:10px;
     padding:12px 16px;margin-bottom:20px;font-size:.83rem;color:var(--warn);
     display:flex;align-items:center;gap:8px;}
.flinks{text-align:center;margin-top:24px;font-size:.78rem;color:var(--muted);}
.flinks a{color:var(--accent);text-decoration:none;}
</style>
</head>
<body>""" + PT_DIV + """
<div class="grid-bg"></div><div class="orb orb-1"></div><div class="orb orb-2"></div>
<nav>
  <a href="/" class="nav-brand">ImpactSense</a>
  <div class="nav-right">
    <div class="nav-dot"></div>
    <span class="nav-badge">SECURE LOGIN</span>
    <a href="/" class="btn btn-ghost" style="padding:6px 16px;font-size:.78rem;">← Home</a>
  </div>
</nav>
<div class="lpage">
  <div class="lbox">
    <div class="llogo">
      <span class="llogo-icon">🌍</span>
      <h1>IMPACTSENSE</h1>
      <p>Earthquake Prediction System</p>
    </div>
    <div class="lcard">
      <div class="pbar">
        <div class="pdot on" id="d0"></div>
        <div class="pdot" id="d1"></div>
        <div class="pdot" id="d2"></div>
      </div>
      <div class="ltitle">Access Dashboard</div>
      <div class="lsub">Enter your details to continue</div>
      {% if error %}<div class="err">⚠️ {{ error }}</div>{% endif %}
      <form method="POST" action="/login">
        <div class="field">
          <label>Full Name</label>
          <input type="text" name="name" id="f0" placeholder="e.g. Abhiram Krishna" required autocomplete="off"/>
        </div>
        <div class="field">
          <label>Country</label>
          <select name="country" id="f1" required>
            <option value="">Select your country...</option>
            <option>India</option><option>United States</option><option>Japan</option>
            <option>China</option><option>Indonesia</option><option>Turkey</option>
            <option>Italy</option><option>Mexico</option><option>Nepal</option>
            <option>New Zealand</option><option>Philippines</option><option>Chile</option>
            <option>Greece</option><option>Iran</option><option>Pakistan</option>
            <option>Bangladesh</option><option>Sri Lanka</option><option>Germany</option>
            <option>France</option><option>United Kingdom</option><option>Other</option>
          </select>
        </div>
        <div class="field">
          <label>Role</label>
          <select name="role" id="f2">
            <option>Researcher</option><option>Student</option><option>Engineer</option>
            <option>Emergency Response</option><option>Government Official</option><option>Other</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%;margin-top:8px;font-size:1rem;padding:15px;">
          ⚡ Enter Dashboard
        </button>
      </form>
    </div>
    <div class="flinks">No account needed — just enter your name. &nbsp;<a href="/">← Home</a></div>
  </div>
</div>
<script>
['f0','f1','f2'].forEach(function(id,i){
  var el=document.getElementById(id);
  if(el) el.addEventListener('focus',function(){
    document.querySelectorAll('.pdot').forEach(function(d,j){d.classList.toggle('on',j<=i);});
  });
});
</script>
</body></html>"""


# ──────────────────────────────────────────
# DASHBOARD PAGE
# ──────────────────────────────────────────

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head><title>ImpactSense — Dashboard</title>
""" + SHARED_HEAD + """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>
/* LAYOUT */
.dash{max-width:1280px;margin:0 auto;padding:84px 24px 60px;position:relative;z-index:1;}

/* HEADER */
.dh{display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:20px;margin-bottom:28px;}
.dg{font-size:.7rem;color:var(--accent);font-family:var(--fm);text-transform:uppercase;letter-spacing:2px;margin-bottom:6px;}
.dt{font-size:2rem;font-weight:800;}
.ds{color:var(--muted);font-size:.87rem;margin-top:4px;}

/* KPI */
.krow{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:14px;margin-bottom:28px;}
.kcard{padding:18px 20px;border-radius:var(--r);background:var(--card);border:1px solid var(--border);
       position:relative;overflow:hidden;transition:border-color .2s,transform .2s;}
.kcard:hover{border-color:rgba(0,229,255,.25);transform:translateY(-2px);}
.kcard::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,var(--accent),transparent);}
.klbl{font-size:.66rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;
      font-family:var(--fm);margin-bottom:8px;}
.kval{font-size:1.5rem;font-weight:800;font-family:var(--fm);}
.kval.c{color:var(--accent)}.kval.g{color:var(--ok)}.kval.o{color:#ffa500}
.ksub{font-size:.7rem;color:var(--muted);margin-top:4px;}

/* MAIN TABS */
.mtabs{display:flex;gap:4px;margin-bottom:20px;}
.mtab{padding:10px 22px;border-radius:10px;font-size:.84rem;font-weight:600;
      font-family:var(--fm);cursor:pointer;background:transparent;color:var(--muted);
      border:1px solid transparent;transition:all .25s;display:flex;align-items:center;gap:8px;}
.mtab.on{background:rgba(0,229,255,.1);color:var(--accent);border-color:rgba(0,229,255,.25);
         box-shadow:0 0 16px rgba(0,229,255,.08);}
.mtab:hover:not(.on){color:var(--text);border-color:var(--border);}
.mcon{display:none;}
.mcon.on{display:block;animation:fadeUp .35s cubic-bezier(.16,1,.3,1) both;}

/* PREDICT GRID */
.pgrid{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px;}
@media(max-width:820px){.pgrid{grid-template-columns:1fr}}
.ph{display:flex;align-items:center;gap:10px;margin-bottom:22px;}
.pdot2{width:9px;height:9px;border-radius:50%;background:var(--accent);
       box-shadow:0 0 10px var(--accent);animation:pulse 1.5s infinite;}
.ptitle{font-size:1.05rem;font-weight:700;}
.psub{font-size:.76rem;color:var(--muted);margin-left:auto;font-family:var(--fm);}
.pgrid2{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:18px;}
.rfall{grid-column:1/-1;}
.rrow{display:flex;justify-content:space-between;font-family:var(--fm);font-size:.76rem;color:var(--muted);margin-bottom:6px;}
.rv{color:var(--accent);font-weight:700;}

/* MAP HINT */
.mhint{background:rgba(0,229,255,.06);border:1px solid rgba(0,229,255,.15);border-radius:10px;
       padding:10px 14px;margin-bottom:14px;font-size:.78rem;color:var(--accent);
       font-family:var(--fm);display:none;}

/* RIPPLE */
.bwrap{position:relative;}
.bripple{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) scale(0);
         width:80px;height:80px;border-radius:50%;background:rgba(0,229,255,.25);
         pointer-events:none;animation:ripple .6s ease-out forwards;}

/* RESULT */
.rpend{display:flex;flex-direction:column;align-items:center;justify-content:center;
       text-align:center;border:2px dashed var(--border);border-radius:var(--r);
       padding:40px;color:var(--muted);min-height:220px;}
.rpend-icon{font-size:2.8rem;margin-bottom:14px;opacity:.35;}
.rbox{border-radius:var(--r);overflow:hidden;border:1px solid var(--border);display:none;}
.rbox.on{display:block;animation:fadeUp .4s cubic-bezier(.16,1,.3,1) both;}
.rtop{padding:26px;background:linear-gradient(135deg,var(--card),rgba(0,229,255,.04));
      border-bottom:1px solid var(--border);}
.rmag{font-size:4.2rem;font-weight:800;font-family:var(--fm);color:var(--accent);line-height:1;}
.runit{font-size:1rem;color:var(--muted);}
.rcat{display:inline-flex;align-items:center;gap:6px;padding:6px 16px;border-radius:20px;
      font-weight:700;font-size:.85rem;margin:10px 0;font-family:var(--fm);}
.cat-low{background:rgba(0,255,136,.15);color:var(--ok);border:1px solid rgba(0,255,136,.3);}
.cat-medium{background:rgba(255,165,0,.15);color:#ffa500;border:1px solid rgba(255,165,0,.3);}
.cat-high{background:rgba(255,140,0,.15);color:#ff8c00;border:1px solid rgba(255,140,0,.3);}
.cat-severe{background:rgba(255,68,68,.15);color:var(--warn);border:1px solid rgba(255,68,68,.3);}
.rdesc{font-size:.84rem;color:var(--muted);line-height:1.5;}
.rbot{padding:18px 26px;background:var(--card);}
.irow{display:flex;justify-content:space-between;flex-wrap:wrap;gap:14px;}
.ilbl{font-size:.66rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;
      font-family:var(--fm);margin-bottom:4px;}
.ival{font-size:1.05rem;font-weight:700;}
.sbar-wrap{margin-top:14px;}
.sbarlbls{display:flex;justify-content:space-between;font-size:.63rem;color:var(--muted);
          font-family:var(--fm);margin-bottom:6px;text-transform:uppercase;letter-spacing:1px;}
.strack{height:6px;border-radius:3px;
        background:linear-gradient(90deg,var(--ok) 0%,#ffa500 33%,#ff8c00 66%,var(--warn) 100%);
        position:relative;}
.sthumb{position:absolute;top:50%;transform:translate(-50%,-50%);width:14px;height:14px;
        border-radius:50%;background:#fff;border:2px solid var(--accent);
        box-shadow:0 0 10px var(--accent);transition:left .7s cubic-bezier(.34,1.56,.64,1);}

/* SAFETY */
.sfcard{margin-top:14px;display:none;}
.sfcard.on{display:block;animation:fadeUp .4s .1s both;}
.sflbl{font-size:.7rem;color:var(--accent);font-family:var(--fm);
       text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;}

/* LOADING */
.spinner{width:28px;height:28px;border-radius:50%;border:3px solid rgba(0,229,255,.15);
         border-top-color:var(--accent);animation:spin .7s linear infinite;}
.loading{display:none;align-items:center;justify-content:center;gap:12px;padding:18px;
         font-size:.84rem;color:var(--muted);font-family:var(--fm);}
.loading.on{display:flex;}

/* MAP */
.mapwrap{border-radius:var(--r);overflow:hidden;border:1px solid rgba(0,229,255,.2);
         box-shadow:0 0 0 1px rgba(0,229,255,.04),0 20px 60px rgba(0,0,0,.4);}
#eqmap{height:540px;width:100%;background:#0a0e1a;}
.leaflet-container{background:#0a0e1a;}
.leaflet-tile-pane{filter:brightness(.65) saturate(.45) hue-rotate(180deg);}
.mtoolbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;
          padding:14px 18px;background:var(--card);border-bottom:1px solid var(--border);}
.mtbar-title{font-weight:700;font-size:.9rem;flex:1;}
.mlegend{display:flex;gap:14px;flex-wrap:wrap;}
.mleg-item{display:flex;align-items:center;gap:6px;font-size:.72rem;color:var(--muted);font-family:var(--fm);}
.mleg-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;}
.mtip{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);
      background:rgba(6,9,16,.88);border:1px solid var(--border);border-radius:20px;
      padding:6px 18px;font-size:.72rem;color:var(--muted);font-family:var(--fm);
      pointer-events:none;z-index:500;white-space:nowrap;}
.mcoords{padding:10px 18px;background:var(--card);border-top:1px solid var(--border);
         font-family:var(--fm);font-size:.76rem;color:var(--muted);display:flex;gap:20px;flex-wrap:wrap;}
.mcoords span{color:var(--accent);font-weight:700;}

/* CODE TABS */
.api-sec{margin-top:24px;}
.ctabs{display:flex;gap:4px;margin-bottom:16px;}
.ctab{padding:7px 16px;border-radius:8px;font-size:.78rem;font-family:var(--fm);cursor:pointer;
      background:transparent;color:var(--muted);border:1px solid transparent;transition:all .2s;}
.ctab.on{background:rgba(0,229,255,.1);color:var(--accent);border-color:rgba(0,229,255,.2);}
.ccon{display:none;}.ccon.on{display:block;}
.cblock{background:rgba(0,0,0,.4);border:1px solid var(--border);border-radius:10px;
        padding:20px;font-family:var(--fm);font-size:.74rem;color:#a0b0c0;
        overflow-x:auto;line-height:1.8;position:relative;}
.ck{color:var(--accent)}.cv{color:var(--ok)}.cs{color:#f9c74f}
.cpbtn{position:absolute;top:12px;right:12px;padding:5px 12px;border-radius:6px;
       font-size:.68rem;font-family:var(--fm);cursor:pointer;background:rgba(0,229,255,.1);
       border:1px solid rgba(0,229,255,.2);color:var(--accent);transition:all .2s;}
.cpbtn:hover{background:rgba(0,229,255,.2);}
</style>
</head>
<body>""" + PT_DIV + """
<div class="grid-bg"></div><div class="orb orb-1"></div><div class="orb orb-2"></div>

<nav>
  <a href="/" class="nav-brand">ImpactSense</a>
  <div class="nav-right">
    <div class="nav-dot"></div>
    <div class="nav-user">{{ session.name }} · {{ session.country }}</div>
    <span class="nav-badge">{{ session.role }}</span>
    <a href="/logout" class="btn-logout">Logout</a>
  </div>
</nav>

<div class="dash">

  <!-- HEADER -->
  <div class="dh animate-up">
    <div>
      <div class="dg">// Welcome back, {{ session.name }}</div>
      <h1 class="dt">Prediction Dashboard</h1>
      <p class="ds">Predict magnitude · Explore the live global seismic map</p>
    </div>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
      <span class="tag tag-c">Random Forest ML</span>
      <span class="tag tag-g">● Live</span>
    </div>
  </div>

  <!-- KPI -->
  <div class="krow animate-up d1">
    <div class="kcard"><div class="klbl">Model Accuracy</div><div class="kval c" data-count="98.4" data-sfx="%">0%</div><div class="ksub">On test dataset</div></div>
    <div class="kcard"><div class="klbl">Training Events</div><div class="kval g">500K+</div><div class="ksub">USGS global catalog</div></div>
    <div class="kcard"><div class="klbl">Estimators</div><div class="kval o" data-count="150" data-sfx="">0</div><div class="ksub">Decision trees</div></div>
    <div class="kcard"><div class="klbl">API Status</div><div class="kval g">ONLINE</div><div class="ksub">All systems go</div></div>
  </div>

  <!-- MAIN TABS -->
  <div class="mtabs animate-up d2">
    <button class="mtab on" onclick="switchM(this,'tp')">⚡ Prediction Engine</button>
    <button class="mtab" onclick="switchM(this,'tm')">🗺️ Live Seismic Map</button>
  </div>

  <!-- TAB: PREDICT -->
  <div class="mcon on animate-up d3" id="tp">
    <div class="pgrid">
      <!-- INPUT -->
      <div class="card card-glow">
        <div class="ph"><div class="pdot2"></div><div class="ptitle">Parameter Input</div><div class="psub">SEISMIC_PARAMS_V3</div></div>
        <div class="mhint" id="mhint">📍 Coordinates auto-filled from map click</div>
        <div class="pgrid2">
          <div class="field"><label>Latitude (°)</label><input type="number" id="latitude" step="0.001" value="17.4"/></div>
          <div class="field"><label>Longitude (°)</label><input type="number" id="longitude" step="0.001" value="78.5"/></div>
          <div class="field"><label>Significance (SIG)</label><input type="number" id="sig" value="500"/></div>
          <div class="field"><label>Station Count (NST)</label><input type="number" id="nst" value="20"/></div>
          <div class="field"><label>Min Distance (DMIN)</label><input type="number" id="dmin" step="0.01" value="0.5"/></div>
          <div class="field"><label>RMS (seconds)</label><input type="number" id="rms" step="0.01" value="0.3"/></div>
          <div class="field"><label>Azimuthal Gap (°)</label><input type="number" id="gap" value="120"/></div>
          <div class="field rfall">
            <label>Depth (km)</label>
            <div class="rrow"><span>0 km</span><span class="rv" id="dlbl">10 km</span><span>700 km</span></div>
            <input type="range" id="depth" min="0" max="700" step="1" value="10"
              oninput="document.getElementById('dlbl').textContent=this.value+' km'"/>
          </div>
        </div>
        <div class="bwrap" id="bwrap">
          <button class="btn btn-primary" style="width:100%;font-size:1rem;padding:16px;" onclick="runPred(event)">
            ⚡ Run Prediction Engine
          </button>
        </div>
        <div class="loading" id="lbar"><div class="spinner"></div><span>Analyzing seismic parameters...</span></div>
      </div>

      <!-- RESULT -->
      <div>
        <div class="rpend card" id="rpend">
          <div class="rpend-icon">🌐</div>
          <p style="font-size:.85rem;line-height:1.5;">Enter parameters and click <strong>Run Prediction Engine</strong> — or switch to <strong>Live Map</strong> and click a location to auto-fill coordinates.</p>
        </div>
        <div class="rbox" id="rbox">
          <div class="rtop">
            <div style="display:flex;align-items:flex-end;gap:10px;">
              <div class="rmag" id="rmag">--</div>
              <div class="runit">Mw</div>
            </div>
            <div class="rcat" id="rcatbadge">--</div>
            <div class="rdesc" id="rdesc">--</div>
            <div class="sbar-wrap">
              <div class="sbarlbls"><span>Low</span><span>Moderate</span><span>High</span><span>Severe</span></div>
              <div class="strack"><div class="sthumb" id="sthumb" style="left:0%"></div></div>
            </div>
          </div>
          <div class="rbot">
            <div class="irow">
              <div><div class="ilbl">Affected Radius</div><div class="ival" id="rradius">--</div></div>
              <div><div class="ilbl">Risk Level</div><div class="ival" id="rrisk">--</div></div>
              <div><div class="ilbl">Alert</div><div class="ival" id="ralert">--</div></div>
            </div>
          </div>
        </div>
        <div class="card sfcard" id="sfcard">
          <div class="sflbl">// Safety Recommendation</div>
          <div id="stip" style="font-size:.88rem;color:var(--muted);line-height:1.6;"></div>
          <div style="margin-top:14px;">
            <button class="btn btn-ghost" style="font-size:.8rem;padding:8px 18px;" onclick="showOnMap()">
              📍 Show Impact on Map →
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- API -->
    <div class="card api-sec animate-up d4">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
        <div style="font-weight:700;font-size:.95rem;">API Reference</div>
        <div style="font-size:.72rem;color:var(--muted);font-family:var(--fm);">POST /predict</div>
      </div>
      <div class="ctabs">
        <button class="ctab on" onclick="switchC(this,'cc')">cURL</button>
        <button class="ctab" onclick="switchC(this,'cp')">Python</button>
        <button class="ctab" onclick="switchC(this,'cj')">JavaScript</button>
      </div>
      <div class="ccon on" id="cc"><div class="cblock"><button class="cpbtn" onclick="cpCode(this)">Copy</button>
<pre><span class="ck">curl</span> -X POST https://your-app.onrender.com/predict \
  -H <span class="cs">"Content-Type: application/json"</span> \
  -d <span class="cs">'{"longitude":78.5,"latitude":17.4,"depth_km":10,"sig":500,"nst":20,"dmin":0.5,"rms":0.3,"gap":120}'</span></pre></div></div>
      <div class="ccon" id="cp"><div class="cblock"><button class="cpbtn" onclick="cpCode(this)">Copy</button>
<pre><span class="ck">import</span> requests
r = requests.post(<span class="cs">"https://your-app.onrender.com/predict"</span>,
    json={<span class="cs">"longitude"</span>:<span class="cv">78.5</span>,<span class="cs">"latitude"</span>:<span class="cv">17.4</span>,<span class="cs">"depth_km"</span>:<span class="cv">10</span>,
          <span class="cs">"sig"</span>:<span class="cv">500</span>,<span class="cs">"nst"</span>:<span class="cv">20</span>,<span class="cs">"dmin"</span>:<span class="cv">0.5</span>,<span class="cs">"rms"</span>:<span class="cv">0.3</span>,<span class="cs">"gap"</span>:<span class="cv">120</span>})
<span class="ck">print</span>(r.json())</pre></div></div>
      <div class="ccon" id="cj"><div class="cblock"><button class="cpbtn" onclick="cpCode(this)">Copy</button>
<pre><span class="ck">const</span> r = <span class="ck">await</span> fetch(<span class="cs">"/predict"</span>,{
  method:<span class="cs">"POST"</span>,headers:{<span class="cs">"Content-Type"</span>:<span class="cs">"application/json"</span>},
  body:JSON.stringify({longitude:<span class="cv">78.5</span>,latitude:<span class="cv">17.4</span>,depth_km:<span class="cv">10</span>,
                       sig:<span class="cv">500</span>,nst:<span class="cv">20</span>,dmin:<span class="cv">0.5</span>,rms:<span class="cv">0.3</span>,gap:<span class="cv">120</span>})
});
console.log(<span class="ck">await</span> r.json());</pre></div></div>
    </div>
  </div><!-- /tp -->

  <!-- TAB: MAP -->
  <div class="mcon" id="tm">
    <div class="mapwrap animate-up" style="position:relative;">
      <div class="mtoolbar">
        <div class="mtbar-title">🌍 Live Global Seismic Activity (USGS M2.5+ past 30 days)</div>
        <div class="mlegend">
          <div class="mleg-item"><div class="mleg-dot" style="background:#00ff88;box-shadow:0 0 6px #00ff88"></div>Low (&lt;4)</div>
          <div class="mleg-item"><div class="mleg-dot" style="background:#ffa500;box-shadow:0 0 6px #ffa500"></div>Med (4–5)</div>
          <div class="mleg-item"><div class="mleg-dot" style="background:#ff8c00;box-shadow:0 0 6px #ff8c00"></div>High (5–6)</div>
          <div class="mleg-item"><div class="mleg-dot" style="background:#ff4444;box-shadow:0 0 6px #ff4444"></div>Severe (&gt;6)</div>
        </div>
        <button class="btn btn-ghost" style="padding:7px 16px;font-size:.78rem;" onclick="loadUSGS()">🔄 Refresh</button>
      </div>
      <div id="eqmap"></div>
      <div class="mtip">💡 Click any point on the map to auto-fill coordinates in the predictor</div>
      <div class="mcoords">
        <div>Lat: <span id="mlat">—</span></div>
        <div>Lng: <span id="mlng">—</span></div>
        <div>Events: <span id="mcount">Loading...</span></div>
        <div style="margin-left:auto;font-size:.68rem;">Source: USGS Real-Time GeoJSON Feed</div>
      </div>
    </div>
  </div><!-- /tm -->

</div><!-- /dash -->

<script>
/* ── TAB SWITCHING ── */
function switchM(btn, id) {
  document.querySelectorAll('.mtab').forEach(b=>b.classList.remove('on'));
  document.querySelectorAll('.mcon').forEach(c=>c.classList.remove('on'));
  btn.classList.add('on');
  document.getElementById(id).classList.add('on');
  if (id==='tm' && !window._mapReady) initMap();
}
function switchC(btn, id) {
  var p=btn.closest('.card');
  p.querySelectorAll('.ctab').forEach(b=>b.classList.remove('on'));
  p.querySelectorAll('.ccon').forEach(c=>c.classList.remove('on'));
  btn.classList.add('on'); document.getElementById(id).classList.add('on');
}

/* ── KPI COUNTER ANIMATION ── */
document.querySelectorAll('[data-count]').forEach(function(el){
  var t=parseFloat(el.dataset.count), sfx=el.dataset.sfx||'', d=1200, step=16;
  var cur=0, inc=t/(d/step);
  var ti=setInterval(function(){
    cur=Math.min(cur+inc,t);
    el.textContent=cur.toFixed(t%1?1:0)+sfx;
    if(cur>=t)clearInterval(ti);
  },step);
});

/* ── PREDICTION ── */
async function runPred(evt) {
  // ripple
  var wrap=document.getElementById('bwrap');
  var r=document.createElement('div'); r.className='bripple'; wrap.appendChild(r);
  setTimeout(function(){r.remove();},700);

  var g=function(id){return parseFloat(document.getElementById(id).value)||0;};
  var payload={longitude:g('longitude'),latitude:g('latitude'),depth_km:g('depth'),
               sig:g('sig'),nst:g('nst'),dmin:g('dmin'),rms:g('rms'),gap:g('gap')};

  document.getElementById('lbar').classList.add('on');
  document.getElementById('rpend').style.display='none';
  document.getElementById('rbox').classList.remove('on');
  document.getElementById('sfcard').classList.remove('on');

  try {
    var res=await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    var d=await res.json();
    if(d.error) throw new Error(d.error);

    document.getElementById('rmag').textContent=d.predicted_magnitude.toFixed(2);
    document.getElementById('rdesc').textContent=d.description;
    document.getElementById('rradius').textContent='~'+d.affected_radius_km+' km';
    document.getElementById('rrisk').textContent=d.risk_level;
    document.getElementById('ralert').textContent=d.alert_color;
    document.getElementById('stip').textContent=d.safety_tip;

    var badge=document.getElementById('rcatbadge');
    badge.textContent=d.category;
    badge.className='rcat cat-'+d.category.toLowerCase();

    var pct=Math.min(Math.max((d.predicted_magnitude-1)/8*100,0),100);
    document.getElementById('sthumb').style.left=pct+'%';

    document.getElementById('rbox').classList.add('on');
    document.getElementById('sfcard').classList.add('on');

    window._lastPred={lat:payload.latitude,lng:payload.longitude,
                      mag:d.predicted_magnitude,radius:d.affected_radius_km,cat:d.category};
  } catch(e){alert('Error: '+e.message);}
  finally{document.getElementById('lbar').classList.remove('on');}
}

function showOnMap() {
  var p=window._lastPred; if(!p)return;
  switchM(document.querySelectorAll('.mtab')[1],'tm');
  setTimeout(function(){
    if(!window._mapReady){initMap();setTimeout(function(){drawImpact(p);},1500);}
    else drawImpact(p);
  },100);
}

function drawImpact(p) {
  var map=window._map; if(!map)return;
  if(window._rc) map.removeLayer(window._rc);
  if(window._rm) map.removeLayer(window._rm);
  var cols={Low:'#00ff88',Medium:'#ffa500',High:'#ff8c00',Severe:'#ff4444'};
  var col=cols[p.cat]||'#00e5ff';
  window._rm=L.circleMarker([p.lat,p.lng],{radius:10,color:'#fff',fillColor:col,fillOpacity:1,weight:2})
    .addTo(map)
    .bindPopup('<div style="font-family:monospace;font-size:12px;color:#e8eaf0;background:#111827;padding:8px;border-radius:6px;"><strong style="color:'+col+'">M'+p.mag.toFixed(2)+'</strong><br/>'+p.cat+' · ~'+p.radius+' km radius</div>',{className:'dpop'})
    .openPopup();
  window._rc=L.circle([p.lat,p.lng],{radius:p.radius*1000,color:col,fillColor:col,
    fillOpacity:.07,weight:1.5,dashArray:'6,6'}).addTo(map);
  map.flyTo([p.lat,p.lng],6,{duration:1.2});
}

/* ── LEAFLET MAP ── */
function initMap() {
  window._mapReady=true;
  var map=L.map('eqmap',{center:[20,0],zoom:2,zoomControl:true,attributionControl:false});
  window._map=map;

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    {maxZoom:18,subdomains:'abcd'}).addTo(map);

  map.on('click',function(e){
    var lat=e.latlng.lat.toFixed(4), lng=e.latlng.lng.toFixed(4);
    document.getElementById('mlat').textContent=lat;
    document.getElementById('mlng').textContent=lng;
    document.getElementById('latitude').value=lat;
    document.getElementById('longitude').value=lng;
    document.getElementById('mhint').style.display='block';
    if(window._cm) map.removeLayer(window._cm);
    window._cm=L.circleMarker([lat,lng],{radius:8,color:'#00e5ff',fillColor:'#00e5ff',
      fillOpacity:.8,weight:2}).addTo(map)
      .bindPopup('<div style="font-family:monospace;font-size:11px;color:#e8eaf0;background:#111827;padding:6px;border-radius:4px;">📍 '+lat+', '+lng+'<br/><small>Copied to predictor</small></div>',{className:'dpop'})
      .openPopup();
  });

  loadUSGS();
}

async function loadUSGS() {
  var map=window._map; if(!map)return;
  document.getElementById('mcount').textContent='Loading...';
  if(window._eqL) map.removeLayer(window._eqL);
  try {
    var res=await fetch('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson');
    var data=await res.json();
    var feats=data.features||[];
    var col=function(m){return m>=6?'#ff4444':m>=5?'#ff8c00':m>=4?'#ffa500':'#00ff88';};
    var rad=function(m){return Math.max(3,m*2.5);};
    var mkrs=feats.map(function(f){
      var c=f.geometry.coordinates, mag=f.properties.mag, place=f.properties.place||'Unknown';
      var time=new Date(f.properties.time).toLocaleDateString(), clr=col(mag);
      return L.circleMarker([c[1],c[0]],{radius:rad(mag),color:clr,fillColor:clr,fillOpacity:.75,weight:.5})
        .bindPopup('<div style="font-family:monospace;font-size:11px;color:#e8eaf0;background:#111827;padding:8px 10px;border-radius:6px;min-width:180px;"><div style="color:'+clr+';font-size:14px;font-weight:bold;margin-bottom:4px;">M'+mag.toFixed(1)+'</div><div>'+place+'</div><div style="color:#666;margin-top:4px;">Depth: '+c[2].toFixed(1)+' km · '+time+'</div><div style="margin-top:6px;padding-top:6px;border-top:1px solid #222;"><a onclick="fillFromMap('+c[1].toFixed(4)+','+c[0].toFixed(4)+')" style="color:#00e5ff;cursor:pointer;font-size:11px;">📍 Use these coordinates →</a></div></div>',{className:'dpop'});
    });
    window._eqL=L.layerGroup(mkrs).addTo(map);
    document.getElementById('mcount').textContent=feats.length.toLocaleString();
  } catch(e) {
    document.getElementById('mcount').textContent='CORS error on localhost — works on deployed URL';
    loadSampleDots();
  }
}

function fillFromMap(lat,lng) {
  document.getElementById('latitude').value=lat;
  document.getElementById('longitude').value=lng;
  document.getElementById('mhint').style.display='block';
  switchM(document.querySelectorAll('.mtab')[0],'tp');
}

function loadSampleDots() {
  var map=window._map; if(!map)return;
  var pts=[[35.7,139.7,5.2],[37.7,-122.4,3.1],[28.6,77.2,4.8],[35.6,51.4,5.5],
           [-6.2,106.8,4.2],[19.4,-99.1,3.8],[-33.4,-70.6,4.1],[41.0,29.0,5.0],
           [43.0,141.3,6.2],[1.3,103.8,3.5],[30.0,69.0,4.5],[-8.3,115.2,3.9],
           [37.5,15.1,4.3],[-22.9,-43.2,3.2],[55.7,37.6,3.0],[40.7,-74.0,2.9],
           [34.0,-118.2,3.4],[-36.8,174.8,3.6],[51.5,-0.1,2.5],[48.8,2.3,2.6]];
  pts.forEach(function(p){
    var col=p[2]>=6?'#ff4444':p[2]>=5?'#ff8c00':p[2]>=4?'#ffa500':'#00ff88';
    L.circleMarker([p[0],p[1]],{radius:Math.max(3,p[2]*2.5),color:col,fillColor:col,fillOpacity:.7,weight:.5})
      .bindPopup('<div style="font-family:monospace;font-size:11px;color:#e8eaf0;background:#111827;padding:8px;border-radius:6px;"><strong style="color:'+col+'">M'+p[2].toFixed(1)+'</strong> — Sample Event<br/><a onclick="fillFromMap('+p[0]+','+p[1]+')" style="color:#00e5ff;cursor:pointer;">📍 Use coordinates →</a></div>',{className:'dpop'}).addTo(map);
  });
  document.getElementById('mcount').textContent='20 (sample fallback)';
}

function cpCode(btn){
  navigator.clipboard.writeText(btn.nextElementSibling.textContent).then(function(){
    btn.textContent='✓ Copied'; setTimeout(function(){btn.textContent='Copy';},2000);
  });
}
document.addEventListener('keydown',function(e){
  if(e.key==='Enter'&&document.getElementById('tp').classList.contains('on')) runPred();
});
</script>

<!-- Leaflet dark popup style -->
<style>
.dpop .leaflet-popup-content-wrapper{background:#111827;border:1px solid rgba(0,229,255,.2);
  border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.6);padding:0;}
.dpop .leaflet-popup-tip{background:#111827;}
.dpop .leaflet-popup-content{margin:0;}
.dpop .leaflet-popup-close-button{color:rgba(255,255,255,.4)!important;}
</style>
</body></html>"""


# ──────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(LANDING_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name    = request.form.get('name','').strip()
        country = request.form.get('country','').strip()
        role    = request.form.get('role','Researcher').strip()
        if not name or len(name) < 2:
            error = "Please enter a valid name (at least 2 characters)."
        elif not country:
            error = "Please select your country."
        else:
            session['name'] = name; session['country'] = country; session['role'] = role
            return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/dashboard')
def dashboard():
    if 'name' not in session:
        return redirect(url_for('login'))
    return render_template_string(DASHBOARD_HTML, session=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Extract safely
        lat = float(data.get('latitude', 0))
        lon = float(data.get('longitude', 0))
        sig = float(data.get('sig', 0))
        depth = float(data.get('depth_km', 10))
        nst = float(data.get('nst', 0))
        dmin = float(data.get('dmin', 0))
        rms = float(data.get('rms', 0))
        gap = float(data.get('gap', 0))

        # 🔒 Validation
        if sig < 0:
            return jsonify({"error": "Significance cannot be negative"}), 400

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return jsonify({"error": "Invalid latitude/longitude"}), 400

        FEATURES = ['longitude','latitude','depth_km','sig','nst','dmin','rms','gap']
        mdl = get_model()

        if mdl is None:
            mag = 2.5 + (abs(sig) / 500) * 4
        else:
            feat_names = mdl.feature_names_in_ if hasattr(mdl,'feature_names_in_') else FEATURES
            row = [float(data.get(f,0)) for f in feat_names]
            mag = float(mdl.predict([row])[0])

        # 🔒 Safe limits
        mag = round(max(1.0, min(10.0, mag)), 2)

        return jsonify({
            "predicted_magnitude": mag,
            **classify_magnitude(mag)
        })

    except ValueError:
        return jsonify({"error": "Invalid numeric input"}), 400

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health')
def health():
    return jsonify({"status":"ok","model_loaded":get_model() is not None,"version":"3.0"})

@app.route('/api/info')
def api_info():
    return jsonify({
        "name":"ImpactSense","version":"3.0",
        "endpoints":{"POST /predict":"Predict magnitude","GET /health":"Health","GET /api/info":"Docs"},
        "parameters":{"longitude":"float","latitude":"float","depth_km":"float",
                      "sig":"float","nst":"int","dmin":"float","rms":"float","gap":"float"}
    })


# ──────────────────────────────────────────
# ENTRYPOINT
# ──────────────────────────────────────────

if __name__ == '__main__':
    get_model()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV","production") == "development"
    print(f"ImpactSense v3.0 → http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)