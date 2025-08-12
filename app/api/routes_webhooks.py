from fastapi import APIRouter, Request, HTTPException
from ..config import settings
import stripe

router = APIRouter()

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    if settings.stripe_webhook_secret:
        try:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header, secret=settings.stripe_webhook_secret
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        # If no secret configured, accept as-is in test mode
        event = (await request.json())

    # TODO: update Payment records based on event['type']
    return {"received": True}

@router.post("/webhooks/mock")
async def mock_webhook(request: Request):
    _ = await request.json()
    return {"received": True}
