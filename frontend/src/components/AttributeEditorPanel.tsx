import React from 'react';

const AttributeEditorPanel: React.FC = () => {
  // This is a placeholder for the attribute editor.
  // In a real application, you would use the selected element from the store
  // to show a form and edit its properties.

  // const { selectedElement, updateNodeData } = useHarnessStore();

  return (
    <aside className="attribute-editor-panel">
      <h3>Attribute Editor</h3>
      {/*
      Example of what would be here:
      if (selectedElement) {
        <form>
          <label>Label</label>
          <input
            value={selectedElement.data.label}
            onChange={(e) => updateNodeData(selectedElement.id, { label: e.target.value })}
          />
        </form>
      }
      */}
      <p>Select an element to edit its attributes.</p>
    </aside>
  );
};

export default AttributeEditorPanel;
