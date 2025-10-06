.PHONY: up down logs core-logs bootstrap token demo frontend-dev core-dev

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

core-logs:
	docker compose logs -f core

bootstrap:
	curl -X POST http://localhost:8000/auth/bootstrap || true

# Prints only the access token
token:
	@curl -s -X POST http://localhost:8000/auth/login \
	  -H "Content-Type: application/x-www-form-urlencoded" \
	  -d "username=admin@bframe.local&password=admin123" \
	  | python3 -c 'import sys,json;print(json.load(sys.stdin).get("access_token",""))'

demo: bootstrap
	@TOKEN=$$(make -s token); \
	echo "TOKEN=$$TOKEN"; \
	curl -s -X POST http://localhost:8000/crm/leads \
	  -H "Authorization: Bearer $$TOKEN" -H "Content-Type: application/json" \
	  -d '{"name":"Demo Lead","email":"demo@example.com"}'; echo; \
	curl -s -H "Authorization: Bearer $$TOKEN" http://localhost:8000/crm/leads; echo;

# Local dev without Docker
frontend-dev:
	cd apps/frontend && npm install && NEXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev

core-dev:
	cd services/core && python -m venv .venv && . .venv/bin/activate && \
	pip install -r requirements.txt && uvicorn app.main:app --reload
