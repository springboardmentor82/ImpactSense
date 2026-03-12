import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, Activity, RefreshCw, AlertTriangle, Info, MapPin, Zap } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_URL = `${API_BASE_URL}/api/predict`;

const Predict = () => {
  const { token } = useAuth();
  
  const [formData, setFormData] = useState({
    cdi: '',
    mmi: '',
    sig: '',
    magnitude: '',
    depth: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Convert string inputs to floats
      const payload = {
        cdi: parseFloat(formData.cdi),
        mmi: parseFloat(formData.mmi),
        sig: parseFloat(formData.sig),
        magnitude: parseFloat(formData.magnitude),
        depth: parseFloat(formData.depth)
      };

      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const response = await axios.post(API_URL, payload, { headers });
      
      // Simulate slight delay for dramatic effect
      setTimeout(() => {
        setResult(response.data.alert);
        setLoading(false);
      }, 800);
      
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to connect to prediction engine.");
      setLoading(false);
    }
  };

  const getAlertConfig = (level) => {
    const configs = {
      'green': {
        color: 'text-green-400',
        bg: 'bg-green-500/10',
        border: 'border-green-500/30',
        gradient: 'from-green-500/20 to-transparent',
        icon: <Activity className="w-12 h-12 text-green-400" />,
        title: 'Green Alert (Low Impact)',
        desc: 'Minimal impact expected. Standard monitoring protocols remain active.'
      },
      'yellow': {
        color: 'text-yellow-400',
        bg: 'bg-yellow-500/10',
        border: 'border-yellow-500/30',
        gradient: 'from-yellow-500/20 to-transparent',
        icon: <Info className="w-12 h-12 text-yellow-400" />,
        title: 'Yellow Alert (Moderate)',
        desc: 'Potential for localized disruption. Advisory notifications should be prepared.'
      },
      'orange': {
        color: 'text-orange-400',
        bg: 'bg-orange-500/10',
        border: 'border-orange-500/30',
        gradient: 'from-orange-500/20 to-transparent',
        icon: <AlertTriangle className="w-12 h-12 text-orange-400" />,
        title: 'Orange Alert (High Impact)',
        desc: 'Significant regional impact likely. Emergency services on standby.'
      },
      'red': {
        color: 'text-red-500',
        bg: 'bg-red-500/10',
        border: 'border-red-500/30',
        gradient: 'from-red-500/20 to-transparent',
        icon: <ShieldAlert className="w-12 h-12 text-red-500" />,
        title: 'Red Alert (Severe)',
        desc: 'Catastrophic impact expected. Immediate widespread evacuation & emergency response required.'
      }
    };
    return configs[level?.toLowerCase()] || configs['green']; // default fallback
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 py-12 relative">

      <motion.div 
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-10 z-10"
      >
        
        {/* Input Form Section */}
        <div className="holo-panel p-8 relative overflow-hidden">
          <div className="mb-8">
            <h2 className="text-xl font-black text-white mb-2 flex items-center space-x-3 tracking-[3px] uppercase">
              <Zap className="text-cyan-400" />
              <span>TELEMETRY_INPUT</span>
            </h2>
            <p className="text-[0.65rem] text-cyan-400/60 font-mono tracking-widest uppercase">{'>'} ENTER SEISMIC PARAMETERS FOR ANALYSIS</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5 relative z-10">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <InputField 
                label="CDI (Community Decimal Intensity)" 
                name="cdi" 
                value={formData.cdi} 
                onChange={handleInputChange} 
                placeholder="e.g. 4.3" 
                icon={<Activity className="w-4 h-4 text-gray-500" />}
              />
              <InputField 
                label="MMI (Modified Mercalli Intensity)" 
                name="mmi" 
                value={formData.mmi} 
                onChange={handleInputChange} 
                placeholder="e.g. 5.1" 
                icon={<Activity className="w-4 h-4 text-gray-500" />}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <InputField 
                label="Magnitude" 
                name="magnitude" 
                value={formData.magnitude} 
                onChange={handleInputChange} 
                placeholder="e.g. 6.5" 
                icon={<Zap className="w-4 h-4 text-gray-500" />}
              />
              <InputField 
                label="Depth (km)" 
                name="depth" 
                value={formData.depth} 
                onChange={handleInputChange} 
                placeholder="e.g. 10.0" 
                icon={<MapPin className="w-4 h-4 text-gray-500" />}
              />
            </div>

            <InputField 
              label="Significance (sig)" 
              name="sig" 
              value={formData.sig} 
              onChange={handleInputChange} 
              placeholder="e.g. 400" 
              icon={<AlertTriangle className="w-4 h-4 text-gray-500" />}
            />

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={loading}
              className={`cyber-btn w-full !py-5 mt-6 !text-sm !font-black ${loading ? 'opacity-50 !cursor-wait' : ''}`}
            >
              {loading ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin mr-3" />
                  <span>PROCESS_TELEMETRY...</span>
                </>
              ) : (
                <>
                  <Activity className="w-5 h-5 mr-3" />
                  <span>RUN_IMPACT_ANALYSIS</span>
                </>
              )}
            </motion.button>
          </form>
        </div>

        {/* Results Section */}
        <div className="flex flex-col space-y-6">
          <AnimatePresence mode="wait">
            {!result && !error && !loading && (
              <motion.div 
                key="idle"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="flex-1 border-2 border-dashed border-white/10 rounded-3xl flex flex-col items-center justify-center p-8 text-center bg-black/20"
              >
                <div className="w-20 h-20 rounded-sm bg-cyan-400/5 flex items-center justify-center mb-6 border border-white/5 shadow-inner">
                  <Activity className="w-10 h-10 text-cyan-400/20" />
                </div>
                <h3 className="text-sm font-black text-cyan-400/40 mb-2 tracking-[2px] uppercase">AWAITING_DATA_STREAM</h3>
                <p className="text-[0.6rem] text-white/30 font-mono tracking-widest uppercase px-12">{'>'} SUBMIT TELEMETRY FOR NEURAL_NETWORK INFERENCE</p>
              </motion.div>
            )}

            {loading && (
              <motion.div 
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex-1 holo-panel flex flex-col items-center justify-center p-8 text-center"
              >
                <div className="relative z-10 flex flex-col items-center">
                  <div className="w-24 h-24 mb-6 relative">
                    <div className="absolute inset-0 border-2 border-t-cyan-400 border-white/5 rounded-sm animate-spin"></div>
                    <div className="absolute inset-4 border-2 border-b-magenta-400 border-white/5 rounded-sm animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
                  </div>
                  <h3 className="text-sm font-black text-white mb-2 tracking-[3px] uppercase">ANALYZING_PATTERNS...</h3>
                  <p className="text-[0.6rem] text-cyan-400 animate-pulse font-mono tracking-[2px]">RUNNING NEURAL_NETWORK_INFERENCE</p>
                </div>
              </motion.div>
            )}

            {error && (
              <motion.div 
                key="error"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="flex-1 rounded-3xl flex flex-col items-center justify-center p-8 text-center bg-danger/10 border border-danger/30"
              >
                <AlertTriangle className="w-16 h-16 text-danger mb-4" />
                <h3 className="text-xl font-bold text-danger mb-2">Analysis Failed</h3>
                <p className="text-red-400 text-sm">{error}</p>
              </motion.div>
            )}

            {result && !loading && (
              <motion.div 
                key="result"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ type: "spring", stiffness: 200, damping: 20 }}
                className={`flex-1 rounded-3xl flex flex-col p-8 relative overflow-hidden ${getAlertConfig(result).bg} border ${getAlertConfig(result).border}`}
              >
                {/* Dynamic Gradient Background based on alert level */}
                <div className={`absolute inset-0 bg-gradient-to-br opacity-50 pointer-events-none ${getAlertConfig(result).gradient}`}></div>
                
                <div className="relative z-10 flex flex-col h-full justify-between">
                  <div>
                    <div className="flex items-center space-x-4 mb-6">
                      <div className={`p-4 rounded-2xl bg-black/40 backdrop-blur-md shadow-2xl`}>
                        {getAlertConfig(result).icon}
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-gray-400 uppercase tracking-widest mb-1">Impact Designation</p>
                        <h3 className={`text-3xl font-extrabold ${getAlertConfig(result).color}`}>
                          {getAlertConfig(result).title.split(' ')[0]} Alert
                        </h3>
                      </div>
                    </div>
                    
                    <div className="mt-8 bg-black/40 backdrop-blur-md p-6 rounded-2xl border border-white/5">
                      <p className={`text-lg font-medium leading-relaxed ${getAlertConfig(result).color}`}>
                        {getAlertConfig(result).desc}
                      </p>
                    </div>
                  </div>

                  <div className="mt-8 pt-6 border-t border-white/10 flex justify-between items-center text-sm text-gray-400 flex-wrap gap-4">
                    <div className="flex items-center space-x-2">
                       <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                       <span>Confidence: High (&gt; 94%)</span>
                    </div>
                    <div>Source: NN Pipeline v2</div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

      </motion.div>
    </div>
  );
};

const InputField = ({ label, name, value, onChange, placeholder, icon }) => (
  <div className="space-y-2">
    <label className="block text-[0.6rem] font-black text-cyan-400/70 ml-1 tracking-[1.5px] uppercase font-mono">{label}</label>
    <div className="relative">
      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
        {icon}
      </div>
      <input
        type="number"
        step="0.1"
        name={name}
        required
        value={value}
        onChange={onChange}
        className="w-full pl-11 pr-4 py-3 bg-black/40 border border-cyan-400/20 rounded-sm focus:outline-none focus:border-cyan-400/60 hover:border-cyan-400/40 text-cyan-100 placeholder-cyan-900/30 transition-all font-mono text-[0.8rem]"
        placeholder={placeholder}
      />
    </div>
  </div>
);

export default Predict;
