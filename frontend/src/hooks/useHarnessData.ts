import { useEffect, useState } from 'react';
import { getHarness } from '../services/api';
import useHarnessStore from '../stores/useHarnessStore';
import { transformHarnessToFlow } from '../utils/dataTransformer';

export const useHarnessData = (harnessId: string) => {
  const setInitialState = useHarnessStore((state) => state.setInitialState);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchHarnessData = async () => {
      try {
        setLoading(true);
        const harnessData = await getHarness(harnessId);
        const { nodes, edges } = transformHarnessToFlow(harnessData);
        setInitialState(harnessId, nodes, edges);
        setError(null);
      } catch (e) {
        setError(e as Error);
      } finally {
        setLoading(false);
      }
    };

    if (harnessId) {
      fetchHarnessData();
    }
  }, [harnessId, setInitialState]);

  return { loading, error };
};
