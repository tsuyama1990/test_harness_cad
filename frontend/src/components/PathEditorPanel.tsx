// frontend/src/components/PathEditorPanel.tsx
import React from 'react';

interface PathEditorPanelProps {
  selectedEdgeId: string | null;
  wireColor: string;
  pathLength: number;
  totalLength: number;
  manufacturingMargin: number;
  setManufacturingMargin: (margin: number) => void;
  onSave: () => void;
  onUndo: () => void;
  onClear: () => void;
}

const PathEditorPanel: React.FC<PathEditorPanelProps> = ({
  selectedEdgeId,
  wireColor,
  pathLength,
  totalLength,
  manufacturingMargin,
  setManufacturingMargin,
  onSave,
  onUndo,
  onClear,
}) => {
  if (!selectedEdgeId) {
    return (
      <div
        style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          background: 'rgba(0, 0, 0, 0.6)',
          color: 'white',
          padding: '15px',
          borderRadius: '10px',
        }}
      >
        <p>Select a wire in the 2D view to start routing.</p>
      </div>
    );
  }

  return (
    <div
      style={{
        position: 'absolute',
        top: '20px',
        left: '20px',
        background: 'rgba(255, 255, 255, 0.8)',
        padding: '15px',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
        fontFamily: 'sans-serif',
        color: '#333',
        width: '240px',
        zIndex: 1000,
      }}
    >
      <h3
        style={{
          marginTop: 0,
          marginBottom: '15px',
          borderBottom: '1px solid #ddd',
          paddingBottom: '10px',
        }}
      >
        Wire Path Editor
      </h3>

      <div style={{ marginBottom: '10px' }}>
        <strong>Selected Wire:</strong>
        <div style={{ display: 'flex', alignItems: 'center', marginTop: '5px' }}>
          <div
            style={{
              width: '16px',
              height: '16px',
              backgroundColor: wireColor,
              marginRight: '8px',
              borderRadius: '3px',
              border: '1px solid #888',
            }}
          ></div>
          <span>ID: {selectedEdgeId}</span>
        </div>
      </div>

      <div style={{ marginBottom: '10px' }}>
        <strong>Path Length:</strong> {pathLength.toFixed(2)} mm
      </div>

      <div style={{ marginBottom: '15px' }}>
        <strong>Total Length (incl. Margin):</strong> {totalLength.toFixed(2)} mm
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>
          Manufacturing Margin:
        </label>
        <input
          type="number"
          value={manufacturingMargin}
          onChange={(e) => setManufacturingMargin(parseFloat(e.target.value))}
          step="0.01"
          min="1"
          style={{ width: '100%', padding: '5px', boxSizing: 'border-box' }}
        />
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', gap: '5px' }}>
        <button
          onClick={onUndo}
          style={{ flex: 1, padding: '8px', cursor: 'pointer' }}
        >
          Undo
        </button>
        <button
          onClick={onClear}
          style={{ flex: 1, padding: '8px', cursor: 'pointer' }}
        >
          Clear
        </button>
      </div>

      <button
        onClick={onSave}
        style={{
          width: '100%',
          padding: '10px',
          marginTop: '10px',
          background: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        Save Path
      </button>
    </div>
  );
};

export default PathEditorPanel;
