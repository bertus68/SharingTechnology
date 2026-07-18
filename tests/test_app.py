import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

import sharing_platform.app as app_module
import sharing_platform.router as router_module


def test_root(monkeypatch):
    app = app_module.app
    client = TestClient(app)

    # Mock database call to get empty lists
    monkeypatch.setattr(router_module, "get_oggetti_con_prenotazioni", lambda **kwargs: [])
    monkeypatch.setattr(router_module, "get_categorie", lambda: [])

    res = client.get("/")

    assert res.status_code == 200
    # Confirm it rendered the HTML template correctly
    assert "Sharing Platform" in res.text


def test_router_is_wired(monkeypatch):
    # mock funzione DB per isolare app
    monkeypatch.setattr(router_module, "get_utenti", lambda: [{"id": 1}])

    app = app_module.app
    client = TestClient(app)

    res = client.get("/api/utenti")

    assert res.status_code == 200
    assert res.json() == [{"id": 1}]
