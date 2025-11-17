import React, { useEffect, useState } from 'react';
import { getComponents, type LibraryComponent } from '../services/api';
import useHarnessStore from '../stores/useHarnessStore';
import { API_BASE_URL } from '../services/api';

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
    <aside className="sidebar" data-testid="sidebar">
      <h3>Component Library</h3>
      {components
        .filter((c) => c.type === 'connector')
        .map((component) => (
          <div
            key={component.id}
            className="sidebar-component"
            onDragStart={(event) => onDragStart(event, component)}
            draggable
            data-testid={`component-${component.name}`}
          >
            {component.name}
          </div>
        ))}
      <div className="sidebar-section">
        <h3>Exports</h3>
        <button
          onClick={() =>
            window.open(
              `${API_BASE_URL}/harnesses/${harnessId}/strip-list`,
              '_blank'
            )
          }
          disabled={!harnessId}
        >
          Export Strip List (CSV)
        </button>
        <button
          onClick={() =>
            window.open(
              `${API_BASE_URL}/harnesses/${harnessId}/mark-tube-list`,
              '_blank'
            )
          }
          disabled={!harnessId}
        >
          Export Mark Tube List (CSV)
        </button>
        <button
          onClick={() =>
            window.open(
              `${API_BASE_URL}/harnesses/${harnessId}/formboard-pdf`,
              '_blank'
            )
          }
          disabled={!harnessId}
        >
          Export Formboard (PDF)
        </button>
        <button
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
        >
          Export Jig (DXF)
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
