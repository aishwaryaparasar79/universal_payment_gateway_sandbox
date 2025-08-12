from sqlalchemy.orm import Session
from typing import Optional
from ..models import Payment, PaymentStatus
from ..adapters.mock_adapter import MockAdapter
from ..adapters.stripe_adapter import StripeAdapter
from . import idempotency as idem

class PaymentService:
    def __init__(self) -> None:
        self.adapters = {
            "mock": MockAdapter(),
            "stripe": StripeAdapter(),
        }

    def create_payment(self, db: Session, *, provider: str, amount: int, currency: str, customer_email: Optional[str], payment_method: Optional[str], idem_key: Optional[str], payload_for_fp: dict) -> dict:
        adapter = self.adapters.get(provider)
        if adapter is None:
            raise ValueError("Unsupported provider")

        # Idempotency: check cache
        if idem_key:
            cached = idem.get_cached_response(db, idem_key, payload_for_fp)
            if cached is not None:
                return cached

        provider_resp = adapter.create_payment(amount=amount, currency=currency, customer_email=customer_email, payment_method=payment_method)
        status_str = provider_resp.get("status", "created")
        status = PaymentStatus(status_str) if status_str in PaymentStatus.__members__.values() else PaymentStatus.created
        provider_payment_id = provider_resp.get("id")

        payment = Payment(
            provider=provider,
            provider_payment_id=provider_payment_id,
            amount=amount,
            currency=currency.upper(),
            customer_email=customer_email,
            status=status,
            raw_provider_response=provider_resp,
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)

        response = {
            "id": payment.id,
            "provider": payment.provider,
            "provider_payment_id": payment.provider_payment_id,
            "status": payment.status.value,
            "amount": payment.amount,
            "currency": payment.currency,
            "customer_email": payment.customer_email,
        }

        if idem_key:
            idem.store_response(db, idem_key, payload_for_fp, response)

        return response

    def refund(self, db: Session, *, provider: str, provider_payment_id: str, amount: int) -> dict:
        adapter = self.adapters.get(provider)
        if adapter is None:
            raise ValueError("Unsupported provider")
        provider_resp = adapter.refund_payment(provider_payment_id=provider_payment_id, amount=amount)
        return provider_resp
