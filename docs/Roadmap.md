# Technical Roadmap

## Team & Roles
- **Founding Eng (Backend)**: Core engine, module loader, events
- **Founding Eng (Frontend)**: Design system, dashboards, module UIs
- **Infra/SRE**: CI/CD, K8s, observability, security baseline
- **Data/ML**: AI assistant, embeddings, RAG pipelines
- **PM/Designer**: UX for workflows, automation studio

## Milestones
- **M0 — Foundations (Weeks 0–2)**
  - Repo scaffolding, CI, code quality gates
  - Auth service (Keycloak/JWT), tenant model
  - Core engine skeleton, event bus integration
- **M1 — Core + CRM (Weeks 3–6)**
  - Module registry/loader
  - CRM module (leads, pipeline)
  - Basic dashboards, audit logging
- **M2 — Sales + Accounting (Weeks 7–10)**
  - Quotes → Orders → Invoices
  - Accounting ledger, taxes
  - Search service, file storage
- **M3 — Inventory + HR (Weeks 11–14)**
  - Stock, POs, supplier mgmt
  - HR records, attendance, payroll basics
- **M4 — AI Assistant v1 + Automation (Weeks 15–18)**
  - Chat UI, prompt router, tool calls
  - No-code workflow builder MVP
- **M5 — Hardening & SaaS Beta (Weeks 19–22)**
  - Observability, RBAC refinement, rate limits
  - Billing, usage metering, SaaS control plane

## Non-Functional Requirements
- p95 < 300ms for typical API calls
- Multi-tenant isolation (row-level security per tenant)
- Zero-downtime deploys; SLO: 99.9%
- Data export/import paths; backups and DR drills

## Deliverables by Phase
- Design docs per service, ADRs
- API specs (OpenAPI), contract tests
- Runbooks, dashboards, alerts
