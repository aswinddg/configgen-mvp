import axios from 'axios';
import { Vendor, Scenario, Param, GenerateRequest } from '@/types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const apiService = {
  getVendors: async (): Promise<Vendor[]> => {
    const response = await api.get('/vendors');
    return response.data;
  },

  getScenarios: async (vendor?: string): Promise<Scenario[]> => {
    const response = await api.get('/scenarios', {
      params: vendor ? { vendor } : {}
    });
    return response.data;
  },

  getScenarioParams: async (scenarioId: number): Promise<Param[]> => {
    const response = await api.get(`/scenarios/${scenarioId}/params`);
    return response.data;
  },

  generateConfig: async (request: GenerateRequest): Promise<Blob> => {
    const response = await api.post('/generate', request, {
      responseType: 'blob'
    });
    return response.data;
  }
};
