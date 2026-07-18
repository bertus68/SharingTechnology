# tests/test_router.py

from fastapi import FastAPI
from fastapi.testclient import TestClient

from sharing_platform.router import router
import sharing_platform.router as router_module


app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_get_utenti_route(monkeypatch):
    monkeypatch.setattr(router_module, "get_utenti", lambda: [])

    res = client.get("/api/utenti")

    assert res.status_code == 200
    assert res.json() == []


def test_create_utente_route(monkeypatch):
    captured = {}

    def fake_create(nome, email, password_hash, metodo_pagamento):
        captured["data"] = (nome, email, password_hash, metodo_pagamento)

    monkeypatch.setattr(router_module, "create_utente", fake_create)

    payload = {
        "nome": "Mario",
        "email": "mario@test.com",
        "password_hash": "hash1",
        "metodo_pagamento": "tok1"
    }

    res = client.post("/api/utenti", json=payload)

    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

    assert captured["data"] == (
        "Mario",
        "mario@test.com",
        "hash1",
        "tok1",
    )


def test_create_utente_route_missing_fields():
    app2 = FastAPI()
    app2.include_router(router)
    client2 = TestClient(app2)

    res = client2.post("/api/utenti", json={})

    assert res.status_code == 500