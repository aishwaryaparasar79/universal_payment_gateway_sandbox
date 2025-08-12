from sqlalchemy import String, Integer, DateTime, JSON, Enum, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base
import enum
import uuid

class PaymentStatus(str, enum.Enum):
    created = "created"
    succeeded = "succeeded"
    failed = "failed"
    refunded = "refunded"

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider: Mapped[str] = mapped_column(String, nullable=False)
    provider_payment_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    customer_email: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.created, nullable=False)
    raw_provider_response: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    request_fingerprint: Mapped[str] = mapped_column(String, nullable=False)
    response_cache: Mapped[dict] = mapped_column(JSON, default=dict)
    __table_args__ = (UniqueConstraint("key", name="uq_idempotency_key"),)
