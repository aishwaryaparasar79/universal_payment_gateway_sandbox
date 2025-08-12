def test_idempotency_returns_same_response(client):
    payload = {
        "provider": "mock",
        "amount": 1500,
        "currency": "USD",
        "customer_email": "a@b.com"
    }
    headers = {"Idempotency-Key": "fixed-key-123"}

    r1 = client.post("/payments", json=payload, headers=headers)
    r2 = client.post("/payments", json=payload, headers=headers)
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json() == r2.json()  # identical cached response
