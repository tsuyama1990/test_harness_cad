import { v4 as uuidv4 } from 'uuid';
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { addEdge, applyNodeChanges, applyEdgeChanges } from 'reactflow';
import type {
  Connection,
  Edge,
  EdgeChange,
  Node,
  NodeChange,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
} from 'reactflow';
import { updateHarness } from '../services/api';
import {
  transformFlowToHarness,
  type HarnessData,
} from '../utils/dataTransformer';
import { debounce } from 'lodash';

// Debounced function to update harness data on the backend
const debouncedUpdateHarness = debounce(
  (harnessId: string, harnessData: HarnessData) => {
    updateHarness(harnessId, harnessData);
  },
  500
);

export interface HarnessState {
  nodes: Node[];
  edges: Edge[];
  harnessId: string | null;
  setHarnessId: (id: string) => void;
  setNodes: (nodes: Node[]) => void;
  setEdges: (edges: Edge[]) => void;
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  updateNodeData: (nodeId: string, data: Record<string, unknown>) => void;
  setInitialData: (nodes: Node[], edges: Edge[]) => void;
}

const useHarnessStore = create<HarnessState>()(
  immer(
    (set, get) => ({
      nodes: [],
      edges: [],
      harnessId: null,
      setHarnessId: (id: string) => set({ harnessId: id }),
      setNodes: (nodes: Node[]) => set({ nodes }),
      setEdges: (edges: Edge[]) => set({ edges }),
      onNodesChange: (changes: NodeChange[]) => {
        set((state) => {
          state.nodes = applyNodeChanges(changes, state.nodes);
        });
        const { nodes, edges, harnessId } = get();
        if (harnessId) {
          const harnessData = transformFlowToHarness(nodes, edges);
          debouncedUpdateHarness(harnessId, harnessData);
        }
      },
      onEdgesChange: (changes: EdgeChange[]) => {
        set((state) => {
          state.edges = applyEdgeChanges(changes, state.edges);
        });
        const { nodes, edges, harnessId } = get();
        if (harnessId) {
          const harnessData = transformFlowToHarness(nodes, edges);
          debouncedUpdateHarness(harnessId, harnessData);
        }
      },
      onConnect: (connection: Connection) => {
        set((state) => {
          const newEdge = {
            ...connection,
            id: uuidv4(), // Generate a unique ID for the edge
            data: {
              wire_id: uuidv4(), // Generate a unique wire_id
              color: 'black', // Default color
            },
          };
          state.edges = addEdge(newEdge, state.edges);
        });
        const { nodes, edges, harnessId } = get();
        if (harnessId) {
          const harnessData = transformFlowToHarness(nodes, edges);
          debouncedUpdateHarness(harnessId, harnessData);
        }
      },
      updateNodeData: (nodeId: string, data: Record<string, unknown>) => {
        set((state) => {
          const nodeToUpdate = state.nodes.find((node) => node.id === nodeId);
          if (nodeToUpdate) {
            nodeToUpdate.data = { ...nodeToUpdate.data, ...data };
          }
        });
        const { nodes, edges, harnessId } = get();
        if (harnessId) {
          const harnessData = transformFlowToHarness(nodes, edges);
          debouncedUpdateHarness(harnessId, harnessData);
        }
      },
      setInitialData: (nodes: Node[], edges: Edge[]) => {
        set({
          nodes: nodes,
          edges: edges,
        });
      },
    })
  )
);

export default useHarnessStore;
