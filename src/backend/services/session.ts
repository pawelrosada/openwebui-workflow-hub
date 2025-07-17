import { Message, ChatSession } from '@/types/index.js';
import { v4 as uuidv4 } from 'uuid';

export class SessionService {
  private sessions: Map<string, ChatSession> = new Map();

  createSession(flowId?: string): ChatSession {
    const session: ChatSession = {
      id: uuidv4(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
      flowId,
    };

    this.sessions.set(session.id, session);
    return session;
  }

  getSession(sessionId: string): ChatSession | undefined {
    return this.sessions.get(sessionId);
  }

  getAllSessions(): ChatSession[] {
    return Array.from(this.sessions.values()).sort(
      (a, b) => b.updatedAt.getTime() - a.updatedAt.getTime()
    );
  }

  addMessage(sessionId: string, message: Message): ChatSession | undefined {
    const session = this.sessions.get(sessionId);
    if (!session) return undefined;

    session.messages.push(message);
    session.updatedAt = new Date();

    // Auto-generate title from first user message
    if (message.role === 'user' && session.messages.length === 1) {
      session.title = message.content.slice(0, 50) + (message.content.length > 50 ? '...' : '');
    }

    return session;
  }

  updateSession(sessionId: string, updates: Partial<ChatSession>): ChatSession | undefined {
    const session = this.sessions.get(sessionId);
    if (!session) return undefined;

    Object.assign(session, updates, { updatedAt: new Date() });
    return session;
  }

  deleteSession(sessionId: string): boolean {
    return this.sessions.delete(sessionId);
  }

  clearAllSessions(): void {
    this.sessions.clear();
  }
}
