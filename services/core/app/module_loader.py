import importlib
import pkgutil
from pathlib import Path
from fastapi import FastAPI
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models.module import ModuleRegistration

MODULES_PATH = Path(__file__).parent / "modules"


def load_modules(app: FastAPI):
    MODULES_PATH.mkdir(parents=True, exist_ok=True)
    db: Session = SessionLocal()
    try:
        for finder, name, ispkg in pkgutil.iter_modules([str(MODULES_PATH)]):
            module_pkg = f"app.modules.{name}.routes"
            try:
                mod = importlib.import_module(module_pkg)
                if hasattr(mod, "register"):
                    mod.register(app)
                # ensure module registration in DB
                existing = db.query(ModuleRegistration).filter(ModuleRegistration.name == name).first()
                if not existing:
                    db.add(ModuleRegistration(name=name, enabled=True, version="0.1.0"))
                    db.commit()
            except Exception as e:
                print(f"Failed loading module {name}: {e}")
    finally:
        db.close()
