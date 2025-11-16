import { useState } from 'react';
import HarnessVisualizer from './components/HarnessVisualizer';
import { ReactFlowProvider } from 'reactflow';
import './App.css';

function App() {
  const [harnessId, setHarnessId] = useState('');
  const [submittedId, setSubmittedId] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittedId(harnessId);
  };

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      {!submittedId ? (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={harnessId}
            onChange={(e) => setHarnessId(e.target.value)}
            placeholder="Enter Harness ID"
          />
          <button type="submit">Load Harness</button>
        </form>
      ) : (
        <ReactFlowProvider>
          <HarnessVisualizer harnessId={submittedId} />
        </ReactFlowProvider>
      )}
    </div>
  );
}

export default App;
