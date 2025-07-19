# Copilot Instructions for Langflow-based Applications

## 📋 Table of Contents

1. [General Guidelines](#general-guidelines)
2. [Technology Stack](#technology-stack)
3. [Architectural Patterns](#architectural-patterns)
4. [Langflow Integration](#langflow-integration)
5. [Code Standards](#code-standards)
6. [Docker Configuration](#docker-configuration)
7. [Development Scripts](#development-scripts)
8. [Security and Performance](#security-and-performance)
9. [Testing Standards](#testing-standards)
10. [Code Generation Rules](#code-generation-rules)
*11. [CI/CD Pipelines](#ci-cd-pipelines)*  // Nowa sekcja dodana dla pipelines

---

## 🎯 General Guidelines

### Communication Language
- **Always respond in Polish** when interacting with users
- **Code comments and documentation** should be in Polish
- **Variable names and functions** can be in English (standard practice)
- **Error messages** should be in Polish for better user experience

### Basic Principles
- **Always use TypeScript** with strict mode enabled
- **Implement proper error handling** with custom error classes
- **Containerize all components** using Docker *i Docker Compose do orkiestracji wieloserwisowych środowisk*
- **Write tests** for every functionality
- **Document code** and APIs in Polish
* - **Buduj całość aplikacji z użyciem Open WebUI jako obowiązkowego frameworka frontendowego, integrując go z Docker i pipelines dla automatyzacji deploymentu***

---

## 🛠 Technology Stack

### Backend (2025 Standards)
| Component | Technology | Version |
|-----------|-------------|--------|
| **Runtime** | Node.js LTS | 22+ |
| **Language** | TypeScript | 5.3+ |
| **Framework** | Fastify / Express | 4.26+ / 5+ |
| **Database** | PostgreSQL | 16+ |
| **ORM** | Prisma / Drizzle | 5.9+ |
| **Validation** | Zod | 3.22+ |
| **Authentication** | Lucia Auth / Auth.js | NextAuth v5 |
| **Cache** | Redis | 7.2+ |
| **Queue** | BullMQ | 5+ |
| **Testing** | Vitest | 1.2+ |
| **Build** | Vite / esbuild | 5+ |
| **Package Manager** | pnpm | 8.15+ |
* | **Konteneryzacja** | Docker & Docker Compose | Latest (z multi-stage builds) |*

### Frontend (MANDATORY)
| Component | Technology | Version |
|-----------|-------------|--------|
| **Framework** | **Open WebUI** | Latest |
| **Base** | Svelte/SvelteKit | Latest supported |
| **Styling** | Tailwind CSS | As per Open WebUI |
| **Components** | Open WebUI Components | Latest |
| **State Management** | Svelte stores | As per Open WebUI |

**⚠️ IMPORTANT: All frontend development MUST use Open WebUI framework (https://github.com/open-webui/open-webui)** *– integruj z Docker do budowania obrazów i pipelines do automatycznego deploymentu, zapewniając kompatybilność z Langflow dla AI flows.*

---

## 🏗 Architectural Patterns

### Recommended Patterns
- **Clean Architecture** - business layer separation
- **Hexagonal Architecture** - better testing
- **Repository Pattern** - data access abstraction
- **CQRS** - read/write separation
- **Event-Driven Architecture** - asynchronous communication
- **Modular Monolith** - modular structure

---

## 🔗 Langflow Integration

### Main Integration Points
- **REST API** - communication with Python backend
- **WebSocket** - real-time updates
- **Webhooks** - callback handling
- **Microservices** - complementary Node.js services
- **Custom Components** - extensions through Node.js
- **Open WebUI Integration** - chat interface for Langflow flows
* - **Docker Integration** - uruchamiaj Langflow w kontenerach Docker z Docker Compose dla łatwej skalowalności*

---

## 💻 Code Standards

### TypeScript - Basic Template

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

// Właściwa obsługa błędów z polskimi komunikatami
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

### Open WebUI Frontend Integration

```typescript
// src/lib/stores/langflow.ts
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

interface LangflowState {
  flows: Flow[];
  activeFlow: Flow | null;
  isExecuting: boolean;
}

export const langflowStore: Writable<LangflowState> = writable({
  flows: [],
  activeFlow: null,
  isExecuting: false
});

// Integracja z Open WebUI chat
export const executeLangflowInChat = async (flowId: string, message: string) => {
  // Implementacja wykonania flow w kontekście chatu Open WebUI
  const response = await fetch('/api/langflow/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ flowId, message })
  });
  
  return response.json();
};
```

### Database Operations with Prisma

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
      throw new DatabaseError('Nie udało się utworzyć przepływu', error);
    }
  }
}
```

---

## 🐳 Docker Configuration

### Docker Compose - Full Configuration
*// Zaktualizowano, aby podkreślić użycie Docker Compose jako głównego narzędzia do budowy i orkiestracji całej aplikacji, integrując Open WebUI z Langflow.*

```yaml
version: '3.8'

services:
  open-webui:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
      - LANGFLOW_API_URL=http://langflow-node-api:3000
    depends_on:
      - langflow-node-api
    ports:
      - "8080:8080"
    volumes:
      - open_webui_data:/app/backend/data

  langflow-node-api:
    build:
      context: ./backend
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
      - open-webui
      - langflow-node-api
      - langflow-python

volumes:
  postgres_data:
  redis_data:
  langflow_data:
  open_webui_data:
```

### Multi-stage Dockerfile for Backend

```dockerfile
# backend/Dockerfile
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

### Dockerfile for Open WebUI Frontend

```dockerfile
# frontend/Dockerfile
FROM ghcr.io/open-webui/open-webui:main

# Kopiuj niestandardowe komponenty i konfigurację
COPY ./src/lib/components /app/src/lib/components
COPY ./src/routes /app/src/routes
COPY ./src/lib/stores /app/src/lib/stores

# Zainstaluj dodatkowe zależności jeśli potrzebne
COPY package.json ./
RUN npm install

# Zbuduj aplikację
RUN npm run build

EXPOSE 8080
```

---

## 🚀 Development Scripts

### Package.json - Standard Scripts

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "dev:frontend": "cd frontend && npm run dev",
    "build": "tsc && tsc-alias",
    "build:frontend": "cd frontend && npm run build",
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

### Development Script (dev.sh)

```bash
#!/bin/bash
# scripts/dev.sh

echo "🚀 Uruchamianie środowiska deweloperskiego Langflow + Open WebUI..."

# Sprawdź czy Docker działa
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker nie działa. Uruchom Docker najpierw."
    exit 1
fi

# Utwórz .env jeśli nie istnieje
if [ ! -f .env ]; then
    echo "📝 Tworzenie pliku .env z szablonu..."
    cp .env.example .env
fi

# Zbuduj i uruchom serwisy
echo "🏗️  Budowanie i uruchamianie serwisów..."
docker-compose -f docker-compose.dev.yml up --build -d

# Poczekaj na bazę danych
echo "⏳ Oczekiwanie na gotowość bazy danych..."
until docker-compose -f docker-compose.dev.yml exec db pg_isready -U user -d langflow_node; do
    sleep 2
done

# Uruchom migracje
echo "🗄️  Uruchamianie migracji bazy danych..."
pnpm db:migrate

# Zainstaluj zależności jeśli potrzebne
if [ ! -d "node_modules" ]; then
    echo "📦 Instalowanie zależności..."
    pnpm install
fi

echo "✅ Środowisko deweloperskie jest gotowe!"
echo "🌐 Open WebUI: http://localhost:8080"
echo "🔧 Node.js API: http://localhost:3000"
echo "🔧 Langflow UI: http://localhost:7860"
echo "📊 Database Studio: pnpm db:studio"
echo "📝 Dokumentacja API: http://localhost:3000/docs"
```

*// Dodano komentarz: Używaj tego skryptu w połączeniu z pipelines CI/CD do automatyzacji budowy w Docker.*

---

## 🔒 Security and Performance

### Security Configuration

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
  timeWindow: '1 minute',
  message: 'Zbyt wiele żądań, spróbuj ponownie później'
});
```

### Performance Optimization - Redis Caching

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

## 🧪 Testing Standards

### Vitest Configuration

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

### Test Examples

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

  it('powinien utworzyć nowy przepływ', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/flows',
      payload: {
        name: 'Test Flow',
        description: 'Testowy przepływ'
      }
    });

    expect(response.statusCode).toBe(201);
    expect(response.json()).toMatchObject({
      name: 'Test Flow',
      description: 'Testowy przepływ'
    });
  });
});
```

---

## ⚙️ Code Generation Rules

### ✅ Mandatory Standards

1. **TypeScript strict mode** - always enabled
2. **Error handling** - custom error classes with Polish messages
3. **Zod validation** - for all inputs with Polish error messages
4. **Vitest tests** - comprehensive coverage with Polish descriptions
5. **Docker** - update docker-compose.yml for all new services
6. **Scripts** - create/update run scripts with Polish comments
7. **Logging** - structured format with Polish messages
8. **Dependency Injection** - better testability
9. **DB Migrations** - Prisma migrations
10. **Monitoring** - health checks with Polish status messages
11. **Redis caching** - for performance optimization
12. **Security** - rate limiting and security headers
13. **Open WebUI Frontend** - MANDATORY for all frontend development
14. **Polish Communication** - all user-facing messages in Polish

### 🎯 End Goal

Every code change should be:
- **Containerized** - ready for Docker deployment
- **Tested** - with full coverage and Polish test descriptions
- **Production-ready** - with proper integration to Langflow Python backend
- **Open WebUI Compatible** - frontend must use Open WebUI framework
- **Polish User Experience** - all interactions in Polish language

### 🚨 Critical Requirements

- **NEVER create custom frontend frameworks** - always use Open WebUI
- **ALWAYS respond to users in Polish** during conversations
- **ALWAYS include Polish comments** in generated code
- **ALWAYS update docker-compose.yml** when adding new services
- **ALWAYS create corresponding tests** for new functionality

---

*// Nowa sekcja:*

## 🔄 CI/CD Pipelines

### Recommended Setup
*Używaj pipelines CI/CD (np. GitHub Actions, GitLab CI lub Jenkins) do automatyzacji budowy całej aplikacji. Integruj z Docker i Docker Compose do tworzenia obrazów, testowania i deploymentu. Open WebUI musi być budowane jako część pipeline, z automatyczną integracją z Langflow dla AI flows. Przykładowy workflow:*

- **Triggers**: Na push do main lub pull requests.
- **Steps**:
  1. **Checkout code** i instalacja zależności (pnpm install).
  2. **Uruchom testy** (pnpm test) z coverage.
  3. **Buduj Docker images** za pomocą Dockerfile (docker build).
  4. **Orkiestruj z Docker Compose** (docker-compose up -d --build) do lokalnego testowania.
  5. **Deploy** do chmury (np. AWS, GCP) z push'em obrazów do registry.
  6. **Monitoruj** z użyciem narzędzi jak Prometheus, integrując z security checks.

### Example GitHub Actions Workflow (pipelines.yml)

```yaml
name: CI/CD Pipeline for Langflow + Open WebUI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Install dependencies
        run: pnpm install

      - name: Run tests
        run: pnpm test:coverage

      - name: Build Docker images
        run: docker build -t myapp-backend ./backend

      - name: Run Docker Compose
        run: docker-compose -f docker-compose.yml up -d --build

      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: |
          # Przykładowy deploy, np. do AWS ECR [[10]]
          aws ecr get-login-password --region region | docker login --username AWS --password-stdin account.dkr.ecr.region.amazonaws.com
          docker push account.dkr.ecr.region.amazonaws.com/myapp:latest
```

*To zapewnia automatyczną budowę całości, z fokusem na Docker, Open WebUI i Langflow dla repozytoriów AI.*

---

*Ostatnia aktualizacja: 18 lipca 2025*