import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useHarnessData } from './useHarnessData';
import useHarnessStore from '../stores/useHarnessStore';
import { getHarness } from '../services/api';
import { transformHarnessToFlow } from '../utils/dataTransformer';
import type { StoreApi, UseBoundStore } from 'zustand';

// Mock dependencies
vi.mock('../stores/useHarnessStore');
vi.mock('../services/api');
vi.mock('../utils/dataTransformer');

// Type assertion for the mocked store
const mockedUseHarnessStore = useHarnessStore as vi.Mocked<UseBoundStore<StoreApi<any>>>;

describe('useHarnessData', () => {
  const mockSetInitialState = vi.fn();
  const harnessId = 'test-harness-id';

  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();
    // Setup the mock store implementation for each test
    mockedUseHarnessStore.mockImplementation((selector: (state: any) => any) => selector({
      setInitialState: mockSetInitialState,
    }));
  });

  it('should fetch harness data, transform it, and set the initial state', async () => {
    const mockApiData = { id: harnessId, name: 'Test Harness', connectors: [], wires: [], connections: [] };
    const mockFlowData = { nodes: [{ id: '1', data: {}, position: { x: 0, y: 0 } }], edges: [] };

    (getHarness as vi.Mock).mockResolvedValue(mockApiData);
    (transformHarnessToFlow as vi.Mock).mockReturnValue(mockFlowData);

    const { result } = renderHook(() => useHarnessData(harnessId));

    // Initially, it should be loading
    expect(result.current.loading).toBe(true);

    // Wait for the async operations to complete
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    // Verify that the correct functions were called
    expect(getHarness).toHaveBeenCalledWith(harnessId);
    expect(transformHarnessToFlow).toHaveBeenCalledWith(mockApiData);
    expect(mockSetInitialState).toHaveBeenCalledWith(
      harnessId,
      mockFlowData.nodes,
      mockFlowData.edges
    );
    expect(result.current.error).toBeNull();
  });

  it('should handle errors during data fetching', async () => {
    const mockError = new Error('Failed to fetch');
    (getHarness as vi.Mock).mockRejectedValue(mockError);

    const { result } = renderHook(() => useHarnessData(harnessId));

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(getHarness).toHaveBeenCalledWith(harnessId);
    expect(transformHarnessToFlow).not.toHaveBeenCalled();
    expect(mockSetInitialState).not.toHaveBeenCalled();
    expect(result.current.error).toBe(mockError);
  });
});
