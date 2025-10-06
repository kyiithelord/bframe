from sqlalchemy.orm import Session
from .models.rbac import AuditLog
import json

def log_action(db: Session, *, actor_user_id: int | None, action: str, entity: str | None = None, entity_id: str | None = None, meta: dict | None = None):
    rec = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        entity=entity,
        entity_id=str(entity_id) if entity_id is not None else None,
        meta=json.dumps(meta or {}) if meta else None,
    )
    db.add(rec)
    db.commit()
