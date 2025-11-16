import React, { useCallback, useRef } from 'react';
import ReactFlow, {
  Controls,
  Background,
  MiniMap,
  useReactFlow,
} from 'reactflow';
import 'reactflow/dist/style.css';
import useHarnessStore from '../stores/useHarnessStore';
import CustomConnectorNode from './CustomConnectorNode';
import CustomWireEdge from './CustomWireEdge';
import { useHarnessData } from '../hooks/useHarnessData';
import { useReactFlowCallbacks } from '../hooks/useReactFlowCallbacks';
import { useHarnessSync } from '../hooks/useHarnessSync';

const nodeTypes = { customConnector: CustomConnectorNode };
const edgeTypes = { customWire: CustomWireEdge };

interface HarnessVisualizerProps {
  harnessId: string;
}

const HarnessVisualizer: React.FC<HarnessVisualizerProps> = ({ harnessId }) => {
  // --- Custom Hooks for Logic Separation ---
  const { loading, error } = useHarnessData(harnessId);
  const { onNodesChange, onEdgesChange, onConnect } = useReactFlowCallbacks();
  useHarnessSync(); // This hook handles background synchronization

  // --- Store State and Actions ---
  const { nodes, edges, addNode } = useHarnessStore((state) => ({
    nodes: state.nodes,
    edges: state.edges,
    addNode: state.addNode,
  }));

  // --- React Flow Instance and Refs ---
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const { screenToFlowPosition } = useReactFlow();

  // --- Drag and Drop Handlers ---
  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow-type');
      const dataString = event.dataTransfer.getData('application/reactflow-data');

      if (!type || !dataString || !reactFlowWrapper.current) {
        return;
      }
      const data = JSON.parse(dataString);
      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();

      const position = screenToFlowPosition({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const newNode = {
        id: `${data.name}-${+new Date()}`,
        type: 'customConnector',
        position,
        data: {
          label: data.name,
          ...data,
        },
      };
      addNode(newNode);
    },
    [screenToFlowPosition, addNode]
  );

  // --- Render Logic ---
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading harness data.</div>;

  return (
    <div style={{ width: '100%', height: '100%' }} ref={reactFlowWrapper}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        onDragOver={onDragOver}
        onDrop={onDrop}
        fitView
      >
        <Controls />
        <Background />
        <MiniMap />
      </ReactFlow>
    </div>
  );
};

export default HarnessVisualizer;
