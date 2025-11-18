import { useState } from 'react';
import HarnessVisualizer from './HarnessVisualizer';
import ThreeDViewer from './ThreeDViewer';
import useHarnessStore from '../stores/useHarnessStore';
import axios from 'axios';

const MainCanvas = () => {
  const harnessId = '0a9eb930-c504-4835-a281-3e5c1800e1d1';
  const { viewMode, setViewMode } = useHarnessStore();
  const [modelPath, setModelPath] = useState<string | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`/api/v1/harnesses/${harnessId}/3d-model`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setModelPath(response.data.file_path);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="main-content">
      <div className="toolbar">
        <button onClick={() => setViewMode('2D')}>2D Layout</button>
        <button onClick={() => setViewMode('3D')}>3D Route</button>
        {viewMode === '3D' && <input type="file" onChange={handleFileUpload} />}
      </div>
      {viewMode === '2D' ? (
        <HarnessVisualizer harnessId={harnessId} />
      ) : (
        <ThreeDViewer modelPath={modelPath} />
      )}
    </div>
  );
};

export default MainCanvas;
