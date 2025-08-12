from fastapi import FastAPI
from .api.routes_payments import router as payments_router
from .api.routes_webhooks import router as webhooks_router

app = FastAPI(title="Universal Payment Gateway Sandbox")

app.include_router(payments_router, tags=["payments"])
app.include_router(webhooks_router, tags=["webhooks"])

@app.get("/health")
def health():
    return {"status": "ok"}
