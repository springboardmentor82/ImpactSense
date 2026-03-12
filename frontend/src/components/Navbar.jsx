import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Activity, Home, History as HistoryIcon, LogOut, LogIn, Zap } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { logout, user } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const navItems = [
    { path: '/', label: 'HOME', icon: <Home className="w-4 h-4" />, public: true },
    { path: '/predict', label: 'PREDICT', icon: <Zap className="w-4 h-4" />, public: true },
    { path: '/history', label: 'HISTORY', icon: <HistoryIcon className="w-4 h-4" />, public: false },
  ];

  const visibleItems = navItems.filter(item => item.public || user);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center space-x-3 cursor-pointer"
          onClick={() => navigate('/')}
        >
          <div className="w-10 h-10 rounded-sm bg-cyan-500/10 flex items-center justify-center border border-cyan-400/40 shadow-[0_0_15px_rgba(0,255,255,0.2)]">
            <Activity className="w-6 h-6 text-cyan-400" />
          </div>
          <span className="text-xl font-bold tracking-[4px] text-white hidden sm:block uppercase">
            IMPACT_SENSE
          </span>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center holo-panel px-2 py-1"
        >
          {visibleItems.map((item) => (
            <Link 
              key={item.path} 
              to={item.path}
              className={`relative px-5 py-2 text-[0.7rem] font-bold tracking-widest transition-all flex items-center space-x-2 ${
                location.pathname === item.path ? 'text-cyan-400' : 'text-white/60 hover:text-white'
              }`}
            >
              {location.pathname === item.path && (
                <motion.div 
                  layoutId="nav-glow"
                  className="absolute inset-0 bg-cyan-400/10 border-b-2 border-cyan-400 z-0"
                  transition={{ type: "spring", bounce: 0, duration: 0.4 }}
                />
              )}
              <span className="relative z-10">{item.icon}</span>
              <span className="relative z-10 hidden md:block">{item.label}</span>
            </Link>
          ))}
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center space-x-4"
        >
          {user ? (
            <button 
              onClick={logout}
              className="flex items-center space-x-2 px-4 py-2 bg-transparent border border-magenta-500/50 text-magenta-500 hover:bg-magenta-500/10 hover:shadow-[0_0_15px_rgba(255,0,255,0.3)] transition-all text-xs font-bold tracking-widest uppercase border-[var(--neon-magenta)] !text-[var(--neon-magenta)]"
              style={{ borderColor: 'var(--neon-magenta)' }}
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:block">LOGOUT</span>
            </button>
          ) : (
            <button 
              onClick={() => navigate('/login')}
              className="flex items-center space-x-2 px-4 py-2 bg-transparent border border-cyan-500/50 text-cyan-500 hover:bg-cyan-500/10 hover:shadow-[0_0_15px_rgba(0,255,255,0.3)] transition-all text-xs font-bold tracking-widest uppercase"
            >
              <LogIn className="w-4 h-4" />
              <span className="hidden sm:block">LOGIN</span>
            </button>
          )}
        </motion.div>
      </div>
    </nav>
  );
};

export default Navbar;
