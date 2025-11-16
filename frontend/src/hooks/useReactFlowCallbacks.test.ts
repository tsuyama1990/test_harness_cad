import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useReactFlowCallbacks } from './useReactFlowCallbacks';
import useHarnessStore from '../stores/useHarnessStore';
import type { StoreApi, UseBoundStore } from 'zustand';

// Mock the entire store
vi.mock('../stores/useHarnessStore');

const mockedUseHarnessStore = useHarnessStore as vi.Mocked<UseBoundStore<StoreApi<any>>>;

describe('useReactFlowCallbacks', () => {
  it('should return callback functions from the store', () => {
    const mockOnNodesChange = vi.fn();
    const mockOnEdgesChange = vi.fn();
    const mockOnConnect = vi.fn();

    // Set the return value for the mocked store
    mockedUseHarnessStore.mockImplementation((selector: (state: any) => any) => selector({
      onNodesChange: mockOnNodesChange,
      onEdgesChange: mockOnEdgesChange,
      onConnect: mockOnConnect,
    }));

    const { result } = renderHook(() => useReactFlowCallbacks());

    expect(result.current.onNodesChange).toBe(mockOnNodesChange);
    expect(result.current.onEdgesChange).toBe(mockOnEdgesChange);
    expect(result.current.onConnect).toBe(mockOnConnect);

    // Ensure the callbacks can be called
    act(() => {
      result.current.onNodesChange([]);
      result.current.onEdgesChange([]);
      result.current.onConnect({ source: 'a', target: 'b', sourceHandle: null, targetHandle: null });
    });

    expect(mockOnNodesChange).toHaveBeenCalledTimes(1);
    expect(mockOnEdgesChange).toHaveBeenCalledTimes(1);
    expect(mockOnConnect).toHaveBeenCalledTimes(1);
  });
});
