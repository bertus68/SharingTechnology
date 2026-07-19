"""
Unit tests for database module.
"""
import os
import sqlite3
import pytest
from sharing_platform import database

TEST_DB = "test.db"


@pytest.fixture(autouse=True)
def setup_db():
    """Setup and teardown database for testing."""
    # usa un DB reale di test
    database.DB_NAME = TEST_DB

    # reset DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    conn.executescript(database.get_schema_scripts())
    conn.close()

    yield

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_create_and_get_utenti():
    """Test user creation and retrieval."""
    database.create_utente("Mario", "mario@test.com", "hash1", "tok1")
    database.create_utente("Luigi", "luigi@test.com", "hash2", None)

    utenti = database.get_utenti()

    assert len(utenti) == 2
    assert utenti[0]["nome"] == "Mario"
    assert utenti[1]["email"] == "luigi@test.com"


def test_delete_utente():
    """Test user deletion."""
    database.create_utente("Mario", "mario@test.com", "hash1")

    uid = database.get_utenti()[0]["id"]

    database.delete_utente(uid)

    assert len(database.get_utenti()) == 0


def test_create_and_get_oggetti():
    """Test object creation and retrieval."""
    database.create_utente("Owner", "o@test.com", "hash1")
    owner_id = database.get_utenti()[0]["id"]

    database.create_oggetto("Trapano", "Pro", "tool", True, owner_id)

    oggetti = database.get_oggetti()

    assert len(oggetti) == 1
    assert oggetti[0]["nome"] == "Trapano"


def test_update_oggetto_disponibilita():
    """Test object availability update."""
    database.create_utente("Owner", "o@test.com", "hash1")
    owner_id = database.get_utenti()[0]["id"]

    database.create_oggetto("Seghetto", "manuale", "tool", True, owner_id)
    obj_id = database.get_oggetti()[0]["id"]

    database.update_oggetto_disponibilita(obj_id, False)

    assert database.get_oggetti()[0]["disponibilita"] == 0


def test_delete_oggetto():
    """Test object deletion."""
    database.create_utente("Owner", "o@test.com", "hash1")
    owner_id = database.get_utenti()[0]["id"]

    database.create_oggetto("Laptop", "gaming", "tech", True, owner_id)
    obj_id = database.get_oggetti()[0]["id"]

    database.delete_oggetto(obj_id)

    assert len(database.get_oggetti()) == 0


def test_prenotazione_flow():
    """Test reservation flow: create and update reservation status."""
    database.create_utente("A", "a@test.com", "h1")
    database.create_utente("B", "b@test.com", "h2")

    owner = database.get_utenti()[0]["id"]
    user = database.get_utenti()[1]["id"]

    database.create_oggetto("Bici", "MTB", "sport", True, owner)
    obj_id = database.get_oggetti()[0]["id"]

    database.create_prenotazione(obj_id, user, "2026-01-01", "2026-01-10")

    pren = database.get_prenotazioni()
    assert pren[0]["stato"] == "in_attesa"

    database.update_prenotazione_stato(pren[0]["id"], "approvata")

    assert database.get_prenotazioni()[0]["stato"] == "approvata"


def test_pagamenti_flow():
    """Test payment flow: create and update payment status."""
    database.create_utente("A", "a@test.com", "h1")
    database.create_utente("B", "b@test.com", "h2")

    owner = database.get_utenti()[0]["id"]
    user = database.get_utenti()[1]["id"]

    database.create_oggetto("Drone", "4K", "tech", True, owner)
    obj_id = database.get_oggetti()[0]["id"]

    database.create_prenotazione(obj_id, user, "2026-01-01", "2026-01-05")
    pren_id = database.get_prenotazioni()[0]["id"]

    database.create_pagamento(pren_id, 15.5, "pending", "penale")

    pag = database.get_pagamenti()
    assert len(pag) == 1

    pay_id = pag[0]["id"]

    database.update_pagamento_stato(pay_id, "paid")

    assert database.get_pagamenti()[0]["stato"] == "paid"


def test_create_prenotazione_atomic_rollback(monkeypatch):
    """Verifica che un errore durante l'aggiornamento dell'oggetto provochi il rollback."""
    database.create_utente("A", "a@test.com", "h1")
    database.create_utente("B", "b@test.com", "h2")

    owner = database.get_utenti()[0]["id"]
    user = database.get_utenti()[1]["id"]

    database.create_oggetto("Bici", "MTB", "sport", True, owner)
    obj_id = database.get_oggetti()[0]["id"]

    # Wrapper per la connessione sqlite3
    class MockConnection:
        """A mock sqlite3 connection class to simulate database write errors."""

        def __init__(self, real_conn):
            self.real_conn = real_conn

        def execute(self, query, *args, **kwargs):
            """Execute a query, but raise an operational error for object updates."""
            if "UPDATE oggetti" in query:
                raise sqlite3.OperationalError("Simulated write error")
            return self.real_conn.execute(query, *args, **kwargs)

        def close(self):
            """Close the real connection."""
            self.real_conn.close()

        def __enter__(self):
            self.real_conn.__enter__()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return self.real_conn.__exit__(exc_type, exc_val, exc_tb)

    original_get_connection = database.get_connection

    def mock_get_connection():
        return MockConnection(original_get_connection())

    monkeypatch.setattr(database, "get_connection", mock_get_connection)

    # L'inserimento della prenotazione dovrebbe fallire e fare il rollback
    with pytest.raises(sqlite3.OperationalError):
        database.create_prenotazione(obj_id, user, "2026-01-01", "2026-01-10")

    # Ripristina l'originale prima di fare controlli nel DB reale per evitare interferenze
    monkeypatch.undo()

    # Verifica che non ci siano prenotazioni salvate a causa del rollback
    prenotazioni = database.get_prenotazioni()
    assert len(prenotazioni) == 0

    # Verifica che la disponibilità dell'oggetto non sia cambiata
    oggetti = database.get_oggetti()
    assert oggetti[0]["disponibilita"] == 1
    assert oggetti[0]["stato"] == "Disponibile"
