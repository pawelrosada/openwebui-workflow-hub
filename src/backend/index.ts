import fastify from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';
import staticFiles from '@fastify/static';
import { chatRoutes } from './routes/chat.js';
import { flowRoutes } from './routes/flows.js';
import { sessionRoutes } from './routes/sessions.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const createApp = () => {
  const app = fastify({
    logger: {
      level: process.env.LOG_LEVEL || 'info',
      transport: {
        target: 'pino-pretty',
        options: {
          colorize: true,
          translateTime: 'HH:MM:ss Z',
          ignore: 'pid,hostname',
        },
      },
    },
  });

  return app;
};

const start = async () => {
  try {
    const app = createApp();

    // Security middleware
    await app.register(helmet, {
      contentSecurityPolicy: process.env.NODE_ENV === 'production' ? false : {
        directives: {
          defaultSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          scriptSrc: ["'self'", "'unsafe-eval'"],
          imgSrc: ["'self'", "data:", "https:"],
          connectSrc: ["'self'", "ws:", "wss:"],
        },
      },
    });

    // CORS
    await app.register(cors, {
      origin: process.env.NODE_ENV === 'production' ? false : true,
      credentials: true,
    });

    // Rate limiting
    await app.register(rateLimit, {
      max: 100,
      timeWindow: '1 minute',
    });

    // Static files (production only)
    if (process.env.NODE_ENV === 'production') {
      await app.register(staticFiles, {
        root: path.join(__dirname, '../../frontend'),
        prefix: '/',
      });
    }

    // Routes
    await app.register(chatRoutes, { prefix: '/api/chat' });
    await app.register(flowRoutes, { prefix: '/api/flows' });
    await app.register(sessionRoutes, { prefix: '/api/sessions' });

    // Health check
    app.get('/api/health', async () => {
      return { status: 'ok', timestamp: new Date().toISOString() };
    });

    // Catch-all for SPA (production only)
    if (process.env.NODE_ENV === 'production') {
      app.setNotFoundHandler((request, reply) => {
        if (request.url.startsWith('/api')) {
          reply.code(404).send({ error: 'API endpoint not found' });
        } else {
          reply.sendFile('index.html');
        }
      });
    }

    const port = Number(process.env.PORT) || 3000;
    const host = process.env.HOST || '0.0.0.0';
    
    await app.listen({ port, host });
    app.log.info(`🚀 Server running on http://${host}:${port}`);
  } catch (err) {
    console.error('Failed to start server:', err);
    process.exit(1);
  }
};

start();
