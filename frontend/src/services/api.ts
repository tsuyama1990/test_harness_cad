import axios from 'axios';
import type { HarnessData } from '../utils/dataTransformer';

export const API_BASE_URL = '/api/v1';

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



interface LibraryComponentData {

  name: string;

  part_number: string;

  pins: { id: string }[];

}



export interface LibraryComponent {

  id: string;

  type: 'connector' | 'wire';

  name: string;

  data: LibraryComponentData;

}

export const getComponents = async (): Promise<LibraryComponent[]> => {
  const response = await axios.get<LibraryComponent[]>(`${API_BASE_URL}/components/`);
  return response.data;
};
