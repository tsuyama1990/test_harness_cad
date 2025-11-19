import React from 'react';
import { Handle, Position } from 'reactflow';

interface Pin {
  id: string;
}

interface CustomConnectorNodeProps {
  data: {
    label: string;
    part_number: string;
    pins: Pin[];
  };
}

const CustomConnectorNode: React.FC<CustomConnectorNodeProps> = ({ data }) => {
  return (
    <div className="w-32 bg-white shadow-md rounded-md border border-gray-300 hover:ring-2 hover:ring-blue-400 transition-all">
      <div className="px-3 py-1 bg-gray-100 border-b border-gray-300 rounded-t-md">
        <div className="font-bold text-xs text-center text-gray-800">
          {data.label}
        </div>
        <div className="text-[10px] text-center text-gray-500">
          {data.part_number}
        </div>
      </div>
      <div className="py-1">
        {data.pins.map((pin) => (
          <div
            key={pin.id}
            className="flex items-center justify-between px-3 h-6 hover:bg-gray-50"
          >
            <Handle
              type="target"
              position={Position.Left}
              id={pin.id}
              className="!bg-gray-400"
              data-testid={`handle-target-${data.label}-${pin.id}`}
            />
            <span className="font-mono text-xs text-gray-500">{pin.id}</span>
            <Handle
              type="source"
              position={Position.Right}
              id={pin.id}
              className="!bg-gray-400"
              data-testid={`handle-source-${data.label}-${pin.id}`}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default CustomConnectorNode;
