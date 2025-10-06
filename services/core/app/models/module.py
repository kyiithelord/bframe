from sqlalchemy import Column, Integer, String, Boolean
from .base import Base

class ModuleRegistration(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    enabled = Column(Boolean, default=True)
    version = Column(String(50), default="0.1.0")
