import React from 'react';
import { useStore, type Node, type Edge } from 'reactflow';
import useHarnessStore from '../stores/useHarnessStore';

const AttributeEditorPanel: React.FC = () => {
  const { updateNodeData, updateEdgeData } = useHarnessStore();
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

  const renderNodeEditor = (node: Node) => (
    <div>
      <h4>Connector Attributes</h4>
      <form>
        <label>ID:</label>
        <input type="text" value={node.data.id || ''} readOnly />
        <label>Manufacturer:</label>
        <input
          type="text"
          value={node.data.manufacturer || ''}
          onChange={(e) =>
            updateNodeData(node.id, { manufacturer: e.target.value })
          }
        />
        <label>Part Number:</label>
        <input
          type="text"
          value={node.data.part_number || ''}
          onChange={(e) =>
            updateNodeData(node.id, { part_number: e.target.value })
          }
        />
      </form>
    </div>
  );

  const renderEdgeEditor = (edge: Edge) => (
    <div>
      <h4>Wire Attributes</h4>
      <form>
        <label>Wire ID:</label>
        <input type="text" value={edge.data.wire_id || ''} readOnly />
        <label>Color:</label>
        <input
          type="text"
          value={edge.data.color || ''}
          onChange={(e) => updateEdgeData(edge.id, { color: e.target.value })}
        />
        <label>Strip Length (A):</label>
        <input
          type="text"
          value={edge.data.strip_length_a || ''}
          onChange={(e) =>
            updateEdgeData(edge.id, { strip_length_a: e.target.value })
          }
        />
        <label>Strip Length (B):</label>
        <input
          type="text"
          value={edge.data.strip_length_b || ''}
          onChange={(e) =>
            updateEdgeData(edge.id, { strip_length_b: e.target.value })
          }
        />
        <label>Terminal (A):</label>
        <input
          type="text"
          value={edge.data.terminal_part_number_a || ''}
          onChange={(e) =>
            updateEdgeData(edge.id, { terminal_part_number_a: e.target.value })
          }
        />
        <label>Terminal (B):</label>
        <input
          type="text"
          value={edge.data.terminal_part_number_b || ''}
          onChange={(e) =>
            updateEdgeData(edge.id, { terminal_part_number_b: e.target.value })
          }
        />
        <label>Marking (A):</label>
        <input
          type="text"
          value={edge.data.marking_text_a || ''}
          onChange={(e) =>
            updateEdgeData(edge.id, { marking_text_a: e.target.value })
          }
        />
        <label>Marking (B):</label>
        <input
          type="text"
          value={edge.data.marking_text_b || ''}
          onChange={(e) =>
            updateEdgeData(edge.id, { marking_text_b: e.target.value })
          }
        />
      </form>
    </div>
  );

  return (
    <aside className="attribute-editor-panel">
      <h3>Attribute Editor</h3>
      {selectedElement
        ? 'position' in selectedElement // Check if it's a Node
          ? renderNodeEditor(selectedElement)
          : renderEdgeEditor(selectedElement)
        : 'Select an element to edit its attributes.'}
    </aside>
  );
};

export default AttributeEditorPanel;
