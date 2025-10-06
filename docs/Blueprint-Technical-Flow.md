# Blueprint — Technical Flow (Architect’s View)

## 1. System Architecture Overview
- **Core Engine**: Auth, DB abstraction, API gateway, event bus, module loader
- **Modules**: Independently developed services/plugins that register routes, models, permissions
- **Data**: PostgreSQL (multi-tenant), Redis cache, S3/MinIO storage, Search (Elasticsearch/Meilisearch)
- **Messaging**: RabbitMQ/Kafka for async events
- **AI Services**: OpenAI + Local LLMs (Ollama/HF)

High-level flow:
```
[Frontend Apps]
      ↓
[API Gateway + Auth Layer]
      ↓
[Core Engine] — [Modules]
      ↓
[DB Cluster + File Storage + AI Services]
```

## 2. Tech Stack
- **Frontend**: Next.js (React, TailwindCSS)
- **Backend**: FastAPI (Python) or NestJS (Node.js)
- **Database**: PostgreSQL + Redis
- **Queue**: RabbitMQ / Kafka
- **Search**: Elasticsearch / Meilisearch
- **Storage**: AWS S3 / MinIO
- **Auth**: Keycloak or JWT + RBAC
- **AI**: OpenAI API + Local LLMs (Ollama/HuggingFace)
- **Infra**: Docker + Kubernetes, GitHub Actions, Prometheus + Grafana

## 3. Core Framework Components
- **User & Role Management**
  - JWT/OAuth2, RBAC, multi-tenant (company workspaces)
- **Module Loader**
  - Each module is an independent repo/package
  - Registers routes/models/permissions dynamically
  - Example: `register_module("crm", routes=["/leads", "/clients"])`
- **Event Bus / Hooks**
  - Pub/Sub for cross-module comms (e.g., `invoice_created`)
- **Workflow Engine**
  - YAML or visual definitions; AI suggests automations
- **AI Assistant Layer**
  - Chat UI issuing API calls across modules; retrieval over unified schema

## 4. AI Integration Plan
- **Stage 1**: Copilot for CRM & Accounting (generate emails, suggest actions)
- **Stage 2**: Conversational dashboards (e.g., “Show sales last week by region”)
- **Stage 3**: Predictive analytics (churn, LTV, demand forecasting)
- **Stage 4**: Autonomous workflows (late payment reminder + task creation)

## 5. Developer Flow (Framework Logic)
Directory structure (proposed):
```
/modules
 ├── crm/
 │   ├── models.py
 │   ├── routes.py
 │   ├── services.py
 │   └── ai_prompts.yaml
 ├── accounting/
 ├── hr/
 └── inventory/
```
Each module exports schema, endpoints, UI widgets, AI prompts/actions.

## 6. Example Data Flow — Creating an Invoice
1. Frontend POST → API Gateway (authn/z)
2. Gateway routes to Accounting service
3. Accounting creates record → emits `invoice_created`
4. CRM subscribed → updates client status
5. AI service suggests follow-up email
6. Frontend updates dashboard

## 7. Hosting & Scalability
- Early: Docker on Render/Railway/Lightsail
- Scale: K8s (EKS/DOKS), load balancer, HPA, read replicas, shard per-tenant as needed

## 8. Security & Compliance
- TLS, OAuth2/SSO, encrypted at rest (PG + KMS), audit logs
- Data residency controls; PII minimization; DLP scanning for AI prompts
- GDPR/SOC2 readiness; secrets management (Vault/SSM)

## 9. Minimal Core API (illustrative)
- `POST /auth/login`, `GET /tenants`, `POST /tenants`
- `GET /modules`, `POST /modules/install`, `POST /modules/permissions`
- `POST /events/publish`, `GET /events/subscriptions`
- `POST /workflows/execute`, `POST /workflows/definitions`
- `POST /ai/query`, `POST /ai/agents/:id/act`

## 10. Observability
- Structured logging (JSON), trace IDs propagated across services
- Metrics (Prometheus): RPS, p95 latency, error rate, queue lag, workflow runtime
- Tracing (OTel + Tempo/Jaeger)
