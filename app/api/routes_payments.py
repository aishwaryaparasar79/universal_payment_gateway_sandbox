from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from ..db import get_db, Base, engine
from ..schemas import PaymentCreate, PaymentOut, RefundRequest
from ..services.payment_service import PaymentService

# Ensure tables exist on first import (simple demo)
Base.metadata.create_all(bind=engine)

router = APIRouter()
svc = PaymentService()

@router.post("/payments", response_model=PaymentOut)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db), idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    response = svc.create_payment(
        db,
        provider=payload.provider,
        amount=payload.amount,
        currency=payload.currency,
        customer_email=payload.customer_email,
        payment_method=payload.payment_method,
        idem_key=idempotency_key,
        payload_for_fp=payload.model_dump()
    )
    return response

@router.post("/refunds")
def refund_payment(payload: RefundRequest, db: Session = Depends(get_db)):
    return svc.refund(db, provider=payload.provider, provider_payment_id=payload.provider_payment_id, amount=payload.amount)
