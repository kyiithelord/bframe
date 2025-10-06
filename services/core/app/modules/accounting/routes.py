from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from decimal import Decimal
from ...db import SessionLocal
from ...security import get_current_user
from ...mq import publish
from .models import Invoice, InvoiceItem, Payment
from .schemas import InvoiceCreate, InvoiceOut, InvoiceOutItem, PaymentIn, PaymentOut

router = APIRouter(prefix="/accounting", tags=["accounting"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def compute_totals(inv: Invoice):
    total = Decimal("0.00")
    for it in inv.items:
        it.line_total = (it.quantity or 0) * (it.unit_price or 0)
        total += Decimal(str(it.line_total))
    inv.total = total


@router.get("/invoices", response_model=list[InvoiceOut])
def list_invoices(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.execute(select(Invoice).order_by(Invoice.id.desc())).scalars().all()
    return rows


@router.post("/invoices", response_model=InvoiceOut)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if db.query(Invoice).filter(Invoice.number == payload.number).first():
        raise HTTPException(status_code=400, detail="Invoice number already exists")
    inv = Invoice(
        number=payload.number,
        customer_name=payload.customer_name,
        issue_date=payload.issue_date,
        due_date=payload.due_date,
        currency=payload.currency,
        notes=payload.notes,
        status="draft",
        tenant_id=user.tenant_id,
    )
    for item in payload.items:
        inv.items.append(
            InvoiceItem(description=item.description, quantity=item.quantity, unit_price=item.unit_price)
        )
    compute_totals(inv)
    db.add(inv)
    db.commit()
    db.refresh(inv)
    # publish event
    try:
        import asyncio
        asyncio.get_event_loop().create_task(publish("invoice.created", {"id": inv.id, "number": inv.number}))
    except Exception:
        pass
    return inv


@router.post("/invoices/{invoice_id}/payments", response_model=PaymentOut)
def add_payment(invoice_id: int, payload: PaymentIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    inv = db.get(Invoice, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    pay = Payment(invoice_id=invoice_id, amount=payload.amount, method=payload.method)
    db.add(pay)
    # status update
    paid_sum = sum([float(p.amount) for p in inv.payments]) + float(payload.amount)
    if paid_sum >= float(inv.total):
        inv.status = "paid"
    db.commit()
    db.refresh(pay)
    try:
        import asyncio
        asyncio.get_event_loop().create_task(publish("invoice.paid", {"id": inv.id, "amount": float(payload.amount)}))
    except Exception:
        pass
    return pay


def register(app: FastAPI):
    app.include_router(router)
