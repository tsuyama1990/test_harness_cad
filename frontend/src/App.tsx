import { ReactFlowProvider } from 'reactflow';
import Sidebar from './components/Sidebar';
import MainCanvas from './components/MainCanvas';
import AttributeEditorPanel from './components/AttributeEditorPanel';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <ReactFlowProvider>
        <Sidebar />
        <MainCanvas />
        <AttributeEditorPanel />
      </ReactFlowProvider>
    </div>
  );
}

export default App;
