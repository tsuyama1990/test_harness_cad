import React from 'react';
import { useStore, type Node, type Edge } from 'reactflow';
import useHarnessStore from '../stores/useHarnessStore';
import Input from './ui/Input'; // Import the new Input component
import Button from './ui/Button'; // Import the new Button component

const AttributeEditorPanel: React.FC = () => {
  const { updateNodeData, updateEdgeData, setViewMode, setSelectedEdgeId } =
    useHarnessStore();
  const selectedNodes = useStore((store) =>
    Array.from(store.nodeInternals.values()).filter((node) => node.selected)
  );
  const selectedEdges = useStore((store) =>
    Array.from(store.edges).filter((edge) => edge.selected)
  );

  const selectedElement =
    selectedNodes.length > 0
      ? selectedNodes[0]
      : selectedEdges.length > 0
        ? selectedEdges[0]
        : null;

  const FormField: React.FC<{ label: string; children: React.ReactNode }> = ({
    label,
    children,
  }) => (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      {children}
    </div>
  );

  const renderNodeEditor = (node: Node) => (
    <div>
      <h4 className="text-lg font-semibold mb-4">Connector Attributes</h4>
      <form>
        <FormField label="ID:">
          <Input type="text" value={node.data.id || ''} readOnly />
        </FormField>
        <FormField label="Manufacturer:">
          <Input
            type="text"
            value={node.data.manufacturer || ''}
            onChange={(e) =>
              updateNodeData(node.id, { manufacturer: e.target.value })
            }
          />
        </FormField>
        <FormField label="Part Number:">
          <Input
            type="text"
            value={node.data.part_number || ''}
            onChange={(e) =>
              updateNodeData(node.id, { part_number: e.target.value })
            }
          />
        </FormField>
      </form>
    </div>
  );

  const renderEdgeEditor = (
    edge: Edge,
    setViewMode: (mode: '2D' | '3D') => void,
    setSelectedEdgeId: (edgeId: string | null) => void
  ) => {
    const handleMeasureClick = () => {
      setSelectedEdgeId(edge.id);
      setViewMode('3D');
    };

    return (
      <div>
        <div className="flex justify-between items-center mb-4">
          <h4 className="text-lg font-semibold">Wire Attributes</h4>
          <Button onClick={handleMeasureClick} variant="primary">
            Measure 3D
          </Button>
        </div>
        <form>
          <FormField label="Wire ID:">
            <Input type="text" value={edge.data.wire_id || ''} readOnly />
          </FormField>
          <FormField label="Color:">
            <Input
              type="text"
              value={edge.data.color || ''}
              onChange={(e) =>
                updateEdgeData(edge.id, { color: e.target.value })
              }
            />
          </FormField>
          <FormField label="Strip Length (A):">
            <Input
              type="text"
              value={edge.data.strip_length_a || ''}
              onChange={(e) =>
                updateEdgeData(edge.id, { strip_length_a: e.target.value })
              }
            />
          </FormField>
          <FormField label="Strip Length (B):">
            <Input
              type="text"
              value={edge.data.strip_length_b || ''}
              onChange={(e) =>
                updateEdgeData(edge.id, { strip_length_b: e.target.value })
              }
            />
          </FormField>
          <FormField label="Terminal (A):">
            <Input
              type="text"
              value={edge.data.terminal_part_number_a || ''}
              onChange={(e) =>
                updateEdgeData(edge.id, {
                  terminal_part_number_a: e.target.value,
                })
              }
            />
          </FormField>
          <FormField label="Terminal (B):">
            <Input
              type="text"
              value={edge.data.terminal_part_number_b || ''}
              onChange={(e) =>
                updateEdgeData(edge.id, {
                  terminal_part_number_b: e.target.value,
                })
              }
            />
          </FormField>
          <FormField label="Marking (A):">
            <Input
              type="text"
              value={edge.data.marking_text_a || ''}
              onChange={(e) =>
                updateEdgeData(edge.id, { marking_text_a: e.target.value })
              }
            />
          </FormField>
          <FormField label="Marking (B):">
            <Input
              type="text"
              value={edge.data.marking_text_b || ''}
              onChange={(e) =>
                updateEdgeData(edge.id, { marking_text_b: e.target.value })
              }
            />
          </FormField>
        </form>
      </div>
    );
  };

  return (
    <aside className="w-96 bg-surface p-4 border-l-4 border-pixel-border overflow-y-auto">
      <h3 className="text-xl font-pixel font-bold mb-4 text-white uppercase tracking-wider">Attribute Editor</h3>
      {selectedElement
        ? 'position' in selectedElement // Check if it's a Node
          ? renderNodeEditor(selectedElement)
          : renderEdgeEditor(selectedElement, setViewMode, setSelectedEdgeId)
        : <p className="text-gray-500">Select an element to edit its attributes.</p>}
    </aside>
  );
};

export default AttributeEditorPanel;
