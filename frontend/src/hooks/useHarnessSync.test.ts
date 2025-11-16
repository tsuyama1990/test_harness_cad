import { renderHook } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useHarnessSync } from './useHarnessSync';
import useHarnessStore from '../stores/useHarnessStore';
import { transformFlowToHarness } from '../utils/dataTransformer';
import debounce from 'lodash/debounce.js';
import { StoreApi, UseBoundStore } from 'zustand';

// Mock dependencies
vi.mock('../stores/useHarnessStore');
vi.mock('../services/api');
vi.mock('../utils/dataTransformer');
vi.mock('lodash/debounce.js', () => ({
  default: vi.fn((fn) => {
    const debouncedFn = vi.fn(fn);
    (debouncedFn as any).cancel = vi.fn();
    return debouncedFn;
  }),
}));

const debouncedUpdateHarnessMock = (debounce as vi.Mock).mock.results[0].value;
const mockedUseHarnessStore = useHarnessStore as vi.Mocked<UseBoundStore<StoreApi<any>>>;

describe('useHarnessSync', () => {
    const harnessId = 'test-harness-id';
    const initialNodes = [{ id: '1', data: {}, position: { x: 0, y: 0 } }];
    const initialEdges: any[] = [];
    const mockHarnessData = { name: 'Test', connectors: [], wires: [], connections: [] };

    beforeEach(() => {
        vi.clearAllMocks();
        (transformFlowToHarness as vi.Mock).mockReturnValue(mockHarnessData);
        // Reset the mock implementation for each test
        mockedUseHarnessStore.mockImplementation((selector: (state: any) => any) => selector({
            nodes: initialNodes,
            edges: initialEdges,
            harnessId: harnessId,
        }));
    });

    it('should call debouncedUpdateHarness when nodes or edges change', () => {
        const { rerender } = renderHook(() => useHarnessSync());

        expect(debouncedUpdateHarnessMock).toHaveBeenCalledWith(harnessId, mockHarnessData);
        expect(debouncedUpdateHarnessMock).toHaveBeenCalledTimes(1);

        rerender();
        expect(debouncedUpdateHarnessMock).toHaveBeenCalledTimes(1);

        const newNodes = [...initialNodes, { id: '2', data: {}, position: { x: 10, y: 10 } }];
        mockedUseHarnessStore.mockImplementation((selector: (state: any) => any) => selector({
            nodes: newNodes,
            edges: initialEdges,
            harnessId: harnessId,
        }));

        rerender();

        expect(transformFlowToHarness).toHaveBeenCalledWith(newNodes, initialEdges);
        expect(debouncedUpdateHarnessMock).toHaveBeenCalledWith(harnessId, mockHarnessData);
        expect(debouncedUpdateHarnessMock).toHaveBeenCalledTimes(2);
    });

    it('should not call debouncedUpdateHarness if harnessId is null', () => {
        mockedUseHarnessStore.mockImplementation((selector: (state: any) => any) => selector({
            nodes: initialNodes,
            edges: initialEdges,
            harnessId: null,
        }));

        renderHook(() => useHarnessSync());

        expect(debouncedUpdateHarnessMock).not.toHaveBeenCalled();
    });

    it('should call cancel on the debounced function on unmount', () => {
        const { unmount } = renderHook(() => useHarnessSync());
        unmount();
        expect((debouncedUpdateHarnessMock as any).cancel).toHaveBeenCalledTimes(1);
    });
});
