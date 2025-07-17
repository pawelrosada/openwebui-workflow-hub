// Shared types for frontend and backend
export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
  flowId?: string;
  metadata?: {
    tokens?: number;
    duration?: number;
    sources?: string[];
  };
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
  flowId?: string;
}

export interface LangflowResponse {
  result: string;
  session_id?: string;
  outputs?: Record<string, any>;
  logs?: any[];
  metadata?: {
    duration: number;
    timestamp: string;
  };
}

export interface LangflowRequest {
  message: string;
  session_id?: string;
  flow_id?: string;
  inputs?: Record<string, any>;
}

export interface FlowConfig {
  id: string;
  name: string;
  description?: string;
  endpoint: string;
  isActive: boolean;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface WebSocketMessage {
  type: 'message' | 'status' | 'error' | 'typing';
  data: any;
  sessionId?: string;
}
