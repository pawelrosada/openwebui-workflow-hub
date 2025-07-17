import axios, { AxiosInstance } from 'axios';
import { LangflowRequest, LangflowResponse } from '@/types/index.js';

export class LangflowService {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.LANGFLOW_API_URL || 'http://localhost:7860';
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async sendMessage(request: LangflowRequest): Promise<LangflowResponse> {
    try {
      const response = await this.client.post('/api/v1/run', {
        input_value: request.message,
        input_type: 'chat',
        output_type: 'chat',
        session_id: request.session_id,
        ...request.inputs,
      });

      return {
        result: response.data.outputs?.[0]?.outputs?.[0]?.results?.message?.text || response.data.result || 'No response',
        session_id: response.data.session_id,
        outputs: response.data.outputs,
        logs: response.data.logs,
        metadata: {
          duration: response.data.duration || 0,
          timestamp: new Date().toISOString(),
        },
      };
    } catch (error) {
      console.error('Langflow API error:', error);
      throw new Error(`Langflow API error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async getFlows(): Promise<any[]> {
    try {
      const response = await this.client.get('/api/v1/flows');
      return response.data || [];
    } catch (error) {
      console.error('Error fetching flows:', error);
      return [];
    }
  }

  async getFlow(flowId: string): Promise<any> {
    try {
      const response = await this.client.get(`/api/v1/flows/${flowId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching flow ${flowId}:`, error);
      throw new Error(`Flow not found: ${flowId}`);
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      await this.client.get('/health');
      return true;
    } catch {
      return false;
    }
  }
}
