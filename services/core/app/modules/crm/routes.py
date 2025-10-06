from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy.orm import Session
from ...security import get_current_user
from ...db import SessionLocal
from .models import Lead as LeadModel
from .schemas import LeadCreate, LeadOut

router = APIRouter(prefix="/crm", tags=["crm"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/leads", response_model=list[LeadOut])
def list_leads(db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = db.query(LeadModel).all()
    return items

@router.post("/leads", response_model=LeadOut)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = LeadModel(name=payload.name, email=payload.email, status=payload.status, tenant_id=user.tenant_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def register(app: FastAPI):
    app.include_router(router)
