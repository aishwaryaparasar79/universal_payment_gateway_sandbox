# Universal Payment Gateway Sandbox

A unified payments API with **pluggable providers** (Stripe + Mock), **idempotency** via `Idempotency-Key`,
and **webhooks**—built with FastAPI, SQLAlchemy, and Docker. Ideal as a portfolio piece and a client-style demo.

> ⚠️ Test-mode only. Do **not** use in production.

## Features
- Consistent **create → confirm/capture → refund** flows across providers
- Providers: **Stripe** (test keys) and **Mock** (deterministic success)
- **Idempotency**: deduplicate retries using `Idempotency-Key`
- **Webhooks**: Stripe endpoint with optional signature verification; mock endpoint for testing
- SQLite by default; optional **Postgres** via Docker Compose
- Typed Pydantic schemas, pytest suite, and GitHub Actions CI

## Quickstart
```bash
# 1) Setup
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# 2) (optional) Add Stripe test keys to .env
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_WEBHOOK_SECRET=whsec_...

# 3) Run API
uvicorn app.main:app --reload
# Open docs: http://127.0.0.1:8000/docs
