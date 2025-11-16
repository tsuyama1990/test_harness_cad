import useHarnessStore from '../stores/useHarnessStore';

export const useReactFlowCallbacks = () => {
  const { onNodesChange, onEdgesChange, onConnect } = useHarnessStore(
    (state) => ({
      onNodesChange: state.onNodesChange,
      onEdgesChange: state.onEdgesChange,
      onConnect: state.onConnect,
    })
  );

  return {
    onNodesChange,
    onEdgesChange,
    onConnect,
  };
};
