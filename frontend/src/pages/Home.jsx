import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { ChevronRight, Activity, ShieldAlert, Zap } from 'lucide-react';
import CyberEarth from '../components/CyberEarth';

const Home = () => {
  const navigate = useNavigate();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { staggerChildren: 0.2, delayChildren: 0.1 }
    }
  };

  const glitchVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1, 
      transition: { 
        duration: 0.2, 
        repeat: 3, 
        repeatType: "reverse"
      } 
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
  };

  return (
    <div className="flex flex-col items-center px-4 pb-20 relative overflow-hidden">
      {/* Hero Section */}
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative w-full min-h-[calc(100vh-80px)] flex flex-col items-center text-center z-10 pt-20"
      >
        <motion.div variants={itemVariants} className="mb-6 inline-flex items-center space-x-2 px-4 py-1.5 holo-panel">
          <span className="w-2.5 h-2.5 rounded-sm bg-cyan-400 animate-pulse shadow-[0_0_8px_var(--neon-cyan)]"></span>
          <span className="text-[0.65rem] font-bold tracking-[2px] text-cyan-400">NEURAL_ORCHESTRATION_ACTIVE</span>
        </motion.div>

        <motion.h1 
          variants={itemVariants} 
          className="text-4xl md:text-6xl font-black tracking-[8px] mb-8 text-white uppercase relative"
        >
          <motion.span 
            variants={glitchVariants} 
            initial="hidden" 
            animate="visible" 
            className="absolute inset-0 text-cyan-400/30 -z-10 translate-x-1"
          >
            EARTHQUAKE_IMPACT <br className="hidden md:block"/>
            NEURAL_ANALYSIS
          </motion.span>
          EARTHQUAKE_IMPACT <br className="hidden md:block"/>
          <span className="text-cyan-400 drop-shadow-[0_0_15px_var(--glow-cyan)]">NEURAL_ANALYSIS</span>
        </motion.h1>

        <motion.p 
          variants={itemVariants}
          className="text-[0.8rem] text-white/70 max-w-2xl mb-12 leading-relaxed tracking-widest uppercase font-mono"
        >
          {'>'} Orchestrating deep-layer neural mesh for seismic anomaly detection. The system anticipates earth-shattering vectors before they manifest in reality.
        </motion.p>

        <motion.div variants={itemVariants} className="mb-20">
          <button 
            onClick={() => navigate('/predict')}
            className="cyber-btn !px-12 !py-5 !text-lg !font-black"
          >
            INITIALIZE PREDICTION_CORE
          </button>
        </motion.div>

        <SystemInterlude label="HANDSHAKE_COMPLETE" status="SECURE" delay={1.2} />

        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2, duration: 1 }}
          className="absolute bottom-10 flex flex-col items-center gap-2 cursor-pointer group"
          onClick={() => window.scrollTo({ top: window.innerHeight - 80, behavior: 'smooth' })}
        >
          <span className="text-[0.6rem] font-black tracking-[4px] text-cyan-400 uppercase opacity-40 group-hover:opacity-100 transition-opacity">Scroll to Explore</span>
          <motion.div 
            animate={{ y: [0, 8, 0] }}
            transition={{ repeat: Infinity, duration: 2 }}
            className="w-1 h-6 bg-gradient-to-b from-cyan-400/50 to-transparent rounded-full"
          />
        </motion.div>
      </motion.div>

      {/* Details Section */}
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        className="max-w-4xl w-full flex flex-col items-center z-10"
      >
        <div 
          className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full text-left mt-20"
        >
          <div className="md:col-span-3 mb-6">
            <span className="text-[0.65rem] font-black text-cyan-400 tracking-[4px] uppercase">VECTOR_EXTRACTION_MODULES</span>
          </div>
          <FeatureCard 
            icon={<Activity className="text-secondary w-6 h-6" />}
            title="Seismic Vectoring"
            desc="Deconstructing CDI and MMI telemetry into actionable neural signatures."
            delay={0.4}
          />
          <FeatureCard 
            icon={<Zap className="text-accent w-6 h-6" />}
            title="Neural Inference"
            desc="Low-latency categorization of subterranean disruption events."
            delay={0.6}
          />
          <FeatureCard 
            icon={<ShieldAlert className="text-danger w-6 h-6" />}
            title="Alert Synthesis"
            desc="Direct distillation of threat levels for rapid defensive maneuvers."
            delay={0.8}
          />
        </div>

        <SystemInterlude label="PLANETARY_GRID" status="SYNCED" delay={2} />

        <motion.div 
          variants={itemVariants}
          className="mt-32 w-full text-left"
        >
          <div className="flex items-center gap-4 mb-6">
            <span className="text-[0.65rem] font-black text-cyan-400 tracking-[4px] uppercase">PLANETARY_INTERCEPT_STREAM</span>
          </div>
          
          <CyberEarth />
          
          <SystemInterlude label="DATABASE_DECRYPTION" status="READY" delay={3} />

          <div className="flex items-center gap-4 mt-32 mb-12">
            <div className="h-[1px] flex-1 bg-gradient-to-r from-transparent via-cyan-400/50 to-transparent"></div>
            <h2 className="text-xl font-black tracking-[4px] text-cyan-400 uppercase">KNOWLEDGE_DECRYPTION_LOGS</h2>
            <div className="h-[1px] flex-1 bg-gradient-to-r from-transparent via-cyan-400/50 to-transparent"></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <DefinitionItem 
              term="CDI" 
              label="Community Weighted Intensity"
              def="A measure of the reported intensity of shaking as perceived by people in the affected area. It aggregates human feedback to gauge real-world impact."
            />
            <DefinitionItem 
              term="MMI" 
              label="Modified Mercalli Intensity"
              def="A scale used for measuring the intensity of shaking produced by an earthquake. Unlike magnitude, intensity varies based on location and surface geology."
            />
            <DefinitionItem 
              term="MAGNITUDE" 
              label="Seismic Energy Release"
              def="A logarithmic measure of the energy released by an earthquake at its source. Each whole number increase represents a 10x increase in amplitude."
            />
            <DefinitionItem 
              term="DEPTH" 
              label="Hypocenter Verticality"
              def="The distance from the earth's surface to the point where the earthquake originated. Shallower quakes often cause more surface damage."
            />
            <DefinitionItem 
              term="SIGNIFICANCE" 
              label="Event Impact Score"
              def="A composite value (0-1000) representing the overall impact of an earthquake, calculated based on magnitude, intensity, and reported effects."
            />
          </div>
        </motion.div>
      </motion.div>
    </div>
  );

};

