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
  setInitialData: (nodes: Node[], edges: Edge[]) => void; // New action
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

  setInitialData: (nodes: Node[], edges: Edge[]) => {
    set({ nodes, edges });
  },

  onNodesChange: (changes: NodeChange[]) => {
    const newNodes = applyNodeChanges(changes, get().nodes);
    set({ nodes: newNodes });
    const { edges, harnessId } = get();
    if (harnessId) {
      const harnessData = transformFlowToHarness(newNodes, edges);
      debouncedUpdateHarness(harnessId, harnessData);
    }
  },

  onEdgesChange: (changes: EdgeChange[]) => {
    const newEdges = applyEdgeChanges(changes, get().edges);
    set({ edges: newEdges });
    const { nodes, harnessId } = get();
    if (harnessId) {
      const harnessData = transformFlowToHarness(nodes, newEdges);
      debouncedUpdateHarness(harnessId, harnessData);
    }
  },

  onConnect: (connection: Connection) => {
    const newEdges = addEdge(connection, get().edges);
    set({ edges: newEdges });
    const { nodes, harnessId } = get();
    if (harnessId) {
      const harnessData = transformFlowToHarness(nodes, newEdges);
      debouncedUpdateHarness(harnessId, harnessData);
    }
  },

  updateNodeData: (nodeId: string, data: any) => {
    const newNodes = get().nodes.map((node) =>
      node.id === nodeId ? { ...node, data: { ...node.data, ...data } } : node
    );
    set({ nodes: newNodes });
    const { edges, harnessId } = get();
    if (harnessId) {
      const harnessData = transformFlowToHarness(newNodes, edges);
      debouncedUpdateHarness(harnessId, harnessData);
    }
  },
}));

export default useHarnessStore;
