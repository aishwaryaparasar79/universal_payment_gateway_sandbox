from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

class PaymentCreate(BaseModel):
    provider: Literal["mock", "stripe"]
    amount: int = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    customer_email: Optional[EmailStr] = None
    payment_method: Optional[str] = None  # used for stripe confirm in server-side flows

class PaymentOut(BaseModel):
    id: str
    provider: str
    provider_payment_id: str | None
    status: str
    amount: int
    currency: str
    customer_email: str | None

class RefundRequest(BaseModel):
    provider: Literal["mock", "stripe"]
    provider_payment_id: str
    amount: int = Field(gt=0)

class WebhookEvent(BaseModel):
    type: str
    data: dict
