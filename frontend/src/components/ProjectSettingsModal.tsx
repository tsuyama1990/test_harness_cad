// frontend/src/components/ProjectSettingsModal.tsx
import React, { useState } from 'react';

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
    <div className="modal">
      <div className="modal-content">
        <h2>Project Settings</h2>
        <label>
          System Voltage:
          <input
            type="number"
            value={voltage}
            onChange={(e) => setVoltage(parseFloat(e.target.value))}
          />
        </label>
        <label>
          <input
            type="checkbox"
            checked={rohs}
            onChange={(e) => setRohs(e.target.checked)}
          />
          Require RoHS Compliance
        </label>
        <div className="modal-actions">
          <button onClick={handleSave}>Save</button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default ProjectSettingsModal;
