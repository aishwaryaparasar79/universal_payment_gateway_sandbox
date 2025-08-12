# Universal Payment Gateway Sandbox

A client-style demo that exposes a **single, unified payments API** with **pluggable providers**
(Stripe + Mock adapter), **idempotency keys**, **webhooks**, and a minimal domain model.
This is a *portfolio-quality* sample to showcase architecture, testing, and reliability patterns
you would deliver to freelance clients.

> ⚠️ Test-mode only. Do **not** use in production.

## Features

- Unified API across providers (`stripe`, `mock`)
- Create payment intents, confirm, capture, refund
- **Idempotency**: safe retries using an `Idempotency-Key` header
- Webhook ingestion (+ signature verification for Stripe if secrets provided)
- SQLAlchemy + SQLite (simple) with optional Postgres via Docker
- CI-ready structure, tests, and typed FastAPI app
- Clear separation: `adapters/`, `services/`, `api/`

## Quickstart

### 1) Clone & install

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2) (Optional) Add Stripe test keys

Edit `.env`:

```
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx   # If you plan to verify signatures locally
```

If you don’t set `STRIPE_SECRET_KEY`, the Stripe adapter is disabled and you can use the `mock` adapter.

### 3) Run the API

```bash
uvicorn app.main:app --reload
```

Open docs at: http://127.0.0.1:8000/docs

### 4) Example usage

Create a payment with idempotency (header is optional but recommended):

```bash
curl -X POST http://127.0.0.1:8000/payments \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 7b6a1e4b-8d4a-4c9d-a0a7-1d8c42e3b111" \
  -d '{"provider":"mock","amount":1299,"currency":"USD","customer_email":"demo@example.com"}'
```

Refund (mock):

```bash
curl -X POST http://127.0.0.1:8000/refunds \
  -H "Content-Type: application/json" \
  -d '{"provider":"mock","provider_payment_id":"<returned_from_create>","amount":1299}'
```

### 5) Webhooks

- Stripe: expose `/webhooks/stripe` (set your endpoint in Stripe CLI or dashboard)
- Mock: `/webhooks/mock` just accepts a generic event shape for testing

## Design

- **Adapters** implement a common interface: `create_payment`, `refund_payment`.
- **Service** layer applies idempotency and persists Payment entities.
- **API** layer validates input/output with Pydantic models.
- **Idempotency** persists request hash + response; repeat key returns the original result without re-executing side-effects.

## Run tests

```bash
pytest -q
```

## Docker (optional)

A Postgres + API compose is included for production-like runs:

```bash
docker compose up --build
```

Then set `DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/payments`
in `.env` and restart.

## Roadmap

- Add capture & partial refund flows for Stripe
- Add UI admin (React) with basic metrics
- Add more providers (Razorpay, Adyen) behind the same interface
