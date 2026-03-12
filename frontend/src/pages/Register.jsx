import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus, Activity } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(email, password);
      navigate('/login');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="flex flex-col items-center justify-center min-h-screen px-4"
    >
      <div className="w-full max-w-md p-10 holo-panel relative overflow-hidden">
        
        <div className="flex flex-col items-center mb-10 relative z-10">
          <motion.div 
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200, damping: 20, delay: 0.2 }}
            className="w-16 h-16 rounded-sm bg-magenta-500/10 flex items-center justify-center mb-6 border border-magenta-500/30 shadow-[0_0_20px_rgba(255,0,255,0.2)]"
          >
            <Activity className="w-10 h-10 text-magenta-500" />
          </motion.div>
          <h1 className="text-2xl font-black text-white tracking-[6px] uppercase">
            CREATE_ACCESS
          </h1>
          <p className="text-[0.65rem] text-magenta-500/60 mt-3 text-center font-mono tracking-widest uppercase font-bold">
            {'>'} INITIALIZING NEW_IDENTITY_PROTOCOL...
          </p>
        </div>

        {error && (
            <div className="bg-red-500/10 border border-red-500/50 text-red-500 text-[0.7rem] p-3 rounded-sm mb-6 text-center font-mono uppercase">
              {error}
            </div>
        )}

        <form onSubmit={handleRegister} className="space-y-6 relative z-10">
          <div className="space-y-2">
            <label className="text-[0.6rem] font-bold text-cyan-400/70 ml-1 tracking-[2px] uppercase font-mono">NEW_USER_ID (EMAIL)</label>
            <div className="relative">
              <input 
                type="email" 
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 bg-black/40 border border-cyan-400/20 rounded-sm focus:outline-none focus:border-cyan-400/50 text-white placeholder-cyan-900/30 transition-all font-mono text-xs uppercase"
                placeholder="NEW_IDENTITY@NETWORK.GOV"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-[0.6rem] font-bold text-cyan-400/70 ml-1 tracking-[2px] uppercase font-mono">ACCESS_PHRASE (PASSWORD)</label>
            <div className="relative">
              <input 
                type="password" 
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-black/40 border border-cyan-400/20 rounded-sm focus:outline-none focus:border-cyan-400/50 text-white placeholder-cyan-900/30 transition-all font-mono text-xs"
                placeholder="••••••••"
              />
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            type="submit"
            disabled={loading}
            className="cyber-btn magenta w-full !py-4 font-black !text-sm flex items-center justify-center space-x-3 transition-all disabled:opacity-50 tracking-[3px]"
          >
            <span>{loading ? 'REGISTERING...' : 'REGISTER_ACCOUNT'}</span>
            <UserPlus className="w-5 h-5 ml-2" />
          </motion.button>
        </form>
        
        <div className="mt-8 text-center text-[0.6rem] text-white/30 relative z-10 font-mono tracking-widest uppercase">
          <p>IDENTITY_FOUND? <Link to="/login" className="text-magenta-500 hover:text-magenta-400 font-bold decoration-magenta-500/30 underline underline-offset-4 decoration-2">RESTORE_LINK</Link></p>
        </div>
      </div>
    </motion.div>
  );
};

export default Register;
