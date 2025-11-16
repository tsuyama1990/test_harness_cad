import React, { useEffect, useCallback, useRef } from 'react';
import ReactFlow, {
  Controls,
  Background,
  MiniMap,
  useReactFlow,
} from 'reactflow';
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

const HarnessVisualizer: React.FC<HarnessVisualizerProps> = ({ harnessId }) => {
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
  const { screenToFlowPosition } = useReactFlow();

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

      const reactFlowBounds = reactFlowWrapper.current?.getBoundingClientRect();
      const type = event.dataTransfer.getData('application/reactflow-type');
      const data = JSON.parse(event.dataTransfer.getData('application/reactflow-data'));

      // check if the dropped element is valid
      if (typeof type === 'undefined' || !type) {
        return;
      }

      const position = screenToFlowPosition({
        x: event.clientX - (reactFlowBounds?.left ?? 0),
        y: event.clientY - (reactFlowBounds?.top ?? 0),
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
    [screenToFlowPosition, nodes, setNodes]
  );

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
