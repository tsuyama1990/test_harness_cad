import { Node, Edge } from 'reactflow';
import { Harness } from '../services/api';

export const transformHarnessToFlow = (harness: Harness): { nodes: Node[]; edges: Edge[] } => {
  const nodes: Node[] = harness.connectors.map((connector, index) => ({
    id: connector.id,
    type: 'default',
    data: { label: `${connector.id} (${connector.part_number})` },
    position: { x: index * 250, y: Math.random() * 400 }, // Simple initial positioning
  }));

  const edges: Edge[] = harness.connections.map((connection, index) => ({
    id: `e${index}-${connection.from_connector_id}-${connection.to_connector_id}`,
    source: connection.from_connector_id,
    target: connection.to_connector_id,
    label: connection.wire_id,
  }));

  return { nodes, edges };
};
