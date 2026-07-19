"""
Unit and integration tests for router endpoints.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from sharing_platform.router import router
import sharing_platform.router as router_module


app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_get_utenti_route(monkeypatch):
    """Test standard retrieval of users through API."""
    monkeypatch.setattr(router_module, "get_utenti", lambda: [])

    res = client.get("/api/utenti")

    assert res.status_code == 200
    assert res.json() == []


def test_create_utente_route(monkeypatch):
    """Test user creation API."""
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
    """Test missing fields trigger 500 error on API."""
    app2 = FastAPI()
    app2.include_router(router)
    client2 = TestClient(app2)

    res = client2.post("/api/utenti", json={})

    assert res.status_code == 500


def test_details_route_not_found(monkeypatch):
    """Test 404 is returned when an object details request does not exist."""
    monkeypatch.setattr(router_module, "get_oggetto_con_prenotazione_by_id", lambda obj_id: None)

    res = client.get("/oggetti/999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Oggetto non trovato"


def test_prenota_oggetto_not_found(monkeypatch):
    """Test 404 is returned when trying to book a non-existent object."""
    monkeypatch.setattr(router_module, "get_oggetto_con_prenotazione_by_id", lambda obj_id: None)

    # Impostiamo cookie utente per saltare il redirect di login
    client.cookies.set("user_email", "mario@test.com")
    fake_user = {
        "id": 1, "nome": "Mario", "email": "mario@test.com",
        "password_hash": "hash1", "metodo_pagamento": "tok1"
    }
    monkeypatch.setattr(router_module, "get_utente_by_email", lambda email: fake_user)

    res = client.post(
        "/oggetti/999/prenota",
        data={"data_inizio": "2026-06-01", "data_fine": "2026-06-10"}
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Oggetto non trovato"


def test_prenota_oggetto_already_booked(monkeypatch):
    """Test 400 is returned when booking an object that is already booked."""
    # Simuliamo un oggetto non disponibile
    fake_row = {
        "id": 1,
        "nome": "Trapano",
        "descrizione": "Pro",
        "categoria": "tool",
        "disponibilita": 0,  # non disponibile
        "id_proprietario": 1,
        "stato": "Prenotato",
        "immagine_url1": "",
        "immagine_url2": "",
        "descrizione_breve": "",
        "descrizione_lunga": "",
    }
    monkeypatch.setattr(router_module, "get_oggetto_con_prenotazione_by_id", lambda obj_id: fake_row)
    client.cookies.set("user_email", "mario@test.com")
    fake_user = {
        "id": 1, "nome": "Mario", "email": "mario@test.com",
        "password_hash": "hash1", "metodo_pagamento": "tok1"
    }
    monkeypatch.setattr(router_module, "get_utente_by_email", lambda email: fake_user)

    res = client.post("/oggetti/1/prenota", data={"data_inizio": "2026-06-01", "data_fine": "2026-06-10"})
    assert res.status_code == 400
    assert res.json()["detail"] == "Oggetto non disponibile per la prenotazione"


def test_prenota_oggetto_invalid_dates(monkeypatch):
    """Test 400 is returned when booking dates are invalid."""
    # Simuliamo un oggetto disponibile
    fake_row = {
        "id": 1,
        "nome": "Trapano",
        "descrizione": "Pro",
        "categoria": "tool",
        "disponibilita": 1,
        "id_proprietario": 1,
        "stato": "Disponibile",
        "immagine_url1": "",
        "immagine_url2": "",
        "descrizione_breve": "",
        "descrizione_lunga": "",
    }
    monkeypatch.setattr(router_module, "get_oggetto_con_prenotazione_by_id", lambda obj_id: fake_row)
    client.cookies.set("user_email", "mario@test.com")
    fake_user = {
        "id": 1, "nome": "Mario", "email": "mario@test.com",
        "password_hash": "hash1", "metodo_pagamento": "tok1"
    }
    monkeypatch.setattr(router_module, "get_utente_by_email", lambda email: fake_user)

    # Fine precedente all'inizio
    res = client.post("/oggetti/1/prenota", data={"data_inizio": "2026-06-10", "data_fine": "2026-06-01"})
    assert res.status_code == 400
    assert res.json()["detail"] == "La data di fine non può essere precedente alla data di inizio"


def test_create_oggetto_empty_fields(monkeypatch):
    """Test 400 is returned when mandatory fields are empty on object creation."""
    client.cookies.set("user_email", "mario@test.com")
    fake_user = {
        "id": 1, "nome": "Mario", "email": "mario@test.com",
        "password_hash": "hash1", "metodo_pagamento": "tok1"
    }
    monkeypatch.setattr(router_module, "get_utente_by_email", lambda email: fake_user)

    res = client.post("/oggetti/crea", data={
        "nome": "   ",
        "descrizione_breve": "Breve",
        "descrizione_lunga": "Lunga",
        "categoria": "Fai-da-te"
    })
    assert res.status_code == 400
    assert "I campi obbligatori" in res.json()["detail"]
