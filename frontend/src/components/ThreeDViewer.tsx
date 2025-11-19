/* eslint-disable react/no-unknown-property */
import React, { useState, useCallback, useEffect, useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import type { ThreeEvent } from '@react-three/fiber';
import { OrbitControls, Gltf, Line } from '@react-three/drei';
import * as THREE from 'three';
import useHarnessStore from '../stores/useHarnessStore';
import axios from 'axios';
import PathEditorPanel from './PathEditorPanel'; // Import the new component

interface ThreeDViewerProps {
  modelPath: string | null;
}

const PathCreator = () => {
  const [points, setPoints] = useState<THREE.Vector3[]>([]);
  const [pathLength, setPathLength] = useState(0);
  const {
    harnessId,
    edges,
    updateWireLength,
    updateEdgeData,
    selectedEdgeId,
    manufacturingMargin,
    setManufacturingMargin,
  } = useHarnessStore();

  const selectedEdge = useMemo(
    () => edges.find((e) => e.id === selectedEdgeId),
    [edges, selectedEdgeId]
  );
  const wireColor = selectedEdge?.data?.color || 'hotpink';
  const totalLength = pathLength * manufacturingMargin;

  const calculateLength = useCallback((currentPoints: THREE.Vector3[]) => {
    let length = 0;
    for (let i = 0; i < currentPoints.length - 1; i++) {
      length += currentPoints[i].distanceTo(currentPoints[i + 1]);
    }
    setPathLength(length);
  }, []);

  useEffect(() => {
    if (selectedEdge?.data?.path_3d) {
      const existingPoints = selectedEdge.data.path_3d.map(
        (p: { x: number; y: number; z: number }) =>
          new THREE.Vector3(p.x, p.y, p.z)
      );
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setPoints(existingPoints);
      calculateLength(existingPoints);
    } else {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setPoints([]);
      setPathLength(0);
    }
  }, [selectedEdge, calculateLength]);

  const handleCanvasClick = useCallback(
    (event: ThreeEvent<MouseEvent>) => {
      if (!selectedEdgeId) return;

      event.stopPropagation();

      const newPoints = [...points, event.point];
      setPoints(newPoints);
      calculateLength(newPoints);
    },
    [points, calculateLength, selectedEdgeId]
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

  useEffect(() => {
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
    if (selectedEdge) {
      const path_3d = points.map((p) => ({ x: p.x, y: p.y, z: p.z }));
      updateEdgeData(selectedEdge.id, { path_3d });

      try {
        const response = await axios.put(
          `/api/v1/harnesses/${harnessId}/wires/${selectedEdge.data.wire_id}/3d-path`,
          {
            points: path_3d,
          },
          {
            params: {
              manufacturing_margin: manufacturingMargin,
            },
          }
        );
        updateWireLength(selectedEdge.id, response.data.length);
      } catch (error) {
        console.error('Error saving 3D path:', error);
      }
    }
  };

  return (
    <>
      <mesh onClick={handleCanvasClick}>
        <planeGeometry args={[1000, 1000]} />
        <meshStandardMaterial
          transparent
          opacity={0}
          side={THREE.DoubleSide}
        />
      </mesh>
      {points.map((point, index) => (
        <mesh key={index} position={point}>
          <sphereGeometry args={[0.5, 16, 16]} />
          <meshStandardMaterial color={wireColor} />
        </mesh>
      ))}
      {points.length > 1 && (
        <Line points={points} color={wireColor} lineWidth={3} />
      )}

      <PathEditorPanel
        selectedEdgeId={selectedEdgeId}
        wireColor={wireColor}
        pathLength={pathLength}
        totalLength={totalLength}
        manufacturingMargin={manufacturingMargin}
        setManufacturingMargin={setManufacturingMargin}
        onSave={savePath}
        onUndo={undo}
        onClear={clearPath}
      />
    </>
  );
};

const ThreeDViewer: React.FC<ThreeDViewerProps> = ({ modelPath }) => {
  return (
    <Canvas className="bg-gray-50">
      <ambientLight intensity={0.5} />
      <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
      <pointLight position={[-10, -10, -10]} />
      {modelPath && <Gltf src={modelPath} />}
      <PathCreator />
      <OrbitControls />
    </Canvas>
  );
};

export default ThreeDViewer;
