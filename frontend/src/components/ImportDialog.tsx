// frontend/src/components/ImportDialog.tsx
import React, { useState } from 'react';
import Button from './ui/Button';
import Input from './ui/Input';
import Panel from './ui/Panel';

interface ImportDialogProps {
  onImport: (file: File) => void;
  onClose: () => void;
}

const ImportDialog: React.FC<ImportDialogProps> = ({ onImport, onClose }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleImportClick = () => {
    if (selectedFile) {
      onImport(selectedFile);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      data-testid="import-dialog"
    >
      <Panel className="w-full max-w-md">
        <div className="flex flex-col gap-4">
          <h2 className="text-lg font-semibold">Import DXF File</h2>
          <Input
            type="file"
            accept=".dxf"
            onChange={handleFileChange}
            className="file:mr-4 file:rounded-md file:border-0 file:bg-muted file:px-4 file:py-2 file:text-sm file:font-semibold file:text-muted-foreground hover:file:bg-muted/80"
          />
          <div className="mt-2 flex justify-end gap-2">
            <Button
              onClick={handleImportClick}
              disabled={!selectedFile}
              variant="primary"
            >
              Import
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

export default ImportDialog;
