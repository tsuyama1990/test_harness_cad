// frontend/src/components/ValidationReportPanel.tsx
import React, { useState } from 'react';
import Button from './ui/Button';
import Panel from './ui/Panel';

interface ValidationError {
  component_id: string;
  component_type: string;
  message: string;
  error_type: string;
}

interface ValidationReportPanelProps {
  harnessId: string;
}

const ValidationReportPanel: React.FC<ValidationReportPanelProps> = ({
  harnessId,
}) => {
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
    }
  };

  const handleExport = () => {
    window.location.href = `/api/v1/harnesses/${harnessId}/procurement/export-csv`;
  };

  return (
    <Panel data-testid="validation-report-panel">
      <div className="flex flex-col gap-4">
        <h3 className="text-lg font-semibold">Design Validation</h3>
        <Button onClick={handleValidate}>Run Validation</Button>
        {isValidated && (
          <div className="mt-4 flex flex-col gap-4">
            {isValidationSuccess ? (
              <div className="rounded-md bg-green-50 p-4 text-green-700">
                <p className="font-semibold">Validation Successful!</p>
                <p>No errors found in the harness design.</p>
              </div>
            ) : (
              <div className="rounded-md bg-red-50 p-4">
                <h4 className="mb-2 font-semibold text-red-800">
                  Validation Errors:
                </h4>
                <ul className="list-disc space-y-1 pl-5 text-red-700">
                  {errors.map((error, index) => (
                    <li key={index}>
                      <strong className="font-medium">{error.error_type}:</strong>{' '}
                      {error.message} (ID: {error.component_id})
                    </li>
                  ))}
                </ul>
              </div>
            )}
            <Button
              onClick={handleExport}
              disabled={!isValidationSuccess}
              variant="secondary"
            >
              Export Procurement CSV
            </Button>
          </div>
        )}
      </div>
    </Panel>
  );
};

export default ValidationReportPanel;
