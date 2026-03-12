import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { History as HistoryIcon, Calendar, Activity, Zap, MapPin, AlertTriangle, ShieldAlert, Trash2 } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const History = () => {
  const { token } = useAuth();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        const response = await axios.get(`${API_BASE_URL}/api/history`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setHistory(response.data);
      } catch (err) {
        setError("Failed to load history.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [token]);

  const getAlertStyle = (level) => {
    const styles = {
      'green': { color: 'text-green-400', border: 'border-green-500/30', glow: 'shadow-[0_0_10px_rgba(74,222,128,0.2)]', icon: <Activity className="w-5 h-5" /> },
      'yellow': { color: 'text-yellow-400', border: 'border-yellow-500/30', glow: 'shadow-[0_0_10px_rgba(250,204,21,0.2)]', icon: <Activity className="w-5 h-5" /> },
      'orange': { color: 'text-orange-400', border: 'border-orange-500/30', glow: 'shadow-[0_0_10px_rgba(251,146,60,0.2)]', icon: <AlertTriangle className="w-5 h-5" /> },
      'red': { color: 'text-red-500', border: 'border-red-500/40', glow: 'shadow-[0_0_15px_rgba(239,68,68,0.3)]', icon: <ShieldAlert className="w-5 h-5" /> },
    };
    return styles[level?.toLowerCase()] || styles['green'];
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-6 flex flex-col items-center">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-5xl w-full"
      >
        <div className="flex items-center justify-between mb-10">
          <div>
            <h1 className="text-2xl font-black text-white flex items-center space-x-4 tracking-[4px] uppercase">
              <HistoryIcon className="text-cyan-400 w-8 h-8" />
              <span>HOLOGRAPHIC_ARCHIVES</span>
            </h1>
            <p className="text-[0.7rem] text-cyan-400/60 mt-2 font-mono tracking-widest uppercase font-bold">{'>'} ARCHIVE_STATUS: SYNCHRONIZED</p>
          </div>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin mb-4"></div>
            <p className="text-gray-400">Loading your history...</p>
          </div>
        ) : error ? (
          <div className="bg-red-500/10 border border-red-500/20 p-6 rounded-2xl text-center">
            <p className="text-red-400">{error}</p>
          </div>
        ) : history.length === 0 ? (
          <div className="bg-surface/40 backdrop-blur-md border border-white/5 rounded-3xl p-12 text-center flex flex-col items-center">
            <div className="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-6">
              <HistoryIcon className="w-8 h-8 text-gray-500" />
            </div>
            <h3 className="text-xl font-semibold text-gray-300 mb-2">No data recorded yet</h3>
            <p className="text-gray-500 max-w-sm">When you run a seismic prediction analysis, it will appear here for your records.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {history.map((record) => {
              const style = getAlertStyle(record.alert_level);
              return (
                <motion.div 
                  key={record.id}
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  whileHover={{ y: -3, borderColor: 'var(--neon-cyan)' }}
                  className={`p-6 holo-panel ${style.glow} border ${style.border} transition-all group`}
                >
                  <div className="flex justify-between items-start mb-6">
                    <div className={`p-2 rounded-sm bg-black/40 border border-white/10 ${style.color}`}>
                      {style.icon}
                    </div>
                    <div className="text-[0.6rem] font-black uppercase tracking-widest text-white/40 flex items-center bg-transparent border border-white/5 px-2 py-1 rounded-sm font-mono">
                      <Calendar className="w-3 h-3 mr-2" />
                      {formatDate(record.timestamp)}
                    </div>
                  </div>

                  <h3 className={`text-sm font-black mb-5 tracking-[2px] uppercase ${style.color}`}>
                    {record.alert_level}_ALERT
                  </h3>

                  <div className="space-y-4 font-mono">
                    <div className="flex justify-between items-center text-[0.7rem] uppercase tracking-wider">
                      <span className="text-white/40 flex items-center">
                        {'>'} MAGNITUDE
                      </span>
                      <span className="text-white font-black">{record.magnitude} M</span>
                    </div>
                    <div className="flex justify-between items-center text-[0.7rem] uppercase tracking-wider">
                      <span className="text-white/40 flex items-center">
                        {'>'} DEPTH
                      </span>
                      <span className="text-white font-black">{record.depth} KM</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 mt-5 pt-5 border-t border-white/10 overflow-hidden">
                      <div className="text-center">
                        <p className="text-[0.55rem] text-white/30 uppercase font-black tracking-tighter">CDI</p>
                        <p className="text-[0.7rem] font-black text-cyan-400">{record.cdi}</p>
                      </div>
                      <div className="text-center border-x border-white/10">
                        <p className="text-[0.55rem] text-white/30 uppercase font-black tracking-tighter">MMI</p>
                        <p className="text-[0.7rem] font-black text-cyan-400">{record.mmi}</p>
                      </div>
                      <div className="text-center">
                        <p className="text-[0.55rem] text-white/30 uppercase font-black tracking-tighter">SIG</p>
                        <p className="text-[0.7rem] font-black text-cyan-400">{record.sig}</p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default History;
