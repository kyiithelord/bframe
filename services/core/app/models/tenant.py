from sqlalchemy import Column, Integer, String, UniqueConstraint
from .base import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    __table_args__ = (UniqueConstraint('slug', name='uq_tenant_slug'),)
