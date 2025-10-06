from pydantic import BaseModel

class LeadCreate(BaseModel):
    name: str
    email: str | None = None
    status: str = "new"

class LeadOut(BaseModel):
    id: int
    name: str
    email: str | None = None
    status: str
    class Config:
        from_attributes = True
