import type { Node, Edge } from 'reactflow';

// This mirrors the Pydantic schemas in the backend
export interface PinData {
  id: string;
}

export interface ConnectorData {
  id: string;
  manufacturer: string;
  part_number: string;
  pins: PinData[];
}

export interface WireData {
  id: string;
  manufacturer: string;
  part_number: string;
  color: string;
  gauge: number;
  length: number; // in mm
}

export interface ConnectionData {
  wire_id: string;
  from_connector_id: string;
  from_pin_id: string;
  to_connector_id: string;
  to_pin_id: string;
}

export interface HarnessData {
  name: string;
  connectors: ConnectorData[];
  wires: WireData[];
  connections: ConnectionData[];
}

// --- Transformation Functions ---

export const transformHarnessToFlow = (
  harness: HarnessData
): { nodes: Node[]; edges: Edge[] } => {
  const nodes: Node[] = harness.connectors.map((connector) => ({
    id: connector.id,
    type: 'customConnector', // Use the custom node type
    data: {
      label: connector.id,
      part_number: connector.part_number,
      pins: connector.pins,
    },
    position: { x: Math.random() * 400, y: Math.random() * 400 }, // Position will be managed by layout
  }));

  const edges: Edge[] = harness.connections.map((connection, index) => ({
    id: `e${index}-${connection.from_connector_id}-${connection.to_connector_id}`,
    source: connection.from_connector_id,
    target: connection.to_connector_id,
    sourceHandle: connection.from_pin_id,
    targetHandle: connection.to_pin_id,
    type: 'customWire', // Use the custom edge type
    data: {
      wire_id: connection.wire_id,
      // Find the corresponding wire to get its color
      color: harness.wires.find((w) => w.id === connection.wire_id)?.color || 'gray',
    },
  }));

  return { nodes, edges };
};

export const transformFlowToHarness = (
  nodes: Node[],
  edges: Edge[]
): HarnessData => {
  const connectors: ConnectorData[] = nodes
    .filter((node) => node.type === 'customConnector')
    .map((node) => ({
      id: node.id,
      manufacturer: 'Unknown', // This should be populated from node.data in a real app
      part_number: node.data.part_number || 'Unknown',
      pins: node.data.pins || [],
    }));

  const connections: ConnectionData[] = edges.map((edge) => ({
    wire_id: edge.data.wire_id,
    from_connector_id: edge.source,
    from_pin_id: edge.sourceHandle || '',
    to_connector_id: edge.target,
    to_pin_id: edge.targetHandle || '',
  }));

  // Wires need to be inferred from the connections or managed separately.
  // For now, we'll create a placeholder wire for each connection.
  const wires: WireData[] = edges.map((edge) => ({
    id: edge.data.wire_id,
    manufacturer: 'Generic',
    part_number: `UL1007-${edge.data.color.toUpperCase()}`,
    color: edge.data.color,
    gauge: 22,
    length: 150, // Default length
  }));

  return {
    name: 'Updated Harness', // This could be managed in the store as well
    connectors,
    wires,
    connections,
  };
};
