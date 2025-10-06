from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..security import get_db, get_current_user
from ..models.module import ModuleRegistration
from ..schemas.module import ModuleOut

router = APIRouter()

@router.get("/", response_model=list[ModuleOut])
def list_modules(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(ModuleRegistration).all()
