from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from ...security import get_current_user
from ...db import SessionLocal
from .models import Lead as LeadModel
from .schemas import LeadCreate, LeadOut, LeadUpdate, LeadQuery
from ...rbac import require_permission
from ...audit import log_action

router = APIRouter(prefix="/crm", tags=["crm"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/leads", response_model=list[LeadOut])
def list_leads(
    page: int = 1,
    size: int = 10,
    status: str | None = None,
    search: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    perm=Depends(require_permission("crm.read")),
):
    q = db.query(LeadModel)
    if status:
        q = q.filter(LeadModel.status == status)
    if search:
        like = f"%{search}%"
        q = q.filter((LeadModel.name.ilike(like)) | (LeadModel.email.ilike(like)))
    if sort:
        if sort.startswith("-"):
            field = sort[1:]
            q = q.order_by(desc(getattr(LeadModel, field, LeadModel.id)))
        else:
            q = q.order_by(asc(getattr(LeadModel, sort, LeadModel.id)))
    else:
        q = q.order_by(LeadModel.id.desc())
    page = max(1, page)
    size = max(1, min(size, 100))
    items = q.offset((page - 1) * size).limit(size).all()
    return items

@router.post("/leads", response_model=LeadOut)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db), user=Depends(get_current_user), perm=Depends(require_permission("crm.write"))):
    obj = LeadModel(name=payload.name, email=payload.email, status=payload.status, tenant_id=user.tenant_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    log_action(db, actor_user_id=user.id, action="lead.create", entity="lead", entity_id=obj.id, meta={"name": obj.name})
    return obj

@router.put("/leads/{lead_id}", response_model=LeadOut)
def replace_lead(lead_id: int, payload: LeadCreate, db: Session = Depends(get_db), user=Depends(get_current_user), perm=Depends(require_permission("crm.write"))):
    obj = db.get(LeadModel, lead_id)
    if not obj:
        return {}
    obj.name = payload.name
    obj.email = payload.email
    obj.status = payload.status
    db.commit()
    db.refresh(obj)
    log_action(db, actor_user_id=user.id, action="lead.update", entity="lead", entity_id=obj.id)
    return obj

@router.patch("/leads/{lead_id}", response_model=LeadOut)
def patch_lead(lead_id: int, payload: LeadUpdate, db: Session = Depends(get_db), user=Depends(get_current_user), perm=Depends(require_permission("crm.write"))):
    obj = db.get(LeadModel, lead_id)
    if not obj:
        return {}
    if payload.name is not None:
        obj.name = payload.name
    if payload.email is not None:
        obj.email = payload.email
    if payload.status is not None:
        obj.status = payload.status
    db.commit()
    db.refresh(obj)
    log_action(db, actor_user_id=user.id, action="lead.patch", entity="lead", entity_id=obj.id)
    return obj

@router.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db), user=Depends(get_current_user), perm=Depends(require_permission("crm.write"))):
    obj = db.get(LeadModel, lead_id)
    if not obj:
        return {"deleted": 0}
    db.delete(obj)
    db.commit()
    log_action(db, actor_user_id=user.id, action="lead.delete", entity="lead", entity_id=lead_id)
    return {"deleted": 1}


def register(app: FastAPI):
    app.include_router(router)
