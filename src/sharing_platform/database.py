"""
FILE: database.py
Author: Marco Sganga
Date: 2026-05-31
"""
import sqlite3


DB_NAME = "app.db"


def get_connection():
    """Crea e restituisce una connessione SQLite al database applicativo."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# UTENTI
# =========================

def create_utente(nome, email, password_hash, metodo_pagamento=None):
    """Inserisce un nuovo utente nella tabella utenti."""
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO utenti
            (nome, email, password_hash, metodo_pagamento)
            VALUES (?, ?, ?, ?)
            """,
            (nome, email, password_hash, metodo_pagamento)
        )
        conn.commit()
    finally:
        conn.close()


def get_utenti():
    """Restituisce tutti gli utenti presenti nel database."""
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM utenti").fetchall()
        return rows
    finally:
        conn.close()


def delete_utente(user_id: int):
    """Elimina un utente dal database tramite ID."""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM utenti WHERE id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()


# =========================
# OGGETTI
# =========================

def create_oggetto(
    nome,
    descrizione,
    categoria,
    disponibilita,
    id_proprietario
    ):
    """Crea un nuovo oggetto inserendolo nella tabella oggetti."""
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO oggetti
            (nome, descrizione, categoria, disponibilita, id_proprietario)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome, descrizione, categoria, int(disponibilita), id_proprietario)
        )
        conn.commit()
    finally:
        conn.close()


def get_oggetti():
    """Restituisce tutti gli oggetti presenti nel database."""
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM oggetti").fetchall()
    finally:
        conn.close()


def delete_oggetto(obj_id: int):
    """Elimina un oggetto dal database tramite ID."""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM oggetti WHERE id = ?", (obj_id,))
        conn.commit()
    finally:
        conn.close()


def update_oggetto_disponibilita(obj_id: int, value: bool):
    """Aggiorna la disponibilità di un oggetto."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE oggetti SET disponibilita = ? WHERE id = ?",
            (int(value), obj_id)
        )
        conn.commit()
    finally:
        conn.close()


# =========================
# PRENOTAZIONI
# =========================

def create_prenotazione(
    id_oggetto,
    id_richiedente,
    data_inizio,
    data_fine,
    stato="in_attesa"
    ):
    """Crea una nuova prenotazione per un oggetto."""
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO prenotazioni
            (id_oggetto, id_richiedente, data_inizio, data_fine, stato)
            VALUES (?, ?, ?, ?, ?)
            """,
            (id_oggetto, id_richiedente, data_inizio, data_fine, stato)
        )
        conn.commit()
    finally:
        conn.close()


def get_prenotazioni():
    """Restituisce tutte le prenotazioni presenti nel database."""
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM prenotazioni").fetchall()
    finally:
        conn.close()


def update_prenotazione_stato(prenotazione_id, stato):
    """Aggiorna lo stato di una prenotazione."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE prenotazioni SET stato = ? WHERE id = ?",
            (stato, prenotazione_id)
        )
        conn.commit()
    finally:
        conn.close()


# =========================
# PAGAMENTI
# =========================

def create_pagamento(id_prenotazione, importo, stato, tipo):
    """Crea un nuovo pagamento associato a una prenotazione."""
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO pagamenti (id_prenotazione, importo, stato, tipo)
            VALUES (?, ?, ?, ?)
            """,
            (id_prenotazione, importo, stato, tipo)
        )
        conn.commit()
    finally:
        conn.close()


def get_pagamenti():
    """Restituisce tutti i pagamenti presenti nel database."""
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM pagamenti").fetchall()
    finally:
        conn.close()


def update_pagamento_stato(payment_id, stato):
    """Aggiorna lo stato di un pagamento."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE pagamenti SET stato = ? WHERE id = ?",
            (stato, payment_id)
        )
        conn.commit()
    finally:
        conn.close()
