# 🌐 ImpactSense: Neural Earthquake Orchestration

**Live Application:** [impactsense.vercel.app](https://impactsense.vercel.app/)

ImpactSense is a high-fidelity earthquake prediction and monitoring system that blends advanced machine learning prototypes with an immersive cyberpunk aesthetic. It leverages historical seismic data to predict impact levels and visualizes global seismic activity in real-time.

---

## ⚡ Core Features

- **🧠 Neural Prediction Engine**: A Scikit-Learn based pipeline that predicts seismic alert levels (Green, Orange, Red) based on CDI, MMI, Significance, Magnitude, and Depth.
- **🌍 3D Telemetry Visualization**: An interactive, React-Three-Fiber powered 3D Earth that displays live-system telemetry and seismic data.
- **🔐 Secure Access Protocols**: Custom JWT-based authentication system with secure password hashing for authorized personnel access.
- **📊 Predictive History Archive**: Persistent storage of seismic analyses, allowing users to track and review historical prediction records.
- **🎭 Matrix Rain Immersion**: High-fidelity digital character transitions and hex-code dissolve effects for a seamless cyberpunk interface experience.

---

## 🛠 Tech Stack

### Backend (Python/FastAPI)
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) for high-performance asynchronous API endpoints.
- **Database**: [MySQL](https://www.mysql.com/) (hosted on Aiven) with SSL-secured connections.
- **Machine Learning**: [Scikit-Learn](https://scikit-learn.org/), [Pandas](https://pandas.pydata.org/), [Joblib](https://joblib.readthedocs.io/).
- **Security**: [JWT (PyJWT)](https://pyjwt.readthedocs.io/), [Passlib](https://passlib.readthedocs.io/) (bcrypt).

### Frontend (React/Vite)
- **Framework**: [React 19](https://react.dev/) + [Vite](https://vitejs.dev/) for ultra-fast development.
- **3D Graphics**: [Three.js](https://threejs.org/), [@react-three/fiber](https://github.com/pmndrs/react-three-fiber), [@react-three/drei](https://github.com/pmndrs/drei).
- **Animations**: [Framer Motion](https://www.framer.com/motion/) for smooth transitions and the Matrix Rain effect.
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) for modern, responsive layouts.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- MySQL Instance (Aiven recommended for SSL support)

### Backend Installation
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in a `.env` file:
   ```env
   DB_HOST=your_host:port
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=impactsense
   SECRET_KEY=your_secret_key
   ```
4. Start the server:
   ```bash
   python main.py
   ```

### Frontend Installation
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## 📂 Project Structure

```text
ImpactSense/
├── backend/            # FastAPI Implementation
│   ├── auth.py         # JWT & Security Logic
│   ├── database.py     # MySQL/Aiven Connectivity
│   └── main.py         # API Endpoints & ML Loading
├── frontend/           # React Fiber Application
│   ├── src/
│   │   ├── components/ # UI Elements (Navbar, ProtectedRoute)
│   │   ├── pages/      # Home, Predict, History, Login
│   │   └── App.jsx     # Routing & Transitions
└── notebooks/          # ML Training & Pipeline Export
```

---

## 📜 License
System protocols are proprietary and confidential. Optimized for terminal-level performance.
