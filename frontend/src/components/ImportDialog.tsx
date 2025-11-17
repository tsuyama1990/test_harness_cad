// frontend/src/components/ImportDialog.tsx
import React, { useState } from 'react';

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
    <div className="modal">
      <div className="modal-content">
        <h2>Import DXF File</h2>
        <input type="file" accept=".dxf" onChange={handleFileChange} />
        <div className="modal-actions">
          <button onClick={handleImportClick} disabled={!selectedFile}>
            Import
          </button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default ImportDialog;
