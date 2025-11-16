import { useCallback } from 'react';
import { useReactFlow } from 'reactflow';
import useHarnessStore from '../stores/useHarnessStore';

export const useReactFlowDnD = () => {
  const { screenToFlowPosition } = useReactFlow();
  const { nodes, setNodes } = useHarnessStore();

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow-type');
      const data = JSON.parse(event.dataTransfer.getData('application/reactflow-data'));

      // check if the dropped element is valid
      if (typeof type === 'undefined' || !type) {
        return;
      }

      const position = screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const newNode = {
        id: `${data.name}-${+new Date()}`,
        type: 'customConnector',
        position,
        data: {
          label: data.name,
          part_number: data.part_number,
          pins: data.pins,
        },
      };

      setNodes([...nodes, newNode]);
    },
    [screenToFlowPosition, nodes, setNodes]
  );

  return { onDragOver, onDrop };
};
