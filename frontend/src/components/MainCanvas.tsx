import { useState } from 'react';
import HarnessVisualizer from './HarnessVisualizer';
import ThreeDViewer from './ThreeDViewer';
import useHarnessStore from '../stores/useHarnessStore';
import axios from 'axios';
import Button from './ui/Button';
import Input from './ui/Input';

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
      const response = await axios.post(
        `/api/v1/harnesses/${harnessId}/3d-model`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setModelPath(response.data.file_path);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="relative h-full w-full">
      <div className="absolute top-4 left-4 z-10 flex items-center gap-2 rounded-lg border border-gray-300 bg-white p-3 shadow-xl backdrop-blur-sm">
        <Button
          onClick={() => setViewMode('2D')}
          variant={viewMode === '2D' ? 'primary' : 'secondary'}
        >
          2D Layout
        </Button>
        <Button
          onClick={() => setViewMode('3D')}
          variant={viewMode === '3D' ? 'primary' : 'secondary'}
        >
          3D Route
        </Button>
        {viewMode === '3D' && (
          <Input
            type="file"
            onChange={handleFileUpload}
            className="text-sm file:mr-2 file:rounded-md file:border-0 file:bg-muted file:px-3 file:py-1.5 file:text-sm file:font-semibold file:text-muted-foreground hover:file:bg-muted/80"
          />
        )}
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
