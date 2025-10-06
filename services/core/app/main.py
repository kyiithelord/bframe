import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_db
from .routers import auth, tenants, modules, events, workflows, ai
from .routers import search, files
from .routers import admin_audit
from .module_loader import load_modules
from .mq import start_background_consumer

app = FastAPI(title="BFrame Core", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    init_db()
    load_modules(app)
    loop = asyncio.get_event_loop()
    await start_background_consumer(loop)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
app.include_router(modules.router, prefix="/modules", tags=["modules"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(admin_audit.router)
app.include_router(search.router)
app.include_router(files.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
