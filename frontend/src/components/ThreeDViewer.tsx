/* eslint-disable react/no-unknown-property */
import React, { useState, useCallback } from 'react';
import { Canvas, useThree } from '@react-three/fiber';
import { OrbitControls, Gltf, Line } from '@react-three/drei';
import * as THREE from 'three';
import useHarnessStore from '../stores/useHarnessStore';
import axios from 'axios';

interface ThreeDViewerProps {
  modelPath: string | null;
}

const PathCreator = ({ modelRef }: { modelRef: React.RefObject<THREE.Group> }) => {
  const [points, setPoints] = useState<THREE.Vector3[]>([]);
  const [pathLength, setPathLength] = useState(0);
  const { camera, size } = useThree();
  const {
    harnessId,
    edges,
    updateWireLength,
    updateEdgeData,
    selectedEdgeId,
    manufacturingMargin,
    setManufacturingMargin,
  } = useHarnessStore();

  const calculateLength = useCallback((currentPoints: THREE.Vector3[]) => {
    let length = 0;
    for (let i = 0; i < currentPoints.length - 1; i++) {
      length += currentPoints[i].distanceTo(currentPoints[i + 1]);
    }
    setPathLength(length);
  }, []);

  const handleCanvasClick = useCallback(
    (event: MouseEvent) => {
      if (!modelRef.current) return;

      const raycaster = new THREE.Raycaster();
      const mouse = new THREE.Vector2();
      mouse.x = (event.clientX / size.width) * 2 - 1;
      mouse.y = -(event.clientY / size.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);

      const intersects = raycaster.intersectObjects(modelRef.current.children, true);

      if (intersects.length > 0) {
        const newPoints = [...points, intersects[0].point];
        setPoints(newPoints);
        calculateLength(newPoints);
      }
    },
    [points, camera, modelRef, size, calculateLength]
  );

  const undo = useCallback(() => {
    const newPoints = points.slice(0, -1);
    setPoints(newPoints);
    calculateLength(newPoints);
  }, [points, calculateLength]);

  const clearPath = useCallback(() => {
    setPoints([]);
    setPathLength(0);
  }, []);

  React.useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.ctrlKey && event.key === 'z') {
        undo();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [undo]);

  const savePath = async () => {
    const edge = edges.find(e => e.id === selectedEdgeId);
    if (edge) {
      const path_3d = points.map(p => ({ x: p.x, y: p.y, z: p.z }));
      updateEdgeData(edge.id, { path_3d });

      try {
        const response = await axios.put(
          `/api/v1/harnesses/${harnessId}/wires/${edge.data.wire_id}/3d-path`,
          {
            points: path_3d,
          },
          {
            params: {
              manufacturing_margin: manufacturingMargin,
            },
          }
        );
        updateWireLength(edge.id, response.data.length);
      } catch (error) {
        console.error('Error saving 3D path:', error);
      }
    }
  };

  return (
    <>
      <mesh onClick={handleCanvasClick}>
        <boxBufferGeometry args={[1000, 1000, 1000]} />
        <meshStandardMaterial transparent opacity={0} />
      </mesh>
      {points.map((point, index) => (
        <mesh key={index} position={point}>
          <sphereGeometry args={[0.5, 16, 16]} />
          <meshStandardMaterial color="hotpink" />
        </mesh>
      ))}
      {points.length > 1 && <Line points={points} color={wireColor} lineWidth={3} />}
      <div
        style={{
          position: 'absolute',
          top: '10px',
          left: '10px',
          background: 'rgba(255, 255, 255, 0.5)',
          padding: '10px',
          borderRadius: '5px',
        }}
      >
        <button onClick={savePath} style={{ marginBottom: '5px' }}>
          Save Path
        </button>
        <button onClick={undo} style={{ marginBottom: '5px', marginLeft: '5px' }}>
          Undo
        </button>
        <button onClick={clearPath} style={{ marginBottom: '5px', marginLeft: '5px' }}>
          Clear Path
        </button>
        <div>
          <label>
            Margin:
            <input
              type="number"
              value={manufacturingMargin}
              onChange={(e) => setManufacturingMargin(parseFloat(e.target.value))}
              step="0.01"
              min="1"
              style={{ width: '60px', marginLeft: '5px' }}
            />
          </label>
        </div>
        <div style={{ marginTop: '5px' }}>Length: {pathLength.toFixed(2)} mm</div>
      </div>
    </>
  );
};

const ThreeDViewer: React.FC<ThreeDViewerProps> = ({ modelPath }) => {
  const modelRef = React.useRef<THREE.Group>(null);

  return (
    <Canvas style={{ background: '#f0f0f0' }}>
      <ambientLight intensity={0.5} />
      <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
      <pointLight position={[-10, -10, -10]} />
      {modelPath && <Gltf src={modelPath} ref={modelRef} />}
      <PathCreator modelRef={modelRef} />
      <OrbitControls />
    </Canvas>
  );
};

export default ThreeDViewer;