const DefinitionItem = ({ term, label, def }) => (
  <div className="p-6 border-l-2 border-cyan-400/30 bg-cyan-400/5 hover:bg-cyan-400/10 transition-colors group">
    <div className="flex items-baseline gap-3 mb-2">
      <h3 className="text-lg font-black text-white tracking-widest group-hover:text-cyan-400 transition-colors">{term}</h3>
      <span className="text-[0.6rem] text-cyan-400/60 font-mono uppercase tracking-tighter">{label}</span>
    </div>
    <p className="text-white/60 text-xs leading-relaxed font-mono tracking-wider uppercase">
      {def}
    </p>
  </div>
);

const SystemInterlude = ({ label, status, delay }) => (
  <motion.div 
    initial={{ opacity: 0 }}
    whileInView={{ opacity: 1 }}
    transition={{ duration: 0.5, delay }}
    className="w-full flex items-center justify-start gap-4 my-8 font-mono"
  >
    <span className="text-[0.6rem] text-white/20">[{new Date().toLocaleTimeString()}]</span>
    <span className="text-[0.6rem] text-cyan-400 font-bold uppercase tracking-widest">{label}</span>
    <div className="h-[1px] flex-1 bg-cyan-400/10"></div>
    <span className="text-[0.6rem] text-cyan-400/60 uppercase tracking-tighter cursor-default hover:text-cyan-400 transition-colors">
        STATUS: <span className="text-cyan-400">{status}</span>
    </span>
  </motion.div>
);

const FeatureCard = ({ icon, title, desc, delay }) => (
  <motion.div 
    variants={{
      hidden: { opacity: 0, scale: 0.95 },
      visible: { opacity: 1, scale: 1, transition: { duration: 0.5, delay } }
    }}
    className="p-6 holo-panel group hover:border-cyan-400/60 transition-all cursor-default"
  >
    <div className="w-12 h-12 rounded-sm bg-cyan-400/10 flex items-center justify-center mb-6 border border-cyan-400/20 group-hover:shadow-[0_0_15px_rgba(0,255,255,0.2)]">
      {icon}
    </div>
    <h3 className="text-xs font-black text-cyan-400 mb-3 tracking-[3px] uppercase">{title}</h3>
    <p className="text-white/50 text-[0.65rem] leading-relaxed tracking-[1.5px] uppercase font-mono">{desc}</p>
  </motion.div>
);

export default Home;
