def test_mock_payment_and_refund(client):
    # Create payment
    create = client.post("/payments", json={"provider":"mock","amount":999,"currency":"USD","customer_email":"x@y.com"})
    assert create.status_code == 200
    data = create.json()
    assert data["status"] in ("created", "succeeded")
    assert data["provider"] == "mock"
    assert data["amount"] == 999
    assert data["currency"] == "USD"
    assert data["provider_payment_id"]

    # Refund
    refund = client.post("/refunds", json={"provider":"mock","provider_payment_id": data["provider_payment_id"], "amount": 999})
    assert refund.status_code == 200
    rj = refund.json()
    assert rj["status"] == "refunded"
    assert rj["amount"] == 999
