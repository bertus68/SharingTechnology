import os
import sqlite3
import pytest
import sharing_platform.database as database

TEST_DB = "test.db"


@pytest.fixture(autouse=True)
def setup_db():
    # usa un DB reale di test
    database.DB_NAME = TEST_DB

    # reset DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    conn.executescript("""
        CREATE TABLE utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            password_hash TEXT,
            metodo_pagamento TEXT
        );

        CREATE TABLE oggetti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descrizione TEXT,
            categoria TEXT,
            disponibilita INTEGER,
            id_proprietario INTEGER
        );

        CREATE TABLE prenotazioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_oggetto INTEGER,
            id_richiedente INTEGER,
            data_inizio TEXT,
            data_fine TEXT,
            stato TEXT
        );

        CREATE TABLE pagamenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_prenotazione INTEGER,
            importo REAL,
            stato TEXT,
            tipo TEXT
        );
    """)
    conn.close()

    yield

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_create_and_get_utenti():
    database.create_utente("Mario", "mario@test.com", "hash1", "tok1")
    database.create_utente("Luigi", "luigi@test.com", "hash2", None)

    utenti = database.get_utenti()

    assert len(utenti) == 2
    assert utenti[0]["nome"] == "Mario"
    assert utenti[1]["email"] == "luigi@test.com"


def test_delete_utente():
    database.create_utente("Mario", "mario@test.com", "hash1")

    uid = database.get_utenti()[0]["id"]

    database.delete_utente(uid)

    assert len(database.get_utenti()) == 0


def test_create_and_get_oggetti():
    database.create_utente("Owner", "o@test.com", "hash1")
    owner_id = database.get_utenti()[0]["id"]

    database.create_oggetto("Trapano", "Pro", "tool", True, owner_id)

    oggetti = database.get_oggetti()

    assert len(oggetti) == 1
    assert oggetti[0]["nome"] == "Trapano"


def test_update_oggetto_disponibilita():
    database.create_utente("Owner", "o@test.com", "hash1")
    owner_id = database.get_utenti()[0]["id"]

    database.create_oggetto("Seghetto", "manuale", "tool", True, owner_id)
    obj_id = database.get_oggetti()[0]["id"]

    database.update_oggetto_disponibilita(obj_id, False)

    assert database.get_oggetti()[0]["disponibilita"] == 0


def test_delete_oggetto():
    database.create_utente("Owner", "o@test.com", "hash1")
    owner_id = database.get_utenti()[0]["id"]

    database.create_oggetto("Laptop", "gaming", "tech", True, owner_id)
    obj_id = database.get_oggetti()[0]["id"]

    database.delete_oggetto(obj_id)

    assert len(database.get_oggetti()) == 0


def test_prenotazione_flow():
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