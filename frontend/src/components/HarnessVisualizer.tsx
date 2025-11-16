import React, { useRef } from 'react';
import ReactFlow, {
  Controls,
  Background,
  MiniMap,
  ReactFlowProvider,
} from 'reactflow';
import 'reactflow/dist/style.css';
import useHarnessStore from '../stores/useHarnessStore';
import CustomConnectorNode from './CustomConnectorNode';
import CustomWireEdge from './CustomWireEdge';
import { useHarnessData } from '../hooks/useHarnessData';
import { useReactFlowDnD } from '../hooks/useReactFlowDnD';
import { useHarnessSync } from '../hooks/useHarnessSync';

const nodeTypes = { customConnector: CustomConnectorNode };
const edgeTypes = { customWire: CustomWireEdge };

interface HarnessVisualizerProps {
  harnessId: string;
}

const FlowCanvas: React.FC<HarnessVisualizerProps> = ({ harnessId }) => {
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect } =
    useHarnessStore();
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  useHarnessData(harnessId);
  useHarnessSync();
  const { onDragOver, onDrop } = useReactFlowDnD();

  return (
    <div
      style={{ width: '100%', height: '100%' }}
      ref={reactFlowWrapper}
      data-testid="rf-canvas-wrapper"
    >
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

// The exported component now includes the ReactFlowProvider
const HarnessVisualizer: React.FC<HarnessVisualizerProps> = ({ harnessId }) => {
  return (
    <ReactFlowProvider>
      <FlowCanvas harnessId={harnessId} />
    </ReactFlowProvider>
  );
};

export default HarnessVisualizer;
