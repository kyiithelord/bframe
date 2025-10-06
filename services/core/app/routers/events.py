from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..security import get_current_user
from ..mq import publish

router = APIRouter()

class EventIn(BaseModel):
    routing_key: str
    payload: dict

@router.post("/publish")
async def publish_event(event: EventIn, user=Depends(get_current_user)):
    await publish(event.routing_key, event.payload)
    return {"status": "queued", "routing_key": event.routing_key}

@router.get("/subscriptions")
async def list_subscriptions(user=Depends(get_current_user)):
    # Placeholder: would return dynamic subscriptions in future
    return {"subscriptions": ["#"]}
