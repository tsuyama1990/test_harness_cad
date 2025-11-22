import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import useHarnessStore from '../stores/useHarnessStore';
import { getComponents, type LibraryComponent } from '../services/api';
import Button from './ui/Button';
import Input from './ui/Input';

interface WizardModalProps {
    isOpen: boolean;
    onClose: () => void;
}

const WizardModal: React.FC<WizardModalProps> = ({ isOpen, onClose }) => {
    const [step, setStep] = useState(1);
    const [numConnectors, setNumConnectors] = useState<string>('2');
    const [selectedConnectors, setSelectedConnectors] = useState<LibraryComponent[]>([]);
    const [availableConnectors, setAvailableConnectors] = useState<LibraryComponent[]>([]);
    const [cableType, setCableType] = useState<string>('22 AWG - Red'); // Default

    const { setNodes, setEdges } = useHarnessStore();

    useEffect(() => {
        const fetchComponents = async () => {
            try {
                const components = await getComponents();
                setAvailableConnectors(components.filter(c => c.type === 'connector'));
            } catch (error) {
                console.error('Failed to fetch components', error);
            }
        };
        if (isOpen) {
            fetchComponents();
        }
    }, [isOpen]);

    // Reset state when opening
    useEffect(() => {
        if (isOpen) {
            setStep(1);
            setNumConnectors('2');
            setSelectedConnectors([]);
        }
    }, [isOpen]);

    const handleNumConnectorsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNumConnectors(e.target.value);
    };

    const handleNextStep1 = () => {
        const val = parseInt(numConnectors);
        if (isNaN(val) || val < 2) {
            alert("Please enter a valid number of connectors (minimum 2).");
            return;
        }
        if (val > 10) {
            alert("Maximum 10 connectors allowed.");
            return;
        }

        // Initialize selectedConnectors array
        const initial = Array(val).fill(null).map((_, i) =>
            selectedConnectors[i] || (availableConnectors[0] || null)
        );
        setSelectedConnectors(initial);
        setStep(2);
    };

    const handleConnectorSelect = (index: number, componentId: string) => {
        const component = availableConnectors.find(c => c.id === componentId);
        if (component) {
            const newSelected = [...selectedConnectors];
            newSelected[index] = component;
            setSelectedConnectors(newSelected);
        }
    };

    const handleAutoArrange = () => {
        // Create nodes based on selected connectors
        const newNodes = selectedConnectors.map((component, index) => {
            // Simple layout: arrange in a circle or grid
            // Let's do a simple horizontal line for now, or a circle if many
            const x = 100 + (index * 250);
            const y = 100 + (index % 2) * 100; // Stagger slightly

            return {
                id: uuidv4(),
                type: 'customConnector',
                position: { x, y },
                data: { ...component.data, label: `${component.name} ${index + 1}` },
            };
        });

        setNodes(newNodes);
        setEdges([]); // Clear existing edges for this wizard flow

        setStep(4); // Skip to cable selection
    };

    const handleAutoRoute = () => {
        const newEdges: any[] = [];
        const currentNodes = useHarnessStore.getState().nodes;

        if (currentNodes.length < 2) return;

        for (let i = 0; i < currentNodes.length - 1; i++) {
            const sourceNode = currentNodes[i];
            const targetNode = currentNodes[i + 1];

            const sourcePins = sourceNode.data.pins || [];
            const targetPins = targetNode.data.pins || [];

            // Find matching pins (by ID or index)
            sourcePins.forEach((srcPin: any) => {
                const targetPin = targetPins.find((tgtPin: any) => tgtPin.id === srcPin.id);
                if (targetPin) {
                    newEdges.push({
                        id: uuidv4(),
                        source: sourceNode.id,
                        sourceHandle: srcPin.id,
                        target: targetNode.id,
                        targetHandle: targetPin.id,
                        type: 'customWire',
                        data: {
                            wire_id: uuidv4(),
                            color: cableType.split(' - ')[1]?.toLowerCase() || 'black', // Extract color
                            length: 0, // Calculator will update this
                        }
                    });
                }
            });
        }

        setEdges(newEdges);
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="w-[600px] bg-[#3b82f6] border-4 border-white p-8 shadow-pixel-lg text-white">
                <h2 className="text-4xl font-pixel font-bold mb-6 text-center uppercase tracking-widest text-white drop-shadow-md">
                    Harness Wizard - Step {step}
                </h2>

                {step === 1 && (
                    <div className="space-y-6">
                        <label className="block font-pixel text-2xl">Number of Connectors</label>
                        <Input
                            type="number"
                            min={2}
                            max={10}
                            value={numConnectors}
                            onChange={handleNumConnectorsChange}
                            className="w-full text-black text-xl p-3"
                        />
                        <div className="flex justify-end mt-8">
                            <Button onClick={handleNextStep1} className="bg-white text-[#3b82f6] hover:bg-gray-100 border-white text-xl px-6 py-2">
                                Next
                            </Button>
                        </div>
                    </div>
                )}

                {step === 2 && (
                    <div className="space-y-6">
                        <p className="font-pixel text-2xl mb-4">Select Connector Types</p>
                        <div className="max-h-[400px] overflow-y-auto space-y-3 pr-2">
                            {Array.from({ length: parseInt(numConnectors) || 0 }).map((_, idx) => (
                                <div key={idx} className="flex items-center justify-between bg-[#2563eb] p-3 border border-white">
                                    <span className="font-pixel text-xl">Connector {idx + 1}</span>
                                    <select
                                        className="bg-white text-black border border-gray-300 text-lg p-2"
                                        value={selectedConnectors[idx]?.id || ''}
                                        onChange={(e) => handleConnectorSelect(idx, e.target.value)}
                                    >
                                        <option value="">Select...</option>
                                        {availableConnectors.map(c => (
                                            <option key={c.id} value={c.id}>{c.name}</option>
                                        ))}
                                    </select>
                                </div>
                            ))}
                        </div>
                        <div className="flex justify-between mt-8">
                            <Button variant="secondary" onClick={() => setStep(1)} className="bg-[#1d4ed8] border-white hover:bg-[#1e40af] text-xl px-6 py-2">Back</Button>
                            <Button
                                onClick={handleAutoArrange}
                                disabled={selectedConnectors.some(c => !c)}
                                className="bg-white text-[#3b82f6] hover:bg-gray-100 border-white text-xl px-6 py-2"
                            >
                                Auto Arrange
                            </Button>
                        </div>
                    </div>
                )}

                {step === 4 && (
                    <div className="space-y-6">
                        <p className="font-pixel text-2xl mb-4">Select Cable Type</p>
                        <select
                            className="w-full bg-white text-black border border-gray-300 p-3 font-pixel text-xl"
                            value={cableType}
                            onChange={(e) => setCableType(e.target.value)}
                        >
                            <option>22 AWG - Red</option>
                            <option>22 AWG - Black</option>
                            <option>22 AWG - Blue</option>
                            <option>22 AWG - Green</option>
                            <option>22 AWG - Yellow</option>
                            <option>22 AWG - White</option>
                        </select>

                        <div className="flex justify-between mt-8">
                            <Button variant="secondary" onClick={() => setStep(2)} className="bg-[#1d4ed8] border-white hover:bg-[#1e40af] text-xl px-6 py-2">Back</Button>
                            <Button onClick={handleAutoRoute} className="bg-white text-[#3b82f6] hover:bg-gray-100 border-white text-xl px-6 py-2">
                                Auto Route & Finish
                            </Button>
                        </div>
                    </div>
                )}

                <div className="mt-4 text-center">
                    <button onClick={onClose} className="text-xs text-blue-200 hover:text-white underline">Cancel</button>
                </div>
            </div>
        </div>
    );
};

export default WizardModal;
