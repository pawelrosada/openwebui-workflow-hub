import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { SessionService } from '../services/session.js';
import { z } from 'zod';

const sessionService = new SessionService();

const CreateSessionSchema = z.object({
  flowId: z.string().optional(),
});

const UpdateSessionSchema = z.object({
  title: z.string().optional(),
  flowId: z.string().optional(),
});

export async function sessionRoutes(fastify: FastifyInstance) {
  // Get all sessions
  fastify.get('/', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const sessions = sessionService.getAllSessions();
      return reply.send({
        success: true,
        data: sessions,
      });
    } catch (error) {
      fastify.log.error('Get sessions error:', error);
      return reply.status(500).send({
        success: false,
        error: 'Failed to fetch sessions',
      });
    }
  });

  // Create new session
  fastify.post('/', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const { flowId } = CreateSessionSchema.parse(request.body);
      const session = sessionService.createSession(flowId);
      
      return reply.send({
        success: true,
        data: session,
      });
    } catch (error) {
      fastify.log.error('Create session error:', error);
      return reply.status(500).send({
        success: false,
        error: 'Failed to create session',
      });
    }
  });

  // Get specific session
  fastify.get('/:sessionId', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const { sessionId } = request.params as { sessionId: string };
      const session = sessionService.getSession(sessionId);

      if (!session) {
        return reply.status(404).send({
          success: false,
          error: 'Session not found',
        });
      }

      return reply.send({
        success: true,
        data: session,
      });
    } catch (error) {
      fastify.log.error('Get session error:', error);
      return reply.status(500).send({
        success: false,
        error: 'Failed to fetch session',
      });
    }
  });

  // Update session
  fastify.patch('/:sessionId', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const { sessionId } = request.params as { sessionId: string };
      const updates = UpdateSessionSchema.parse(request.body);
      
      const session = sessionService.updateSession(sessionId, updates);

      if (!session) {
        return reply.status(404).send({
          success: false,
          error: 'Session not found',
        });
      }

      return reply.send({
        success: true,
        data: session,
      });
    } catch (error) {
      fastify.log.error('Update session error:', error);
      return reply.status(500).send({
        success: false,
        error: 'Failed to update session',
      });
    }
  });

  // Delete session
  fastify.delete('/:sessionId', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const { sessionId } = request.params as { sessionId: string };
      const deleted = sessionService.deleteSession(sessionId);

      if (!deleted) {
        return reply.status(404).send({
          success: false,
          error: 'Session not found',
        });
      }

      return reply.send({
        success: true,
        message: 'Session deleted successfully',
      });
    } catch (error) {
      fastify.log.error('Delete session error:', error);
      return reply.status(500).send({
        success: false,
        error: 'Failed to delete session',
      });
    }
  });

  // Clear all sessions
  fastify.delete('/', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      sessionService.clearAllSessions();
      return reply.send({
        success: true,
        message: 'All sessions cleared',
      });
    } catch (error) {
      fastify.log.error('Clear sessions error:', error);
      return reply.status(500).send({
        success: false,
        error: 'Failed to clear sessions',
      });
    }
  });
}
