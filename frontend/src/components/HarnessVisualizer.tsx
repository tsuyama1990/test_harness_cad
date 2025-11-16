import React, { useEffect, useState, useCallback } from 'react';
import ReactFlow, {
  Controls,
  Background,
  Node,
  Edge,
  useNodesState,
  useEdgesState,
  useReactFlow,
  ReactFlowProvider,
} from 'reactflow';
import 'reactflow/dist/style.css';
import dagre from 'dagre';
import { getHarness } from '../services/api';
import { transformHarnessToFlow } from '../utils/dataTransformer';

interface HarnessVisualizerProps {
  harnessId: string;
}

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 172;
const nodeHeight = 36;

const getLayoutedElements = (nodes: Node[], edges: Edge[]) => {
  dagreGraph.setGraph({ rankdir: 'LR' });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  nodes.forEach((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    node.targetPosition = 'left';
    node.sourcePosition = 'right';

    // We are shifting the dagre node position (anchor=center center) to the top left
    // so it matches the React Flow node anchor point (top left).
    node.position = {
      x: nodeWithPosition.x - nodeWidth / 2,
      y: nodeWithPosition.y - nodeHeight / 2,
    };

    return node;
  });

  return { nodes, edges };
};

const HarnessVisualizer: React.FC<HarnessVisualizerProps> = ({ harnessId }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const { fitView } = useReactFlow();

  useEffect(() => {
    const fetchAndLayoutData = async () => {
      try {
        const harnessData = await getHarness(harnessId);
        const { nodes: transformedNodes, edges: transformedEdges } = transformHarnessToFlow(harnessData);
        const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
          transformedNodes,
          transformedEdges
        );
        setNodes(layoutedNodes);
        setEdges(layoutedEdges);
      } catch (error) {
        console.error('Failed to fetch harness data:', error);
      }
    };

    if (harnessId) {
      fetchAndLayoutData();
    }
  }, [harnessId, setNodes, setEdges]);

  const onLayout = useCallback(() => {
    const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
      nodes,
      edges
    );
    setNodes([...layoutedNodes]);
    setEdges([...layoutedEdges]);
    fitView({ duration: 800, padding: 0.1 });
  }, [nodes, edges, setNodes, setEdges, fitView]);


  useEffect(() => {
    if (nodes.length > 0) {
      fitView({ duration: 800, padding: 0.1 });
    }
  }, [nodes, fitView]);


  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
      >
        <Controls />
        <Background />
      </ReactFlow>
      <button onClick={onLayout} style={{ position: 'absolute', right: 10, top: 10, zIndex: 4 }}>
        Layout
      </button>
    </div>
  );
};


const HarnessVisualizerWrapper: React.FC<HarnessVisualizerProps> = (props) => {
  return (
    <ReactFlowProvider>
      <HarnessVisualizer {...props} />
    </ReactFlowProvider>
  );
};

export default HarnessVisualizerWrapper;
