from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..security import get_db, get_current_user
from ..schemas.tenant import TenantCreate, TenantOut
from ..models.tenant import Tenant

router = APIRouter()

@router.get("/", response_model=list[TenantOut])
def list_tenants(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Tenant).all()

@router.post("/", response_model=TenantOut)
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = Tenant(name=payload.name, slug=payload.slug)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t
