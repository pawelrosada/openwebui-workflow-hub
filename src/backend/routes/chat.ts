import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { z } from 'zod';
import { LangflowService } from '../services/langflow.js';
import { SessionService } from '../services/session.js';
import { Message } from '@/types/index.js';
import { v4 as uuidv4 } from 'uuid';

const langflowService = new LangflowService();
const sessionService = new SessionService();

const SendMessageSchema = z.object({
  message: z.string().min(1).max(10000),
  sessionId: z.string().uuid().optional(),
  flowId: z.string().optional(),
});

const GetMessagesSchema = z.object({
  sessionId: z.string().uuid(),
});

export async function chatRoutes(fastify: FastifyInstance) {
  // Send message to Langflow
  fastify.post('/send', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const { message, sessionId, flowId } = SendMessageSchema.parse(request.body);

      // Get or create session
      let session = sessionId ? sessionService.getSession(sessionId) : null;
      if (!session) {
        session = sessionService.createSession(flowId);
      }

      // Add user message
      const userMessage: Message = {
        id: uuidv4(),
        content: message,
        role: 'user',
        timestamp: new Date(),
        flowId: session.flowId,
      };

      sessionService.addMessage(session.id, userMessage);

      // Send to Langflow
      const langflowResponse = await langflowService.sendMessage({
        message,
        session_id: session.id,
        flow_id: session.flowId,
      });

      // Add assistant response
      const assistantMessage: Message = {
        id: uuidv4(),
        content: langflowResponse.result,
        role: 'assistant',
        timestamp: new Date(),
        flowId: session.flowId,
        metadata: langflowResponse.metadata,
      };

      sessionService.addMessage(session.id, assistantMessage);

      return reply.send({
        success: true,
        data: {
          sessionId: session.id,
          userMessage,
          assistantMessage,
          session: sessionService.getSession(session.id),
        },
      });
    } catch (error) {
      fastify.log.error('Chat send error:', error);
      return reply.status(500).send({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  });

  // Get messages for a session
  fastify.get('/messages/:sessionId', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const { sessionId } = GetMessagesSchema.parse(request.params);
      const session = sessionService.getSession(sessionId);

      if (!session) {
        return reply.status(404).send({
          success: false,
          error: 'Session not found',
        });
      }

      return reply.send({
        success: true,
        data: {
          messages: session.messages,
          session,
        },
      });
    } catch (error) {
      fastify.log.error('Get messages error:', error);
      return reply.status(500).send({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  });
}
