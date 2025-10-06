from fastapi import APIRouter, FastAPI, Depends
from pydantic import BaseModel
from ...security import get_current_user

router = APIRouter(prefix="/crm", tags=["crm"])

class Lead(BaseModel):
    id: int | None = None
    name: str
    email: str | None = None
    status: str = "new"

LEADS_DB: list[Lead] = []

@router.get("/leads", response_model=list[Lead])
def list_leads(user=Depends(get_current_user)):
    return LEADS_DB

@router.post("/leads", response_model=Lead)
def create_lead(payload: Lead, user=Depends(get_current_user)):
    payload.id = (LEADS_DB[-1].id + 1) if LEADS_DB else 1
    LEADS_DB.append(payload)
    return payload


def register(app: FastAPI):
    app.include_router(router)
