from typing import Optional
import stripe
from ..config import settings

class StripeAdapter:
    def __init__(self) -> None:
        self.secret = settings.stripe_secret_key
        if self.secret:
            stripe.api_key = self.secret

    def is_enabled(self) -> bool:
        return bool(self.secret)

    def create_payment(self, *, amount: int, currency: str, customer_email: Optional[str], payment_method: Optional[str]) -> dict:
        if not self.is_enabled():
            raise RuntimeError("Stripe adapter not configured")
        # Using PaymentIntents for test-mode demo. Confirm immediately if payment_method is provided.
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency.lower(),
            receipt_email=customer_email,
            payment_method=payment_method,
            confirm=bool(payment_method),
            automatic_payment_methods=None if payment_method else {"enabled": True},
        )
        return intent.to_dict()

    def refund_payment(self, *, provider_payment_id: str, amount: int) -> dict:
        if not self.is_enabled():
            raise RuntimeError("Stripe adapter not configured")
        refund = stripe.Refund.create(
            payment_intent=provider_payment_id,
            amount=amount
        )
        return refund.to_dict()
