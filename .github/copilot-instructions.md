# Copilot Instructions for Langflow-based Applications

## 📋 Spis treści

1. [Ogólne wytyczne](#ogólne-wytyczne)
2. [Stack technologiczny](#stack-technologiczny)
3. [Wzorce architektoniczne](#wzorce-architektoniczne)
4. [Integracja z Langflow](#integracja-z-langflow)
5. [Standardy kodu](#standardy-kodu)
6. [Konfiguracja Docker](#konfiguracja-docker)
7. [Skrypty deweloperskie](#skrypty-deweloperskie)
8. [Bezpieczeństwo i wydajność](#bezpieczeństwo-i-wydajność)
9. [Standardy testowania](#standardy-testowania)
10. [Zasady generowania kodu](#zasady-generowania-kodu)

---

## 🎯 Ogólne wytyczne

### Podstawowe zasady
- **Zawsze używaj TypeScript** z włączonym trybem strict
- **Implementuj właściwą obsługę błędów** z niestandardowymi klasami błędów
- **Konteneryzuj wszystkie komponenty** za pomocą Docker
- **Pisz testy** dla każdej funkcjonalności
- **Dokumentuj kod** i API

---

## 🛠 Stack technologiczny

### Backend (2025 Standards)
| Komponent | Technologia | Wersja |
|-----------|-------------|--------|
| **Runtime** | Node.js LTS | 22+ |
| **Język** | TypeScript | 5.3+ |
| **Framework** | Fastify / Express | 4.26+ / 5+ |
| **Baza danych** | PostgreSQL | 16+ |
| **ORM** | Prisma / Drizzle | 5.9+ |
| **Walidacja** | Zod | 3.22+ |
| **Autentykacja** | Lucia Auth / Auth.js | NextAuth v5 |
| **Cache** | Redis | 7.2+ |
| **Queue** | BullMQ | 5+ |
| **Testing** | Vitest | 1.2+ |
| **Build** | Vite / esbuild | 5+ |
| **Package Manager** | pnpm | 8.15+ |

---

## 🏗 Wzorce architektoniczne

### Rekomendowane wzorce
- **Clean Architecture** - separacja warstw biznesowych
- **Hexagonal Architecture** - lepsze testowanie
- **Repository Pattern** - abstrakcja dostępu do danych
- **CQRS** - separacja odczytu i zapisu
- **Event-Driven Architecture** - asynchroniczna komunikacja
- **Modular Monolith** - struktura modularna

---

## 🔗 Integracja z Langflow

### Główne punkty integracji
- **REST API** - komunikacja z backendem Python
- **WebSocket** - aktualizacje w czasie rzeczywistym
- **Webhooks** - obsługa callbacków
- **Mikrousługi** - komplementarne serwisy Node.js
- **Custom Components** - rozszerzenia przez Node.js

---

## 💻 Standardy kodu

### TypeScript - podstawowy szablon

```typescript
// Używaj strict TypeScript configuration
import { z } from 'zod';
import type { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';

// Zawsze używaj Zod do walidacji
const FlowRequestSchema = z.object({
  flowId: z.string().uuid(),
  inputs: z.record(z.unknown()),
  metadata: z.object({
    userId: z.string(),
    timestamp: z.date().default(() => new Date())
  }).optional()
});

type FlowRequest = z.infer<typeof FlowRequestSchema>;

// Właściwa obsługa błędów
class FlowExecutionError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500
  ) {
    super(message);
    this.name = 'FlowExecutionError';
  }
}
```

### Operacje bazodanowe z Prisma

```typescript
import { PrismaClient } from '@prisma/client';
import type { Flow, User } from '@prisma/client';

class FlowRepository {
  constructor(private prisma: PrismaClient) {}

  async createFlow(data: CreateFlowInput): Promise<Flow> {
    try {
      return await this.prisma.flow.create({
        data,
        include: { user: true, components: true }
      });
    } catch (error) {
      throw new DatabaseError('Failed to create flow', error);
    }
  }
}
```

### API Design z Fastify

```typescript
import fastify from 'fastify';
import { flowRoutes } from './routes/flows.js';

const app = fastify({
  logger: {
    level: process.env.LOG_LEVEL || 'info',
    transport: {
      target: 'pino-pretty'
    }
  }
});

// Rejestracja pluginów
await app.register(import('@fastify/helmet'));
await app.register(import('@fastify/cors'));
await app.register(import('@fastify/rate-limit'));
await app.register(flowRoutes, { prefix: '/api/v1' });
```

---

## 🐳 Konfiguracja Docker

### Docker Compose - pełna konfiguracja

```yaml
version: '3.8'

services:
  langflow-node-api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/langflow_node
      - REDIS_URL=redis://redis:6379
      - LANGFLOW_API_URL=http://langflow-python:7860
    depends_on:
      - db
      - redis
      - langflow-python
    ports:
      - "3000:3000"
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  langflow-python:
    image: langflowai/langflow:latest
    environment:
      - LANGFLOW_DATABASE_URL=postgresql://user:pass@db:5432/langflow
    depends_on:
      - db
    ports:
      - "7860:7860"
    volumes:
      - langflow_data:/app/data

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: langflow_node
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7.2-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - langflow-node-api
      - langflow-python

volumes:
  postgres_data:
  redis_data:
  langflow_data:
```

### Multi-stage Dockerfile

```dockerfile
# Dockerfile
FROM node:22-alpine AS base
RUN corepack enable pnpm

FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM base AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

FROM base AS production
WORKDIR /app
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nodejs
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist
COPY --from=build --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=nodejs:nodejs /app/package.json ./package.json
USER nodejs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

---

## 🚀 Skrypty deweloperskie

### Package.json - standardowe skrypty

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc && tsc-alias",
    "start": "node dist/index.js",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "db:generate": "prisma generate",
    "db:migrate": "prisma migrate dev",
    "db:studio": "prisma studio",
    "docker:dev": "./scripts/dev.sh",
    "docker:prod": "./scripts/prod.sh"
  }
}
```

### Skrypt deweloperski (dev.sh)

```bash
#!/bin/bash
# scripts/dev.sh

echo "🚀 Starting Langflow Node.js development environment..."

# Sprawdź czy Docker działa
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Utwórz .env jeśli nie istnieje
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
fi

# Zbuduj i uruchom serwisy
echo "🏗️  Building and starting services..."
docker-compose -f docker-compose.dev.yml up --build -d

# Poczekaj na bazę danych
echo "⏳ Waiting for database to be ready..."
until docker-compose -f docker-compose.dev.yml exec db pg_isready -U user -d langflow_node; do
    sleep 2
done

# Uruchom migracje
echo "🗄️  Running database migrations..."
pnpm db:migrate

# Zainstaluj zależności jeśli potrzebne
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    pnpm install
fi

echo "✅ Development environment is ready!"
echo "🌐 Node.js API: http://localhost:3000"
echo "🔧 Langflow UI: http://localhost:7860"
echo "📊 Database Studio: pnpm db:studio"
echo "📝 API Documentation: http://localhost:3000/docs"
```

### Skrypt produkcyjny (prod.sh)

```bash
#!/bin/bash
# scripts/prod.sh

echo "🚀 Deploying to production..."

# Zbuduj obrazy produkcyjne
docker-compose build --no-cache

# Uruchom serwisy
docker-compose up -d

# Sprawdź zdrowie aplikacji
echo "🏥 Running health checks..."
sleep 10

if curl -f http://localhost:3000/health; then
    echo "✅ Node.js API is healthy"
else
    echo "❌ Node.js API health check failed"
    exit 1
fi

if curl -f http://localhost:7860/health; then
    echo "✅ Langflow is healthy"
else
    echo "❌ Langflow health check failed"
    exit 1
fi

echo "🎉 Production deployment successful!"
```

---

## 🔒 Bezpieczeństwo i wydajność

### Konfiguracja bezpieczeństwa

```typescript
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';

await app.register(helmet, {
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"]
    }
  }
});

await app.register(rateLimit, {
  max: 100,
  timeWindow: '1 minute'
});
```

### Optymalizacja wydajności - Redis caching

```typescript
import Redis from 'ioredis';

class CacheService {
  private redis = new Redis(process.env.REDIS_URL);

  async get<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }

  async set(key: string, value: unknown, ttl = 3600): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }
}
```

---

## 🧪 Standardy testowania

### Konfiguracja Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html']
    }
  }
});
```

### Przykłady testów

```typescript
// tests/flows.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { build } from '../src/app.js';

describe('Flow API', () => {
  let app: FastifyInstance;

  beforeEach(async () => {
    app = build({ logger: false });
    await app.ready();
  });

  it('should create a new flow', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/flows',
      payload: {
        name: 'Test Flow',
        description: 'A test flow'
      }
    });

    expect(response.statusCode).toBe(201);
    expect(response.json()).toMatchObject({
      name: 'Test Flow',
      description: 'A test flow'
    });
  });
});
```

---

## ⚙️ Zasady generowania kodu

### ✅ Obowiązkowe standardy

1. **TypeScript strict mode** - zawsze włączony
2. **Obsługa błędów** - niestandardowe klasy błędów
3. **Walidacja Zod** - dla wszystkich inputów
4. **Testy Vitest** - comprehensive coverage
5. **Docker** - aktualizacja docker-compose.yml
6. **Skrypty** - tworzenie/aktualizacja run scripts
7. **Logging** - structured format
8. **Dependency Injection** - lepsza testowalność
9. **Migracje DB** - Prisma migrations
10. **Monitoring** - health checks
11. **Redis caching** - dla wydajności
12. **Security** - rate limiting i security headers

### 🎯 Cel końcowy

Każda zmiana kodu powinna być:
- **Skonteneryzowana** - gotowa do Docker
- **Przetestowana** - z pełnym pokryciem
- **Gotowa do produkcji** - z właściwą integracją z Langflow Python backend

---

*Ostatnia aktualizacja: 17 lipca 2025*