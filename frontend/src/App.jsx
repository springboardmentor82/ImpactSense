import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import Predict from './pages/Predict';
import History from './pages/History';
import SampleDataset from './pages/SampleDataset';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import { useState, useEffect } from 'react';
import skyline from './assets/cyberpunk_city_skyline.png';

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        transition={{ duration: 0.3 }}
      >
        <Routes location={location}>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/samples" element={<SampleDataset />} />
          <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />
        </Routes>
      </motion.div>
    </AnimatePresence>
  );
}

const TransitionOverlay = () => {
  const location = useLocation();
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    setIsTransitioning(true);
    const timer = setTimeout(() => setIsTransitioning(false), 800);
    return () => clearTimeout(timer);
  }, [location.pathname]);

  if (!isTransitioning) return null;

  return (
    <div className="gear-sync-overlay">
      <div className="gear-container">
        {/* Outer Gear */}
        <div className="gear-outer">
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M50 10L55 25H45L50 10ZM50 90L45 75H55L50 90ZM10 50L25 45V55L10 50ZM90 50L75 55V45L90 50ZM21.7 21.7L32.3 32.3L25.2 39.4L14.6 28.8L21.7 21.7ZM78.3 78.3L67.7 67.7L74.8 60.6L85.4 71.2L78.3 78.3ZM21.7 78.3L14.6 71.2L25.2 60.6L32.3 67.7L21.7 78.3ZM78.3 21.7L85.4 28.8L74.8 39.4L67.7 32.3L78.3 21.7Z" />
            <circle cx="50" cy="50" r="20" />
            {[...Array(8)].map((_, i) => (
              <rect key={i} x="47" y="5" width="6" height="15" rx="1" transform={`rotate(${i * 45} 50 50)`} fill="currentColor" />
            ))}
          </svg>
        </div>
        
        {/* Inner Gear */}
        <div className="gear-inner">
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="3">
            <circle cx="50" cy="50" r="30" strokeDasharray="10 5" />
            {[...Array(6)].map((_, i) => (
              <rect key={i} x="46" y="15" width="8" height="12" rx="1" transform={`rotate(${i * 60} 50 50)`} fill="currentColor" />
            ))}
          </svg>
        </div>
        
        <div className="gear-core"></div>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col items-center gap-4"
      >
        <div className="sync-status text-xs">
          SYNCING_NODE_PROTOCOLS...
        </div>
        <div className="flex gap-1">
          {[...Array(3)].map((_, i) => (
            <motion.div
              key={i}
              className="w-2 h-2 bg-cyan-400"
              animate={{ opacity: [0, 1, 0] }}
              transition={{ duration: 1, delay: i * 0.2, repeat: Infinity }}
            />
          ))}
        </div>
      </motion.div>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-[#0a0a0b] text-white selection:bg-cyan-500/30 overflow-x-hidden">
          {/* Global Cyberpunk Background */}
          <div className="cyberpunk-bg" style={{ backgroundImage: `url(${skyline})` }}></div>
          <div className="scanlines"></div>
          <div className="rain"></div>

          {/* New Immersive Elements */}
          <div className="perspective-container">
            <div className="grid-3d"></div>
          </div>
          
          <div className="particles">
            {[...Array(20)].map((_, i) => (
              <div 
                key={i} 
                className="particle"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                  width: `${Math.random() * 3 + 1}px`,
                  height: `${Math.random() * 3 + 1}px`,
                  animationDuration: `${Math.random() * 10 + 10}s`,
                  animationDelay: `${Math.random() * 20}s`
                }}
              />
            ))}
          </div>
          
          <TransitionOverlay />
          
          <main className="relative z-10">
            <Navbar />
            <div className="pt-20">
              <AnimatedRoutes />
            </div>
          </main>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
