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
  const pinHeight = 20;
  const totalHeight = data.pins.length * pinHeight + 40;

  return (
    <div
      style={{
        border: '1px solid #777',
        padding: '10px',
        borderRadius: '5px',
        background: 'white',
        width: 150,
        height: totalHeight,
      }}
    >
      <div style={{ textAlign: 'center', fontWeight: 'bold' }}>{data.label}</div>
      <div style={{ textAlign: 'center', fontSize: '10px', color: '#666' }}>
        {data.part_number}
      </div>
      <div style={{ marginTop: '10px' }}>
        {data.pins.map((pin, index) => (
          <div
            key={pin.id}
            style={{
              position: 'relative',
              height: `${pinHeight}px`,
              display: 'flex',
              alignItems: 'center',
            }}
          >
            <Handle
              type="source"
              position={Position.Right}
              id={pin.id}
              style={{ top: `${index * pinHeight + 25}px` }}
            />
            <span style={{ fontSize: '12px' }}>{pin.id}</span>
            <Handle
              type="target"
              position={Position.Left}
              id={pin.id}
              style={{ top: `${index * pinHeight + 25}px` }}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default CustomConnectorNode;
