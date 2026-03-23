import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Sphere, MeshDistortMaterial, Points, PointMaterial } from '@react-three/drei';
import * as THREE from 'three';

const EarthPoints = ({ isHovered }) => {
  const pointsRef = useRef();

  // Create points on a sphere
  const [positions, initialPositions] = useMemo(() => {
    const count = 3000;
    const pos = new Float32Array(count * 3);
    const initial = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const phi = Math.acos(-1 + (2 * i) / count);
      const theta = Math.sqrt(count * Math.PI) * phi;
      
      const x = Math.cos(theta) * Math.sin(phi) * 2;
      const y = Math.sin(theta) * Math.sin(phi) * 2;
      const z = Math.cos(phi) * 2;
      
      pos[i * 3] = x;
      pos[i * 3 + 1] = y;
      pos[i * 3 + 2] = z;

      initial[i * 3] = x;
      initial[i * 3 + 1] = y;
      initial[i * 3 + 2] = z;
    }
    return [pos, initial];
  }, []);

  useFrame((state) => {
    pointsRef.current.rotation.y += 0.002;
    pointsRef.current.rotation.x += 0.001;

    const positions = pointsRef.current.geometry.attributes.position.array;
    const factor = isHovered ? 1.5 : 0;
    const t = state.clock.getElapsedTime();
    
    for (let i = 0; i < positions.length; i += 3) {
        const ix = initialPositions[i];
        const iy = initialPositions[i+1];
        const iz = initialPositions[i+2];

        // Normal direction (from center 0,0,0)
        const nx = ix / 2;
        const ny = iy / 2;
        const nz = iz / 2;

        // Displace points outwards with some noise/sin variation
        const targetX = ix + nx * factor * (1 + Math.sin(t * 2 + i * 0.1) * 0.2);
        const targetY = iy + ny * factor * (1 + Math.cos(t * 2 + i * 0.1) * 0.2);
        const targetZ = iz + nz * factor * (1 + Math.sin(t * 2 + i * 0.1) * 0.2);

        positions[i] = THREE.MathUtils.lerp(positions[i], targetX, 0.1);
        positions[i+1] = THREE.MathUtils.lerp(positions[i+1], targetY, 0.1);
        positions[i+2] = THREE.MathUtils.lerp(positions[i+2], targetZ, 0.1);
    }
    pointsRef.current.geometry.attributes.position.needsUpdate = true;
  });

  return (
    <Points ref={pointsRef} positions={positions} stride={3}>
      <PointMaterial
        transparent
        color="#22d3ee"
        size={0.015}
        sizeAttenuation={true}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </Points>
  );
};

const Globe = ({ isHovered }) => {
  const meshRef = useRef();
  
  useFrame((state) => {
    meshRef.current.rotation.y += 0.002;
    meshRef.current.rotation.x += 0.001;
    
    const targetScale = isHovered ? 0.8 : 1;
    const s = THREE.MathUtils.lerp(meshRef.current.scale.x, targetScale, 0.1);
    meshRef.current.scale.set(s, s, s);
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[2, 64, 64]} />
      <meshBasicMaterial 
        color="#0891b2" 
        wireframe 
        transparent 
        opacity={isHovered ? 0.05 : 0.15} 
      />
    </mesh>
  );
};

const Atmosphere = () => {
  const meshRef = useRef();

  useFrame((state) => {
    const t = state.clock.getElapsedTime();
    meshRef.current.rotation.y = -t * 0.05;
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[2.05, 64, 64]} />
      <meshBasicMaterial
        color="#22d3ee"
        transparent
        opacity={0.05}
        side={THREE.BackSide}
      />
    </mesh>
  );
};

const CyberEarth = () => {
  const [isHovered, setIsHovered] = React.useState(false);

  return (
    <div 
      className="w-full h-[500px] relative mt-20 mb-10 overflow-hidden cursor-crosshair group"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="absolute inset-0 z-0 opacity-40">
        <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-background"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.1)_0%,transparent_70%)]"></div>
      </div>
      
      <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center pointer-events-none z-10">
        <div className="text-center">
            <div className="inline-block px-4 py-1 border border-cyan-400/30 bg-cyan-400/5 backdrop-blur-sm mb-4">
                <span className={`text-[10px] font-black tracking-[4px] uppercase animate-pulse ${isHovered ? 'text-red-400' : 'text-cyan-400'}`}>
                    {isHovered ? 'SEISMIC_EVENT_SIMULATED' : 'PLANETARY_INTERCEPT_STREAM'}
                </span>
            </div>
            <div className="flex gap-2 justify-center mb-2">
                {[...Array(5)].map((_, i) => (
                    <div key={i} className={`w-1 h-1 ${isHovered ? 'bg-red-400' : 'bg-cyan-400/50'} animate-ping`} style={{ animationDelay: `${i * 0.2}s` }}></div>
                ))}
            </div>
        </div>
      </div>

      <Canvas camera={{ position: [0, 0, 6], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} color={isHovered ? "#f87171" : "#22d3ee"} />
        <Float
          speed={isHovered ? 4 : 1.5} 
          rotationIntensity={isHovered ? 2 : 0.5} 
          floatIntensity={isHovered ? 2 : 0.5} 
        >
          <group scale={1.2}>
            <Globe isHovered={isHovered} />
            <EarthPoints isHovered={isHovered} />
            <Atmosphere />
          </group>
        </Float>
      </Canvas>
      
      {/* Decorative scanner lines */}
      <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[450px] h-[1px] ${isHovered ? 'bg-red-400/40' : 'bg-cyan-400/20'} shadow-[0_0_15px_rgba(34,211,238,0.2)] transition-colors duration-300 pointer-events-none`}></div>
      <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[450px] w-[1px] ${isHovered ? 'bg-red-400/40' : 'bg-cyan-400/20'} shadow-[0_0_15px_rgba(34,211,238,0.2)] transition-colors duration-300 pointer-events-none`}></div>
      
      {/* HUD Elements */}
      <div className="absolute bottom-10 left-10 border-l border-cyan-400/40 pl-4 py-2 hidden md:block">
        <div className={`text-[9px] font-mono uppercase tracking-widest mb-1 ${isHovered ? 'text-red-400' : 'text-cyan-400/60'}`}>
            {isHovered ? 'CRITICAL_DISRUPTION_DETECTED' : 'Live_Telemetry_Stream_v2.0'}
        </div>
        <div className={`text-[11px] font-mono ${isHovered ? 'text-red-400/60' : 'text-white/40'} uppercase tracking-tighter transition-colors`}>
            LAT: 35.6895° N [ACTIVE]<br/>
            LONG: 139.6917° E [ACTIVE]<br/>
            ALT: {isHovered ? 'VARIABLE' : '0.00km'} [STABLE]
        </div>
      </div>

      <div className="absolute top-10 right-10 border-r border-cyan-400/40 pr-4 py-2 text-right hidden md:block">
        <div className={`text-[9px] font-mono uppercase tracking-widest mb-1 ${isHovered ? 'text-red-400' : 'text-cyan-400/60'}`}>Neural_Inference_Core</div>
        <div className={`text-[11px] font-mono ${isHovered ? 'text-red-400/60' : 'text-white/40'} uppercase tracking-tighter transition-colors`}>
            NODE_UPTIME: 142.5h<br/>
            SYNC_RATE: {isHovered ? 'DEGRADING' : '99.8%'}<br/>
            OVERRIDE: {isHovered ? 'ACTIVE' : 'INACTIVE'}
        </div>
      </div>
    </div>
  );
};

export default CyberEarth;
