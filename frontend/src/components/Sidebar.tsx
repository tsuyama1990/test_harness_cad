import React, { useEffect, useState } from 'react';
import { getComponents, type LibraryComponent } from '../services/api';
import useHarnessStore from '../stores/useHarnessStore';
import { API_BASE_URL } from '../services/api';
import Button from './ui/Button'; // Import the new Button component

import WizardModal from './WizardModal';

const Sidebar: React.FC = () => {
  const [components, setComponents] = useState<LibraryComponent[]>([]);
  const [isWizardOpen, setIsWizardOpen] = useState(false);
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
    <>
      <aside
        className="w-64 bg-surface p-4 border-r-4 border-pixel-border flex flex-col"
        data-testid="sidebar"
      >
        <h3 className="text-xl font-pixel font-bold mb-4 text-white uppercase tracking-wider">Component Library</h3>

        <div className="mb-4">
          <Button onClick={() => setIsWizardOpen(true)} className="w-full mb-2">
            Start Wizard
          </Button>
        </div>

        <div className="flex-grow">
          {components
            .filter((c) => c.type === 'connector')
            .map((component) => (
              <div
                key={component.id}
                className="cursor-grab bg-white text-black font-pixel border-2 border-pixel-border p-3 shadow-pixel-sm hover:shadow-pixel hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all mb-3"
                onDragStart={(event) => onDragStart(event, component)}
                draggable
                data-testid={`component-${component.name}`}
              >
                {component.name}
              </div>
            ))}
        </div>
        <div className="flex flex-col space-y-3">
          <h3 className="text-xl font-pixel font-bold mb-2 text-white uppercase tracking-wider">Exports</h3>
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
      <WizardModal isOpen={isWizardOpen} onClose={() => setIsWizardOpen(false)} />
    </>
  );
};

export default Sidebar;
