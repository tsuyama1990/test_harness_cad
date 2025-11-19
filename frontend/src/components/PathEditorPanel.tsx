import React from 'react';
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
      <div className="absolute top-4 right-4 w-64 bg-white/90 backdrop-blur-md shadow-lg rounded-xl p-4 border border-gray-200">
        <p className="text-sm text-gray-600">
          Select a wire in the 2D view to start routing.
        </p>
      </div>
    );
  }

  return (
    <div className="absolute top-4 right-4 w-64 bg-white/90 backdrop-blur-md shadow-lg rounded-xl p-4 border border-gray-200">
      <h3 className="text-lg font-bold mb-3 text-gray-800">Wire Path Editor</h3>

      <div className="bg-gray-50 rounded-md p-3 mb-3 text-sm space-y-1">
        <div className="flex justify-between items-center">
          <span className="text-gray-500">Wire ID</span>
          <div className="flex items-center gap-2">
            <div
              className="w-4 h-4 rounded-sm border border-gray-400"
              style={{ backgroundColor: wireColor }}
            ></div>
            <span className="font-mono text-gray-800">{selectedEdgeId}</span>
          </div>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-500">Length</span>
          <span className="font-mono text-gray-800">
            {pathLength.toFixed(2)} mm
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-500">Total Length</span>
          <span className="font-mono text-gray-800">
            {totalLength.toFixed(2)} mm
          </span>
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1 text-gray-600">
          Manufacturing Margin
        </label>
        <Input
          type="number"
          value={manufacturingMargin}
          onChange={(e) => setManufacturingMargin(parseFloat(e.target.value))}
          step="0.01"
          min="1"
        />
      </div>

      <div className="flex gap-2">
        <Button onClick={onUndo} variant="secondary" className="flex-1">
          Undo
        </Button>
        <Button onClick={onClear} variant="outline" className="flex-1">
          Clear
        </Button>
        <Button onClick={onSave} variant="primary" className="flex-1">
          Save
        </Button>
      </div>
    </div>
  );
};

export default PathEditorPanel;
