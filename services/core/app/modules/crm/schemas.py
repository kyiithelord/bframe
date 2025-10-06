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

class LeadUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    status: str | None = None

class LeadQuery(BaseModel):
    page: int = 1
    size: int = 10
    status: str | None = None
    search: str | None = None
    sort: str | None = None  # e.g., 'name' or '-id'
