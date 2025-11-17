import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import AttributeEditorPanel from './AttributeEditorPanel';
import useHarnessStore from '../stores/useHarnessStore';

// Mock the useStore hook from reactflow
vi.mock('reactflow', () => ({
  ...vi.importActual('reactflow'),
  useStore: vi.fn(),
}));

describe('AttributeEditorPanel', () => {
  it('renders wire attributes when an edge is selected', () => {
    // Mock the Zustand store state
    useHarnessStore.setState({
      nodes: [],
      edges: [
        {
          id: 'edge-1',
          source: 'node-1',
          target: 'node-2',
          selected: true,
          data: {
            wire_id: 'W-001',
            color: 'blue',
            strip_length_a: '5',
            terminal_part_number_a: 'TERM-A',
            marking_text_a: 'W-001-A',
          },
        },
      ],
      updateEdgeData: vi.fn(),
      updateNodeData: vi.fn(),
    });

    render(<AttributeEditorPanel />);

    expect(screen.getByLabelText('Wire ID:')).toHaveValue('W-001');
    expect(screen.getByLabelText('Color:')).toHaveValue('blue');
    expect(screen.getByLabelText('Strip Length (A):')).toHaveValue('5');
    expect(screen.getByLabelText('Terminal (A):')).toHaveValue('TERM-A');
    expect(screen.getByLabelText('Marking (A):')).toHaveValue('W-001-A');
  });
});
