from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..security import get_db, get_current_user
from ..rbac import require_any_permission
from ..models.rbac import AuditLog

router = APIRouter(prefix="/admin", tags=["admin"]) 

@router.get("/audit")
def list_audit(db: Session = Depends(get_db), user=Depends(get_current_user), perm=Depends(require_any_permission("audit.read"))):
    rows = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(200).all()
    # return basic fields only
    return [
        {
            "id": r.id,
            "actor_user_id": r.actor_user_id,
            "action": r.action,
            "entity": r.entity,
            "entity_id": r.entity_id,
            "meta": r.meta,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
