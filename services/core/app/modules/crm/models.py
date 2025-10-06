from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ...models.base import Base


class Lead(Base):
    __tablename__ = "crm_leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="new")
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)

    tenant = relationship("Tenant")
