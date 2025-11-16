import { useEffect } from 'react';
import useHarnessStore from '../stores/useHarnessStore';
import { updateHarness } from '../services/api';
import { transformFlowToHarness } from '../utils/dataTransformer';
import debounce from 'lodash/debounce.js';

// It's crucial to define the debounced function *outside* the hook
// to prevent it from being recreated on every render.
const debouncedUpdateHarness = debounce(
  (harnessId: string, harnessData) => {
    updateHarness(harnessId, harnessData);
  },
  500 // 500ms delay
);

export const useHarnessSync = () => {
  const { nodes, edges, harnessId } = useHarnessStore((state) => ({
    nodes: state.nodes,
    edges: state.edges,
    harnessId: state.harnessId,
  }));

  useEffect(() => {
    // This effect listens for changes in nodes or edges and triggers the sync.
    if (harnessId && (nodes.length > 0 || edges.length > 0)) {
      const harnessData = transformFlowToHarness(nodes, edges);
      debouncedUpdateHarness(harnessId, harnessData);
    }

    // Cleanup function to cancel any pending debounced calls when the component unmounts.
    return () => {
      debouncedUpdateHarness.cancel();
    };
  }, [nodes, edges, harnessId]); // Dependencies array ensures this runs only when data changes.
};
