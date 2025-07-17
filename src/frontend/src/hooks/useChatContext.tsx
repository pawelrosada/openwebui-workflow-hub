import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Message, ChatSession, ApiResponse } from '@/types';

interface ChatContextType {
  sessions: ChatSession[];
  currentSession: ChatSession | null;
  isLoading: boolean;
  isTyping: boolean;
  createNewSession: () => Promise<ChatSession>;
  selectSession: (sessionId: string) => void;
  sendMessage: (content: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  clearAllSessions: () => Promise<void>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export function ChatProvider({ children }: { children: ReactNode }) {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);

  // Load sessions on mount
  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const response = await fetch('/api/sessions');
      const data: ApiResponse<ChatSession[]> = await response.json();
      if (data.success && data.data) {
        setSessions(data.data);
        if (data.data.length > 0 && !currentSession) {
          setCurrentSession(data.data[0]);
        }
      }
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const createNewSession = async (): Promise<ChatSession> => {
    try {
      const response = await fetch('/api/sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      const data: ApiResponse<ChatSession> = await response.json();
      if (data.success && data.data) {
        setSessions(prev => [data.data!, ...prev]);
        setCurrentSession(data.data);
        return data.data;
      }
      throw new Error(data.error || 'Failed to create session');
    } catch (error) {
      console.error('Failed to create session:', error);
      throw error;
    }
  };

  const selectSession = (sessionId: string) => {
    const session = sessions.find(s => s.id === sessionId);
    if (session) {
      setCurrentSession(session);
    }
  };

  const sendMessage = async (content: string) => {
    if (!currentSession) {
      await createNewSession();
    }

    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await fetch('/api/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          sessionId: currentSession?.id,
        }),
      });

      const data: ApiResponse<{
        sessionId: string;
        userMessage: Message;
        assistantMessage: Message;
        session: ChatSession;
      }> = await response.json();

      if (data.success && data.data) {
        // Update current session
        setCurrentSession(data.data.session);
        
        // Update sessions list
        setSessions(prev => 
          prev.map(s => s.id === data.data!.session.id ? data.data!.session : s)
        );
      } else {
        throw new Error(data.error || 'Failed to send message');
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      throw error;
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const deleteSession = async (sessionId: string) => {
    try {
      const response = await fetch(`/api/sessions/${sessionId}`, {
        method: 'DELETE',
      });

      const data: ApiResponse = await response.json();
      if (data.success) {
        setSessions(prev => prev.filter(s => s.id !== sessionId));
        if (currentSession?.id === sessionId) {
          const remainingSessions = sessions.filter(s => s.id !== sessionId);
          setCurrentSession(remainingSessions[0] || null);
        }
      }
    } catch (error) {
      console.error('Failed to delete session:', error);
    }
  };

  const clearAllSessions = async () => {
    try {
      const response = await fetch('/api/sessions', {
        method: 'DELETE',
      });

      const data: ApiResponse = await response.json();
      if (data.success) {
        setSessions([]);
        setCurrentSession(null);
      }
    } catch (error) {
      console.error('Failed to clear sessions:', error);
    }
  };

  return (
    <ChatContext.Provider value={{
      sessions,
      currentSession,
      isLoading,
      isTyping,
      createNewSession,
      selectSession,
      sendMessage,
      deleteSession,
      clearAllSessions,
    }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}
