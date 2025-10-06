from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..security import get_current_user

router = APIRouter()

class AIQuery(BaseModel):
    query: str

@router.post("/query")
def ai_query(payload: AIQuery, user=Depends(get_current_user)):
    # TODO: wire to OpenAI/Local LLM via tools
    return {"answer": f"Stub: you asked '{payload.query}'"}
