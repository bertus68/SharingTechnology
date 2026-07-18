import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

import sharing_platform.app as app_module
import sharing_platform.router as router_module


def test_root(monkeypatch):
    # mock FileResponse per evitare accesso file system
    class FakeResponse:
        def __init__(self, path):
            self.path = path

    monkeypatch.setattr(app_module, "FileResponse", FakeResponse)

    app = app_module.app
    client = TestClient(app)

    res = client.get("/")

    assert res.status_code == 200
    assert res.json() == {"path": "src/sharing_platform/templates/index.html"}


def test_router_is_wired(monkeypatch):
    # mock funzione DB per isolare app
    monkeypatch.setattr(router_module, "get_utenti", lambda: [{"id": 1}])

    app = app_module.app
    client = TestClient(app)

    res = client.get("/api/utenti")

    assert res.status_code == 200
    assert res.json() == [{"id": 1}]