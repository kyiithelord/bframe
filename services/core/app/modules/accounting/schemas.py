from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class InvoiceItemIn(BaseModel):
    description: str
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)

class InvoiceCreate(BaseModel):
    number: str
    customer_name: str
    issue_date: date
    due_date: Optional[date] = None
    currency: str = "USD"
    notes: Optional[str] = None
    items: List[InvoiceItemIn] = []

class InvoiceOutItem(BaseModel):
    id: int
    description: str
    quantity: float
    unit_price: float
    line_total: float
    class Config:
        from_attributes = True

class InvoiceOut(BaseModel):
    id: int
    number: str
    customer_name: str
    status: str
    issue_date: date
    due_date: Optional[date]
    currency: str
    notes: Optional[str]
    total: float
    items: List[InvoiceOutItem] = []
    class Config:
        from_attributes = True

class PaymentIn(BaseModel):
    amount: float = Field(gt=0)
    method: Optional[str] = None

class PaymentOut(BaseModel):
    id: int
    amount: float
    method: Optional[str]
    paid_at: datetime
    class Config:
        from_attributes = True
