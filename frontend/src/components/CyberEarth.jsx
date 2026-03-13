import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Sphere, MeshDistortMaterial, Points, PointMaterial } from '@react-three/drei';
import * as THREE from 'three';

const EarthPoints = () => {
  const pointsRef = useRef();

  // Create points on a sphere
  const [positions, setPositions] = useMemo(() => {
    const count = 3000;
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const phi = Math.acos(-1 + (2 * i) / count);
      const theta = Math.sqrt(count * Math.PI) * phi;
      
      const x = Math.cos(theta) * Math.sin(phi) * 2;
      const y = Math.sin(theta) * Math.sin(phi) * 2;
      const z = Math.cos(phi) * 2;
      
      pos[i * 3] = x;
      pos[i * 3 + 1] = y;
      pos[i * 3 + 2] = z;
    }
    return [pos];
  }, []);

  useFrame((state) => {
    pointsRef.current.rotation.y += 0.002;
    pointsRef.current.rotation.x += 0.001;
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

const Globe = () => {
  const meshRef = useRef();
  
  useFrame((state) => {
    meshRef.current.rotation.y += 0.002;
    meshRef.current.rotation.x += 0.001;
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[2, 64, 64]} />
      <meshBasicMaterial 
        color="#0891b2" 
        wireframe 
        transparent 
        opacity={0.15} 
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
  return (
    <div className="w-full h-[500px] relative mt-20 mb-10 overflow-hidden">
      <div className="absolute inset-0 z-0 opacity-40">
        <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-background"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.1)_0%,transparent_70%)]"></div>
      </div>
      
      <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center pointer-events-none z-10">
        <div className="text-center">
            <div className="flex gap-2 justify-center mb-2">
                {[...Array(5)].map((_, i) => (
                    <div key={i} className="w-1 h-1 bg-cyan-400/50 animate-ping" style={{ animationDelay: `${i * 0.2}s` }}></div>
                ))}
            </div>
        </div>
      </div>

      <Canvas camera={{ position: [0, 0, 6], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#22d3ee" />
        <Float
          speed={1.5} 
          rotationIntensity={0.5} 
          floatIntensity={0.5} 
        >
          <group scale={1.2}>
            <Globe />
            <EarthPoints />
            <Atmosphere />
          </group>
        </Float>
      </Canvas>
      
      {/* Decorative scanner lines */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[450px] h-[1px] bg-cyan-400/20 shadow-[0_0_15px_rgba(34,211,238,0.2)] pointer-events-none"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[450px] w-[1px] bg-cyan-400/20 shadow-[0_0_15px_rgba(34,211,238,0.2)] pointer-events-none"></div>
      
      {/* HUD Elements */}
      <div className="absolute bottom-10 left-10 border-l border-cyan-400/40 pl-4 py-2 hidden md:block">
        <div className="text-[9px] font-mono text-cyan-400/60 uppercase tracking-widest mb-1">Live_Telemetry_Stream</div>
        <div className="text-[11px] font-mono text-white/40 uppercase tracking-tighter">
            LAT: 35.6895° N<br/>
            LONG: 139.6917° E<br/>
            ALT: 0.00km
        </div>
      </div>

      <div className="absolute top-10 right-10 border-r border-cyan-400/40 pr-4 py-2 text-right hidden md:block">
        <div className="text-[9px] font-mono text-cyan-400/60 uppercase tracking-widest mb-1">System_Diagnostics</div>
        <div className="text-[11px] font-mono text-white/40 uppercase tracking-tighter">
            NODE_UPTIME: 142.5h<br/>
            SYNC_RATE: 99.8%<br/>
            ENCRYPTION: AES-256
        </div>
      </div>
    </div>
  );
};

export default CyberEarth;
