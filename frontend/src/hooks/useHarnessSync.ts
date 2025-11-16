import { useEffect, useRef } from 'react';
import { debounce } from 'lodash';
import useHarnessStore from '../stores/useHarnessStore';
import { updateHarness } from '../services/api';
import { transformFlowToHarness, type HarnessData } from '../utils/dataTransformer';

// Debounced function to update harness data on the backend
const debouncedUpdateHarness = debounce(
  (harnessId: string, harnessData: HarnessData) => {
    updateHarness(harnessId, harnessData);
  },
  500
);

export const useHarnessSync = () => {
  const { nodes, edges, harnessId } = useHarnessStore();
  const isInitialLoad = useRef(true);

  useEffect(() => {
    // Skip the first effect call, which happens on initial load
    if (isInitialLoad.current) {
      isInitialLoad.current = false;
      return;
    }

    if (harnessId && nodes.length > 0) {
      const harnessData = transformFlowToHarness(nodes, edges);
      debouncedUpdateHarness(harnessId, harnessData);
    }
  }, [nodes, edges, harnessId]);
};
