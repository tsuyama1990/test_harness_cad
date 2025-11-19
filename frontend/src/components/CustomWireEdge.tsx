import React from 'react';
import { getBezierPath, EdgeLabelRenderer, BaseEdge } from 'reactflow';
import type { Position } from 'reactflow';

interface CustomWireEdgeProps {
  id: string;
  sourceX: number;
  sourceY: number;
  targetX: number;
  targetY: number;
  sourcePosition: Position;
  targetPosition: Position;
  style?: React.CSSProperties;
  data?: {
    color: string;
    wire_id: string;
  };
}

const CustomWireEdge: React.FC<CustomWireEdgeProps> = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
}) => {
  if (!data) {
    return null;
  }

  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  return (
    <>
      <BaseEdge
        path={edgePath}
        style={{ stroke: data.color, strokeWidth: 2 }}
        id={id}
      />
      <EdgeLabelRenderer>
        <div
          style={{
            position: 'absolute',
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            pointerEvents: 'all',
          }}
          className="nodrag nopan bg-yellow-100 text-yellow-800 border border-yellow-300 text-[10px] font-mono px-1.5 py-0.5 rounded shadow-sm hover:scale-110 transition-transform cursor-pointer"
        >
          {data.wire_id}
        </div>
      </EdgeLabelRenderer>
    </>
  );
};

export default CustomWireEdge;
