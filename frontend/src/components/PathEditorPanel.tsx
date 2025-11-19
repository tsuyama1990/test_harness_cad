import React from 'react';
import Panel from './ui/Panel';
import Input from './ui/Input';
import Button from './ui/Button';

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
      <div className="absolute top-4 left-4 bg-gray-900 bg-opacity-70 text-white p-4 rounded-lg shadow-lg">
        <p>Select a wire in the 2D view to start routing.</p>
      </div>
    );
  }

  return (
    <Panel className="absolute top-4 left-4 w-64 bg-opacity-90 backdrop-blur-sm">
      <h3 className="text-lg font-semibold mb-3 pb-2 border-b border-gray-200">
        Wire Path Editor
      </h3>

      <div className="mb-3">
        <strong className="text-sm font-medium">Selected Wire:</strong>
        <div className="flex items-center mt-1">
          <div
            className="w-4 h-4 rounded-sm border border-gray-400 mr-2"
            style={{ backgroundColor: wireColor }}
          ></div>
          <span className="text-sm font-mono">{selectedEdgeId}</span>
        </div>
      </div>

      <div className="mb-2 text-sm">
        <strong>Path Length:</strong> {pathLength.toFixed(2)} mm
      </div>

      <div className="mb-4 text-sm">
        <strong>Total Length (incl. Margin):</strong> {totalLength.toFixed(2)} mm
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">
          Manufacturing Margin:
        </label>
        <Input
          type="number"
          value={manufacturingMargin}
          onChange={(e) => setManufacturingMargin(parseFloat(e.target.value))}
          step="0.01"
          min="1"
        />
      </div>

      <div className="flex justify-between gap-2 mb-2">
        <Button onClick={onUndo} variant="secondary" className="flex-1">
          Undo
        </Button>
        <Button onClick={onClear} variant="outline" className="flex-1">
          Clear
        </Button>
      </div>

      <Button onClick={onSave} variant="primary" className="w-full">
        Save Path
      </Button>
    </Panel>
  );
};

export default PathEditorPanel;
