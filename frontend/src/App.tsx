import { ReactFlowProvider } from 'reactflow';
import Sidebar from './components/Sidebar';
import HarnessVisualizer from './components/HarnessVisualizer';
import AttributeEditorPanel from './components/AttributeEditorPanel';
import './App.css';

function App() {
  // For Cycle 2, we'll hardcode the harness ID.
  // In a future cycle, this would come from a URL or project selection UI.
  const harnessId = '3fa85f64-5717-4562-b3fc-2c963f66afa6'; // A valid UUID

  return (
    <div className="app-container">
      <ReactFlowProvider>
        <Sidebar />
        <div className="main-content">
          <HarnessVisualizer harnessId={harnessId} />
        </div>
        <AttributeEditorPanel />
      </ReactFlowProvider>
    </div>
  );
}

export default App;
