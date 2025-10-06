from pydantic import BaseModel

class TenantCreate(BaseModel):
    name: str
    slug: str

class TenantOut(BaseModel):
    id: int
    name: str
    slug: str
    class Config:
        from_attributes = True
