import { useEffect } from 'react';
import useHarnessStore from '../stores/useHarnessStore';
import { getHarness } from '../services/api';
import { transformHarnessToFlow } from '../utils/dataTransformer';

export const useHarnessData = (harnessId: string) => {
  const { setInitialData, setHarnessId } = useHarnessStore();

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
};
