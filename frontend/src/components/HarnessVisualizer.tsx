import React, { useEffect, useCallback, useRef, useState } from 'react';
import ReactFlow, {
  Controls,
  Background,
  MiniMap,
} from 'reactflow';
import type { ReactFlowInstance } from 'reactflow';
import 'reactflow/dist/style.css';
import useHarnessStore from '../stores/useHarnessStore';
import { getHarness } from '../services/api';
import { transformHarnessToFlow } from '../utils/dataTransformer';
import CustomConnectorNode from './CustomConnectorNode';
import CustomWireEdge from './CustomWireEdge';

const nodeTypes = { customConnector: CustomConnectorNode };
const edgeTypes = { customWire: CustomWireEdge };

interface HarnessVisualizerProps {
  harnessId: string;
}

// The core logic is moved into this new component.
const FlowCanvas: React.FC<HarnessVisualizerProps> = ({ harnessId }) => {
  const {
    nodes,
    edges,
    setInitialData,
    onNodesChange,
    onEdgesChange,
    onConnect,
    setHarnessId,
    setNodes, // Keep for onDrop
  } = useHarnessStore();
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance | null>(null);

  useEffect(() => {
    setHarnessId(harnessId);
    const fetchHarnessData = async () => {
      try {
        const harnessData = await getHarness(harnessId);
        const { nodes: transformedNodes, edges: transformedEdges } =
          transformHarnessToFlow(harnessData);
        setInitialData(transformedNodes, transformedEdges);
      } catch (error) {
        console.error('Failed to fetch harness data:', error);
      }
    };
    fetchHarnessData();
  }, [harnessId, setHarnessId, setInitialData]);

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      if (!reactFlowInstance) {
        return;
      }

      const type = event.dataTransfer.getData('application/reactflow-type');
      const data = JSON.parse(event.dataTransfer.getData('application/reactflow-data'));

      // check if the dropped element is valid
      if (typeof type === 'undefined' || !type) {
        return;
      }

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const newNode = {
        id: `${data.name}-${+new Date()}`,
        type: 'customConnector',
        position,
        data: {
          label: data.name,
          part_number: data.part_number,
          pins: data.pins,
        },
      };

      setNodes([...nodes, newNode]);
    },
    [reactFlowInstance, nodes, setNodes]
  );

  return (
    <div style={{ width: '100%', height: '100%' }} ref={reactFlowWrapper} data-testid="rf-canvas-wrapper">
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
        onLoad={setReactFlowInstance}
        fitView
      >
        <Controls />
        <Background />
        <MiniMap />
      </ReactFlow>
    </div>
  );
};


// The exported component remains the same, but now it just renders the FlowCanvas.
// Since FlowCanvas is a child of HarnessVisualizer, and HarnessVisualizer is a child
// of ReactFlowProvider in App.tsx, we ensure the context is available.
const HarnessVisualizer: React.FC<HarnessVisualizerProps> = ({ harnessId }) => {
  return <FlowCanvas harnessId={harnessId} />;
};

export default HarnessVisualizer;
