import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
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

type State = {
  nodes: Node[];
  edges: Edge[];
  harnessId: string | null;
};

type Actions = {
  setInitialState: (harnessId: string, nodes: Node[], edges: Edge[]) => void;
  addNode: (node: Node) => void;
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  updateNodeData: (nodeId: string, data: Record<string, unknown>) => void;
};

export const useHarnessStore = create<State & Actions>()(
  immer((set) => ({
    nodes: [],
    edges: [],
    harnessId: null,

    setInitialState: (harnessId, nodes, edges) => {
      set((state) => {
        state.harnessId = harnessId;
        state.nodes = nodes;
        state.edges = edges;
      });
    },

    addNode: (node: Node) => {
      set((state) => {
        state.nodes.push(node);
      });
    },

    onNodesChange: (changes: NodeChange[]) => {
      set((state) => {
        state.nodes = applyNodeChanges(changes, state.nodes);
      });
    },

    onEdgesChange: (changes: EdgeChange[]) => {
      set((state) => {
        state.edges = applyEdgeChanges(changes, state.edges);
      });
    },

    onConnect: (connection: Connection) => {
      set((state) => {
        state.edges = addEdge(connection, state.edges);
      });
    },

    updateNodeData: (nodeId: string, data: Record<string, unknown>) => {
      set((state) => {
        const nodeToUpdate = state.nodes.find((node) => node.id === nodeId);
        if (nodeToUpdate) {
          nodeToUpdate.data = { ...nodeToUpdate.data, ...data };
        }
      });
    },
  }))
);

export default useHarnessStore;
