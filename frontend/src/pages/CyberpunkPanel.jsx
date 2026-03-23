import React, { useState, useEffect } from 'react';
import './CyberpunkPanel.css';

const CyberpunkPanel = () => {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="cyberpunk-container">
      <div className="scanning-line"></div>
      
      {/* Background Image */}
      <div 
        className="cyberpunk-bg" 
        style={{ backgroundImage: `url('/src/assets/cyberpunk_city_skyline.png')` }} 
      />
      
      <div className="scanlines"></div>
      <div className="rain"></div>

      <div className="control-grid">
        {/* Header Widget */}
        <div className="holo-panel" style={{ gridColumn: '1 / 6', gridRow: '1 / 2', padding: '15px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--neon-cyan)', letterSpacing: '2px' }}>[ SYSTEM STATUS: OPTIMAL ]</span>
            <span style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#fff' }}>{time}</span>
          </div>
        </div>

        {/* System Monitoring */}
        <div className="holo-panel magenta" style={{ gridColumn: '1 / 4', gridRow: '3 / 8', padding: '20px' }}>
          <h3 style={{ borderBottom: '1px solid var(--neon-magenta)', marginBottom: '15px', color: 'var(--neon-magenta)', fontSize: '0.9rem' }}>// NETWORK_LOAD</h3>
          <div className="system-monitor-placeholder">
            <div style={{ height: '150px', display: 'flex', alignItems: 'flex-end', gap: '5px' }}>
              {[40, 60, 45, 80, 55, 90, 70, 50, 85].map((h, i) => (
                <div key={i} style={{ 
                  flex: 1, 
                  height: `${h}%`, 
                  background: 'var(--neon-magenta)', 
                  boxShadow: '0 0 10px var(--neon-magenta)',
                  opacity: 0.5 + (h/200)
                }}></div>
              ))}
            </div>
            <p style={{ marginTop: '15px', fontSize: '0.65rem', color: 'var(--neon-magenta)', letterSpacing: '1px' }}>{'>'} TRACING ENCRYPTED PACKETS...</p>
          </div>
        </div>

        {/* Terminal Widget */}
        <div className="holo-panel" style={{ gridColumn: '4 / 10', gridRow: '3 / 11', padding: '0', overflow: 'hidden' }}>
          <div style={{ background: 'rgba(0,255,255,0.1)', padding: '5px 15px', fontSize: '0.7rem', borderBottom: '1px solid var(--neon-cyan)', color: 'var(--neon-cyan)' }}>
            ROOT@CMD_TERM: ~/IMPACT_SENSE/SENSORS
          </div>
          <div style={{ padding: '20px', fontFamily: 'JetBrains Mono, monospace', fontSize: '0.85rem', color: 'var(--neon-cyan)', lineHeight: '1.6' }}>
            <p style={{ color: 'var(--neon-magenta)' }}>[CRITICAL] UNAUTHORIZED ACCESS ATTEMPT DETECTED...</p>
            <p>{'>'} INITIALIZING COUNTERMEASURES...</p>
            <p>{'>'} LOADING HEURISTIC MODELS [OK]</p>
            <p>{'>'} DECRYPTING BASEBAND SIGNAL...</p>
            <p>{'>'} ACCESS LEVEL: OMEGA</p>
            <p style={{ marginTop: '10px' }}>{'>'} CONNECTION ESTABLISHED VIA NODE_772</p>
            <div style={{ marginTop: '20px' }}>
              <span style={{ color: '#fff' }}>USER@SENSE:</span> <span className="pulse" style={{ color: 'var(--neon-cyan)' }}>█</span>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="holo-panel" style={{ gridColumn: '10 / 13', gridRow: '3 / 6', padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '15px' }}>
          <button className="cyber-btn">
            [ SCAN SECTOR ]
          </button>
          <button className="cyber-btn magenta">
            [ OVERRIDE ]
          </button>
        </div>

        {/* Radial Menu Replacement */}
        <div className="holo-panel" style={{ gridColumn: '10 / 13', gridRow: '7 / 11', padding: '20px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '20px' }}>
          <div className="pulse" style={{ width: '100px', height: '100px', border: '2px solid var(--neon-cyan)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 20px var(--neon-cyan)', background: 'rgba(0,255,255,0.05)' }}>
             <span style={{ fontSize: '0.7rem', fontWeight: 'bold' }}>CORE_7</span>
          </div>
          <div style={{ textAlign: 'center' }}>
            <p style={{ fontSize: '0.6rem', color: 'var(--neon-cyan)' }}>SYNC: 99.4%</p>
            <p style={{ fontSize: '0.6rem', color: 'var(--neon-magenta)' }}>STABILITY: 100%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CyberpunkPanel;
