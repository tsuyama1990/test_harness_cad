import axios from 'axios';

const API_BASE_URL = '/api/v1';

export interface Pin {
  id: string;
}

export interface Connector {
  id: string;
  manufacturer: string;
  part_number: string;
  pins: Pin[];
}

export interface Wire {
  id: string;
  manufacturer: string;
  part_number: string;
  color: string;
  gauge: number;
  length: number;
}

export interface Connection {
  wire_id: string;
  from_connector_id: string;
  from_pin_id: string;
  to_connector_id: string;
  to_pin_id: string;
}

export interface Harness {
  id: string;
  name: string;
  connectors: Connector[];
  wires: Wire[];
  connections: Connection[];
}

export const getHarness = async (harnessId: string): Promise<Harness> => {
  const response = await axios.get<Harness>(`${API_BASE_URL}/harnesses/${harnessId}`);
  return response.data;
};

export const createHarness = async (harness: Omit<Harness, 'id'>): Promise<Harness> => {
  const response = await axios.post<Harness>(`${API_BASE_URL}/harnesses/`, harness);
  return response.data;
};
