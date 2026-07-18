import pytest
from datetime import date

from sharing_platform.models import Utente, Oggetto, Prenotazione, Pagamento


# =========================
# UTENTE
# =========================
def test_utente_creation():
    u = Utente(
        id=1,
        nome="Mario Rossi",
        email="mario@test.com",
        password_hash="hash123"
    )

    assert u.id == 1
    assert u.nome == "Mario Rossi"
    assert u.email == "mario@test.com"
    assert u.password_hash == "hash123"
    assert u.oggetti == []  # default factory


# =========================
# OGGETTO
# =========================
def test_oggetto_creation():
    o = Oggetto(
        id=10,
        nome="Trapano",
        descrizione="Trapano Bosch",
        categoria="Utensili",
        disponibilita=True,
        id_proprietario=1
    )

    assert o.id == 10
    assert o.nome == "Trapano"
    assert o.disponibilita is True
    assert o.prenotazioni == []


# =========================
# PRENOTAZIONE
# =========================
def test_prenotazione_creation():
    p = Prenotazione(
        id=100,
        id_oggetto=10,
        id_richiedente=2,
        data_inizio=date(2026, 6, 1),
        data_fine=date(2026, 6, 5),
        stato="in_attesa"
    )

    assert p.id_oggetto == 10
    assert p.stato == "in_attesa"
    assert p.data_fine > p.data_inizio


# =========================
# PAGAMENTO
# =========================
def test_pagamento_creation():
    pay = Pagamento(
        id=500,
        id_prenotazione=100,
        importo=9.99,
        stato="pagato",
        tipo="penale"
    )

    assert pay.importo == 9.99
    assert pay.stato == "pagato"
    assert pay.tipo == "penale"


# =========================
# MOCK TEST (logica simulata)
# =========================
def test_relazione_logica_utente_oggetti():
    u = Utente(id=1, nome="A", email="a@a.it", password_hash="x")
    o1 = Oggetto(id=1, nome="A", descrizione="B", categoria="C", disponibilita=True, id_proprietario=1)
    o2 = Oggetto(id=2, nome="B", descrizione="C", categoria="D", disponibilita=True, id_proprietario=1)

    # simuliamo associazione (mock logico)
    u.oggetti = [o1.id, o2.id]

    assert len(u.oggetti) == 2
    assert 1 in u.oggetti
    assert 2 in u.oggetti