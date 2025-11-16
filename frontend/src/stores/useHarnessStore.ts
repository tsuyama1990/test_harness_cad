import { create } from 'zustand';
import {
  Connection,
  Edge,
  EdgeChange,
  Node,
  NodeChange,
  addEdge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';
import { updateHarness } from '../services/api';
import {
  transformFlowToHarness,
  HarnessData,
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
  updateNodeData: (nodeId: string, data: any) => void;
}

const useHarnessStore = create<HarnessState>((set, get) => ({
  nodes: [],
  edges: [],
  harnessId: null,

  setHarnessId: (id: string) => set({ harnessId: id }),

  setNodes: (nodes: Node[]) => set({ nodes }),

  setEdges: (edges: Edge[]) => set({ edges }),

  onNodesChange: (changes: NodeChange[]) => {
    set({
      nodes: applyNodeChanges(changes, get().nodes),
    });
    const { nodes, edges, harnessId } = get();
    if (harnessId) {
      const harnessData = transformFlowToHarness(nodes, edges);
      debouncedUpdateHarness(harnessId, harnessData);
    }
  },

  onEdgesChange: (changes: EdgeChange[]) => {
    set({
      edges: applyEdgeChanges(changes, get().edges),
    });
    const { nodes, edges, harnessId } = get();
    if (harnessId) {
      const harnessData = transformFlowToHarness(nodes, edges);
      debouncedUpdateHarness(harnessId, harnessData);
    }
  },

  onConnect: (connection: Connection) => {
    set({
      edges: addEdge(connection, get().edges),
    });
    const { nodes, edges, harnessId } = get();
    if (harnessId) {
      const harnessData = transformFlowToHarness(nodes, edges);
      debouncedUpdateHarness(harnessId, harnessData);
    }
  },

  updateNodeData: (nodeId: string, data: any) => {
    set({
      nodes: get().nodes.map((node) =>
        node.id === nodeId ? { ...node, data: { ...node.data, ...data } } : node
      ),
    });
    const { nodes, edges, harnessId } = get();
    if (harnessId) {
      const harnessData = transformFlowToHarness(nodes, edges);
      debouncedUpdateHarness(harnessId, harnessData);
    }
  },
}));

export default useHarnessStore;
