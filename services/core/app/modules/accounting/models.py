from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ...models.base import Base


class Invoice(Base):
    __tablename__ = "acc_invoices"
    id = Column(Integer, primary_key=True)
    number = Column(String(50), unique=True, nullable=False)
    customer_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="draft")  # draft, sent, paid, overdue, void
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)
    currency = Column(String(10), nullable=False, default="USD")
    notes = Column(Text, nullable=True)
    total = Column(Numeric(12,2), nullable=False, default=0)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    items = relationship("InvoiceItem", cascade="all, delete-orphan", backref="invoice")
    payments = relationship("Payment", cascade="all, delete-orphan", backref="invoice")


class InvoiceItem(Base):
    __tablename__ = "acc_invoice_items"
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("acc_invoices.id"), nullable=False)
    description = Column(String(255), nullable=False)
    quantity = Column(Numeric(10,2), nullable=False, default=1)
    unit_price = Column(Numeric(12,2), nullable=False, default=0)
    line_total = Column(Numeric(12,2), nullable=False, default=0)


class Payment(Base):
    __tablename__ = "acc_payments"
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("acc_invoices.id"), nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    method = Column(String(50), nullable=True)
    paid_at = Column(DateTime, default=datetime.utcnow, nullable=False)
