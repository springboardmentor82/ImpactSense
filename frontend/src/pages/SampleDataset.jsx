import { motion } from 'framer-motion';
import { Database, Activity, AlertTriangle, ShieldAlert, Zap, Info, ChevronRight } from 'lucide-react';
import { useState } from 'react';

const SampleDataset = () => {
  const [activeFilter, setActiveFilter] = useState('ALL');

  const SAMPLES_DATA = {
    "green": [
      { "magnitude": 1.02, "depth": 103.62, "cdi": 0.7, "mmi": 3.12, "sig": 48.3, "alert": "green", "status": "STABLE", "desc": "Micro-seismic activity. No structural impact." },
      { "magnitude": 2.33, "depth": 137.03, "cdi": 0.15, "mmi": 1.37, "sig": 73.67, "alert": "green", "status": "STABLE", "desc": "Deep lithospheric shift. Undetectable by surface populations." },
      { "magnitude": 3.73, "depth": 150.57, "cdi": 1.4, "mmi": 3.76, "sig": 97.23, "alert": "green", "status": "STABLE", "desc": "Light tech-plate adjustment. Background noise only." },
      { "magnitude": 6.5, "depth": 595.0, "cdi": 3.0, "mmi": 3.0, "sig": -115.0, "alert": "green", "status": "STABLE", "desc": "High magnitude, ultra-deep event. Surface energy dissipation complete." },
      { "magnitude": 6.9, "depth": 43.0, "cdi": 7.0, "mmi": 6.0, "sig": -105.0, "alert": "green", "status": "STABLE", "desc": "Significant oceanic tremor. Non-coastal impact minimal." }
    ],
    "yellow": [
      { "magnitude": 5.0, "depth": 13.83, "cdi": 3.63, "mmi": 5.99, "sig": 339.57, "alert": "yellow", "status": "ADVISORY", "desc": "Shallow moderate surge. Localized minor tremors reported." },
      { "magnitude": 5.62, "depth": 28.5, "cdi": 3.83, "mmi": 5.45, "sig": 126.23, "alert": "yellow", "status": "ADVISORY", "desc": "Mid-depth adjustment. Advisory protocols initiated for sensitive zones." },
      { "magnitude": 6.23, "depth": 152.9, "cdi": 5.25, "mmi": 5.42, "sig": 225.68, "alert": "yellow", "status": "ADVISORY", "desc": "Deep critical mass shift. Monitoring stations on notice." },
      { "magnitude": 6.9, "depth": 19.0, "cdi": 9.0, "mmi": 7.0, "sig": 111.0, "alert": "yellow", "status": "ADVISORY", "desc": "High-intensity shallow tremor. Alert levels elevated to advisory." },
      { "magnitude": 6.99, "depth": 123.0, "cdi": 6.0, "mmi": 6.0, "sig": 51.0, "alert": "yellow", "status": "ADVISORY", "desc": "Major lithospheric snap. Sustained low-frequency waves." }
    ],
    "orange": [
      { "magnitude": 6.5, "depth": 11.0, "cdi": 7.0, "mmi": 7.0, "sig": -6.0, "alert": "orange", "status": "CRITICAL", "desc": "Strong shallow event. Significant localized structural damage likely." },
      { "magnitude": 6.78, "depth": 58.0, "cdi": 8.0, "mmi": 7.0, "sig": 60.0, "alert": "orange", "status": "CRITICAL", "desc": "Regional critical vector. Emergency services placed on standby." },
      { "magnitude": 6.96, "depth": 40.0, "cdi": 8.0, "mmi": 8.0, "sig": 69.0, "alert": "orange", "status": "CRITICAL", "desc": "Major tectonic discharge. Widespread power-grid instability." },
      { "magnitude": 7.26, "depth": 13.0, "cdi": 8.0, "mmi": 8.0, "sig": 2.0, "alert": "orange", "status": "CRITICAL", "desc": "High magnitude shallow strike. Urban centers at immediate risk." },
      { "magnitude": 7.95, "depth": 19.0, "cdi": 8.0, "mmi": 8.0, "sig": -76.0, "alert": "orange", "status": "CRITICAL", "desc": "Severe lithospheric rupture. Critical infrastructure failure reported." }
    ],
    "red": [
      { "magnitude": 6.6, "depth": 13.0, "cdi": 8.0, "mmi": 8.0, "sig": 34.0, "alert": "red", "status": "CATASTROPHIC", "desc": "Extreme shallow strike. Total structural collapse in immediate radius." },
      { "magnitude": 7.05, "depth": 11.0, "cdi": 8.0, "mmi": 8.0, "sig": 23.0, "alert": "red", "status": "CATASTROPHIC", "desc": "Major catastrophic event. Immediate widespread evacuation mandated." },
      { "magnitude": 7.23, "depth": 19.0, "cdi": 9.0, "mmi": 8.0, "sig": 93.0, "alert": "red", "status": "CATASTROPHIC", "desc": "Severe surface rupture. Communications grid offline in target sector." },
      { "magnitude": 7.51, "depth": 16.0, "cdi": 6.0, "mmi": 8.0, "sig": -29.0, "alert": "red", "status": "CATASTROPHIC", "desc": "Massive tectonic collapse. National emergency protocols active." },
      { "magnitude": 8.2, "depth": 47.0, "cdi": 9.0, "mmi": 7.0, "sig": 94.0, "alert": "red", "status": "CATASTROPHIC", "desc": "Great earthquake class. Global seismic shockwave detected." }
    ]
  };

  const CATEGORIES = [
    { id: 'ALL', label: 'ALL_NODES', color: 'text-white' },
    { id: 'green', label: 'STABLE', color: 'text-green-400' },
    { id: 'yellow', label: 'ADVISORY', color: 'text-yellow-400' },
    { id: 'orange', label: 'CRITICAL', color: 'text-orange-400' },
    { id: 'red', label: 'CATASTROPHIC', color: 'text-red-500' }
  ];

  const getAlertConfig = (level) => {
    const configs = {
      'green': { color: 'text-green-400', border: 'border-green-500/20', bgGlow: 'bg-green-500/5', icon: <Activity className="w-5 h-5" /> },
      'yellow': { color: 'text-yellow-400', border: 'border-yellow-500/20', bgGlow: 'bg-yellow-500/5', icon: <Info className="w-5 h-5" /> },
      'orange': { color: 'text-orange-400', border: 'border-orange-500/20', bgGlow: 'bg-orange-500/5', icon: <AlertTriangle className="w-5 h-5" /> },
      'red': { color: 'text-red-500', border: 'border-red-500/20', bgGlow: 'bg-red-500/5', icon: <ShieldAlert className="w-5 h-5" /> }
    };
    return configs[level.toLowerCase()];
  };

  const filteredData = activeFilter === 'ALL' 
    ? [...SAMPLES_DATA.green, ...SAMPLES_DATA.yellow, ...SAMPLES_DATA.orange, ...SAMPLES_DATA.red]
    : SAMPLES_DATA[activeFilter];

  return (
    <div className="min-h-screen pt-24 pb-12 px-6 flex flex-col items-center">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl w-full"
      >
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
          <div>
            <h1 className="text-3xl font-black text-white flex items-center space-x-4 tracking-[6px] uppercase">
              <Database className="text-cyan-400 w-10 h-10" />
              <span>TRAINING_ASSET_VAULT</span>
            </h1>
            <p className="text-[0.6rem] text-cyan-400/60 mt-3 font-mono tracking-widest uppercase font-bold flex items-center">
              <Zap className="w-3 h-3 mr-2 animate-pulse" />
              DATA_POINTS: 20 // FILTER: {activeFilter} // REGION: GLOBAL_ARCHIVE
            </p>
          </div>

          {/* Filter Bar */}
          <div className="flex flex-wrap gap-2 p-1 bg-black/40 border border-white/5 rounded-sm backdrop-blur-md">
            {CATEGORIES.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveFilter(cat.id)}
                className={`px-4 py-2 text-[0.6rem] font-bold tracking-widest transition-all rounded-sm uppercase ${
                  activeFilter === cat.id 
                    ? `${cat.id === 'ALL' ? 'bg-cyan-400 text-black' : `bg-white/10 ${cat.color} border border-white/10 shadow-[0_0_10px_rgba(255,255,255,0.05)]`}` 
                    : 'text-white/40 hover:text-white/70 hover:bg-white/5'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          {filteredData.map((sample, index) => {
            const config = getAlertConfig(sample.alert);
            return (
              <motion.div
                key={`${sample.alert}-${index}`}
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
                className={`holo-panel p-5 border ${config.border} relative overflow-hidden group hover:border-cyan-400/30 transition-all`}
              >
                <div className={`absolute inset-0 ${config.bgGlow} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />
                
                <div className="relative z-10 flex flex-col gap-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-sm bg-black/40 border border-white/5 ${config.color}`}>
                        {config.icon}
                      </div>
                      <div>
                        <h3 className={`text-sm font-black tracking-widest ${config.color}`}>
                          {sample.alert.toUpperCase()}_ALERT
                        </h3>
                        <p className="text-[0.5rem] text-white/40 font-mono uppercase tracking-tighter">REF_ID: TRN_{sample.alert.toUpperCase()}_0{index + 1}</p>
                      </div>
                    </div>
                    <div className="text-[0.5rem] font-mono text-cyan-400/40 uppercase tracking-widest bg-cyan-400/5 px-2 py-1 rounded-sm border border-cyan-400/10">
                      VERIFIED_TELEMETRY
                    </div>
                  </div>

                  <div className="grid grid-cols-5 gap-2">
                    {['magnitude', 'depth', 'cdi', 'mmi', 'sig'].map(key => (
                      <div key={key} className="text-center p-2 bg-black/40 border border-white/5 rounded-sm">
                        <p className="text-[0.45rem] text-white/20 font-black uppercase mb-1 font-mono tracking-tighter">{key.slice(0, 3)}</p>
                        <p className="text-[0.75rem] font-black text-white">{sample[key]}</p>
                      </div>
                    ))}
                  </div>

                  <p className="text-[0.65rem] text-white/60 font-medium leading-normal h-8 line-clamp-2">
                    {sample.desc}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>

        <div className="mt-16 p-8 border-t border-white/5 flex flex-col items-center">
            <div className="w-16 h-1 bg-cyan-400/20 mb-8 rounded-full overflow-hidden">
                <motion.div 
                    className="h-full bg-cyan-400"
                    animate={{ x: [-100, 100] }}
                    transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                />
            </div>
          <p className="text-[0.65rem] text-center text-white/30 font-mono tracking-[4px] uppercase max-w-3xl leading-relaxed">
            NEURAL_VAULT INITIALIZED. 20/20 VECTORS SYNCED. <br/>
            ALL DATA POINTS ARE AUTHENTIC RECORDS EXTRACTED FROM HISTORICAL SEISMIC ARTIFACTS.
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default SampleDataset;
