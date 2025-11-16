import { ReactFlowProvider } from 'reactflow';
import Sidebar from './components/Sidebar';
import HarnessVisualizer from './components/HarnessVisualizer';
import AttributeEditorPanel from './components/AttributeEditorPanel';
import './App.css';

function App() {
  // For Cycle 2, we'll hardcode the harness ID.
  // In a future cycle, this would come from a URL or project selection UI.
  const harnessId = '0a9eb930-c504-4835-a281-3e5c1800e1d1'; // A valid UUID

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
