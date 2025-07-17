import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { LangflowService } from '../services/langflow.js';

const langflowService = new LangflowService();

export async function flowRoutes(fastify: FastifyInstance) {
  // Get all available flows
  fastify.get('/', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const flows = await langflowService.getFlows();
      return reply.send({
        success: true,
        data: flows,
      });
    } catch (error) {
      fastify.log.error('Get flows error:', error);
      return reply.status(500).send({
        success: false,
        error: 'Failed to fetch flows',
      });
    }
  });

  // Get specific flow
  fastify.get('/:flowId', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const { flowId } = request.params as { flowId: string };
      const flow = await langflowService.getFlow(flowId);
      
      return reply.send({
        success: true,
        data: flow,
      });
    } catch (error) {
      fastify.log.error('Get flow error:', error);
      return reply.status(404).send({
        success: false,
        error: 'Flow not found',
      });
    }
  });

  // Health check for Langflow connection
  fastify.get('/health/langflow', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const isHealthy = await langflowService.healthCheck();
      return reply.send({
        success: true,
        data: {
          status: isHealthy ? 'healthy' : 'unhealthy',
          timestamp: new Date().toISOString(),
        },
      });
    } catch (error) {
      fastify.log.error('Langflow health check error:', error);
      return reply.status(503).send({
        success: false,
        error: 'Langflow service unavailable',
      });
    }
  });
}
