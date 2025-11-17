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
        setPoints([...points, intersects[0].point]);
      }
    },
    [points, camera, modelRef]
  );

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
      {points.length > 1 && <Line points={points} color="red" lineWidth={3} />}
      <div style={{ position: 'absolute', top: '10px', left: '10px', background: 'white', padding: '5px' }}>
        <button onClick={savePath}>Save Path</button>
        <label>
          Margin:
          <input
            type="number"
            value={manufacturingMargin}
            onChange={(e) => setManufacturingMargin(parseFloat(e.target.value))}
            step="0.01"
            min="1"
          />
        </label>
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
