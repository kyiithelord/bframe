from pydantic import BaseModel

class ModuleOut(BaseModel):
    id: int
    name: str
    enabled: bool
    version: str
    class Config:
        from_attributes = True
