import axios from 'axios';
import { HarnessData } from '../utils/dataTransformer';

const API_BASE_URL = '/api/v1';

// --- Harness API ---

export const getHarness = async (harnessId: string): Promise<HarnessData> => {
  const response = await axios.get<HarnessData>(
    `${API_BASE_URL}/harnesses/${harnessId}`
  );
  return response.data;
};

export const updateHarness = async (
  harnessId: string,
  harness: HarnessData
): Promise<HarnessData> => {
  const response = await axios.put<HarnessData>(
    `${API_BASE_URL}/harnesses/${harnessId}`,
    harness
  );
  return response.data;
};

// --- Component Library API ---

export interface LibraryComponent {
  id: string;
  type: 'connector' | 'wire';
  name: string;
  data: any;
}

export const getComponents = async (): Promise<LibraryComponent[]> => {
  const response = await axios.get<LibraryComponent[]>(`${API_BASE_URL}/components/`);
  return response.data;
};
