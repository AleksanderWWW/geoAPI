def test_status(client):
    response = client.get("/status")
    assert response.json["status"] == "ok"
    assert response.status_code == 200
