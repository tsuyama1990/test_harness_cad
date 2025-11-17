// frontend/src/components/ValidationReportPanel.tsx
import React, { useState } from 'react';

interface ValidationError {
  component_id: string;
  component_type: string;
  message: string;
  error_type: string;
}

interface ValidationReportPanelProps {
  harnessId: string; // Assuming we have the harness ID
}

const ValidationReportPanel: React.FC<ValidationReportPanelProps> = ({ harnessId }) => {
  const [errors, setErrors] = useState<ValidationError[]>([]);
  const [isValidated, setIsValidated] = useState(false);
  const [isValidationSuccess, setIsValidationSuccess] = useState(false);

  const handleValidate = async () => {
    try {
      const response = await fetch(`/api/v1/harnesses/${harnessId}/validate`);
      const data: ValidationError[] = await response.json();
      setErrors(data);
      setIsValidated(true);
      setIsValidationSuccess(data.length === 0);
    } catch (error) {
      console.error('Validation failed:', error);
      // You might want to show a generic error message to the user
    }
  };

  const handleExport = () => {
    // This will trigger the file download
    window.location.href = `/api/v1/harnesses/${harnessId}/procurement/export-csv`;
  };

  return (
    <div className="validation-panel">
      <h3>Design Validation</h3>
      <button onClick={handleValidate}>Run Validation</button>
      {isValidated && (
        <>
          {isValidationSuccess ? (
            <div className="success-message">Validation successful!</div>
          ) : (
            <div className="error-list">
              <h4>Validation Errors:</h4>
              <ul>
                {errors.map((error, index) => (
                  <li key={index}>
                    <strong>{error.error_type}:</strong> {error.message}
                  </li>
                ))}
              </ul>
            </div>
          )}
          <button onClick={handleExport} disabled={!isValidationSuccess}>
            Export Procurement CSV
          </button>
        </>
      )}
    </div>
  );
};

export default ValidationReportPanel;
