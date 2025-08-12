import uuid
from typing import Optional

class MockAdapter:
    """A fake provider for local testing and deterministic demos."""
    def __init__(self) -> None:
        self._enabled = True

    def is_enabled(self) -> bool:
        return self._enabled

    def create_payment(self, *, amount: int, currency: str, customer_email: Optional[str], payment_method: Optional[str]) -> dict:
        # Simulate success
        return {
            "id": f"mock_{uuid.uuid4().hex[:12]}",
            "status": "succeeded",
            "amount": amount,
            "currency": currency,
            "receipt_email": customer_email,
        }

    def refund_payment(self, *, provider_payment_id: str, amount: int) -> dict:
        return {
            "id": f"mock_ref_{uuid.uuid4().hex[:12]}",
            "status": "refunded",
            "amount": amount,
            "provider_payment_id": provider_payment_id,
        }
