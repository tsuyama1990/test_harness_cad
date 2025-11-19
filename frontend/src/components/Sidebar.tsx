import React, { useEffect, useState } from 'react';
import { getComponents, type LibraryComponent } from '../services/api';
import useHarnessStore from '../stores/useHarnessStore';
import { API_BASE_URL } from '../services/api';
import Button from './ui/Button'; // Import the new Button component

const Sidebar: React.FC = () => {
  const [components, setComponents] = useState<LibraryComponent[]>([]);
  const { harnessId } = useHarnessStore();

  useEffect(() => {
    const fetchComponents = async () => {
      try {
        const componentList = await getComponents();
        setComponents(componentList);
      } catch (error) {
        console.error('Failed to fetch components:', error);
      }
    };
    fetchComponents();
  }, []);

  const onDragStart = (event: React.DragEvent, component: LibraryComponent) => {
    event.dataTransfer.setData('application/reactflow-type', 'customConnector');
    event.dataTransfer.setData('application/reactflow-data', JSON.stringify(component.data));
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <aside
      className="w-64 bg-surface p-4 border-r border-gray-200 flex flex-col"
      data-testid="sidebar"
    >
      <h3 className="text-lg font-semibold mb-4">Component Library</h3>
      <div className="flex-grow">
        {components
          .filter((c) => c.type === 'connector')
          .map((component) => (
            <div
              key={component.id}
              className="p-2 mb-2 border rounded cursor-grab bg-white shadow-sm hover:shadow-md transition-shadow"
              onDragStart={(event) => onDragStart(event, component)}
              draggable
              data-testid={`component-${component.name}`}
            >
              {component.name}
            </div>
          ))}
      </div>
      <div className="flex flex-col space-y-2">
        <h3 className="text-lg font-semibold mb-2">Exports</h3>
        <Button
          onClick={() =>
            window.open(
              `${API_BASE_URL}/harnesses/${harnessId}/strip-list`,
              '_blank'
            )
          }
          disabled={!harnessId}
          variant="secondary"
        >
          Strip List (CSV)
        </Button>
        <Button
          onClick={() =>
            window.open(
              `${API_BASE_URL}/harnesses/${harnessId}/mark-tube-list`,
              '_blank'
            )
          }
          disabled={!harnessId}
          variant="secondary"
        >
          Mark Tube List (CSV)
        </Button>
        <Button
          onClick={() =>
            window.open(
              `${API_BASE_URL}/harnesses/${harnessId}/formboard-pdf`,
              '_blank'
            )
          }
          disabled={!harnessId}
          variant="secondary"
        >
          Formboard (PDF)
        </Button>
        <Button
          onClick={() => {
            const scale = prompt('Enter scale factor:', '1.0');
            if (scale) {
              window.open(
                `${API_BASE_URL}/harnesses/${harnessId}/jig-dxf?scale=${scale}`,
                '_blank'
              );
            }
          }}
          disabled={!harnessId}
          variant="secondary"
        >
          Jig (DXF)
        </Button>
      </div>
    </aside>
  );
};

export default Sidebar;
