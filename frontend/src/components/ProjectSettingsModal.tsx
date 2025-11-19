// frontend/src/components/ProjectSettingsModal.tsx
import React, { useState } from 'react';
import Button from './ui/Button';
import Input from './ui/Input';
import Panel from './ui/Panel';

interface ProjectSettings {
  system_voltage: number;
  require_rohs: boolean;
}

interface ProjectSettingsModalProps {
  onSave: (settings: ProjectSettings) => void;
  onClose: () => void;
  initialSettings: ProjectSettings;
}

const ProjectSettingsModal: React.FC<ProjectSettingsModalProps> = ({
  onSave,
  onClose,
  initialSettings,
}) => {
  const [voltage, setVoltage] = useState(initialSettings.system_voltage);
  const [rohs, setRohs] = useState(initialSettings.require_rohs);

  const handleSave = () => {
    onSave({
      system_voltage: voltage,
      require_rohs: rohs,
    });
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      data-testid="project-settings-modal"
    >
      <Panel className="w-full max-w-md">
        <div className="flex flex-col gap-4">
          <h2 className="text-lg font-semibold">Project Settings</h2>
          <div className="flex flex-col gap-2">
            <label htmlFor="system-voltage" className="font-medium">
              System Voltage:
            </label>
            <Input
              id="system-voltage"
              type="number"
              value={voltage}
              onChange={(e) => setVoltage(parseFloat(e.target.value))}
            />
          </div>
          <div className="flex items-center gap-2">
            <Input
              id="rohs-compliance"
              type="checkbox"
              checked={rohs}
              onChange={(e) => setRohs(e.target.checked)}
              className="h-4 w-4"
            />
            <label htmlFor="rohs-compliance">Require RoHS Compliance</label>
          </div>
          <div className="mt-2 flex justify-end gap-2">
            <Button onClick={handleSave} variant="primary">
              Save
            </Button>
            <Button onClick={onClose} variant="secondary">
              Cancel
            </Button>
          </div>
        </div>
      </Panel>
    </div>
  );
};

export default ProjectSettingsModal;
