import { ReactFlowProvider } from 'reactflow';
import Sidebar from './components/Sidebar';
import MainCanvas from './components/MainCanvas';
import AttributeEditorPanel from './components/AttributeEditorPanel';

function App() {
  return (
    <div className="flex flex-row h-screen bg-background text-text-main">
      <ReactFlowProvider>
        <Sidebar />
        <div className="flex-grow h-screen">
          <MainCanvas />
        </div>
        <AttributeEditorPanel />
      </ReactFlowProvider>
    </div>
  );
}

export default App;
