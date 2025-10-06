#!/bin/sh
set -e

# Wait for Postgres
python - <<'PY'
import time, os
import psycopg2
url=os.environ.get('DATABASE_URL','')
# crude wait loop
for i in range(30):
    try:
        import urllib.parse as up
        up.use = up
        # Parse psycopg2 DSN
        if url.startswith('postgresql'):
            pass
        conn=psycopg2.connect(url.replace('+psycopg2',''))
        conn.close()
        break
    except Exception as e:
        time.sleep(1)
else:
    raise SystemExit('DB not ready')
PY

# Run migrations
alembic upgrade head || true

# Start API
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
