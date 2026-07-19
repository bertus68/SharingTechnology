"""
FILE: database.py
Author: Marco Sganga
Date: 2026-05-31
"""
import sqlite3
import time
from sharing_platform.seed_data import seed_database


DB_NAME = "app.db"


def get_connection():
    """Crea e restituisce una connessione SQLite al database applicativo."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# INITIALIZATION & SEEDING
# =========================

def get_schema_scripts() -> str:
    """Restituisce le query SQL necessarie a inizializzare lo schema del database."""
    return """
    CREATE TABLE IF NOT EXISTS utenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        nome TEXT,
        email TEXT UNIQUE,
        password_hash TEXT,
        metodo_pagamento TEXT
    );

    CREATE TABLE IF NOT EXISTS categorie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        icona_path TEXT
    );

    CREATE TABLE IF NOT EXISTS oggetti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proprietario_id INTEGER,
        id_proprietario INTEGER,
        nome TEXT,
        descrizione TEXT,
        descrizione_breve TEXT,
        descrizione_lunga TEXT,
        categoria TEXT,
        categoria_id INTEGER,
        stato TEXT DEFAULT 'Disponibile',
        immagine_url1 TEXT,
        immagine_url2 TEXT,
        disponibilita INTEGER DEFAULT 1,
        FOREIGN KEY (proprietario_id) REFERENCES utenti(id),
        FOREIGN KEY (categoria_id) REFERENCES categorie(id)
    );

    CREATE TABLE IF NOT EXISTS prenotazioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        oggetto_id INTEGER,
        id_oggetto INTEGER,
        utente_id INTEGER,
        id_richiedente INTEGER,
        data_inizio TEXT,
        data_fine TEXT,
        stato_prenotazione TEXT DEFAULT 'attiva',
        stato TEXT DEFAULT 'in_attesa',
        FOREIGN KEY (oggetto_id) REFERENCES oggetti(id),
        FOREIGN KEY (utente_id) REFERENCES utenti(id)
    );

    CREATE TABLE IF NOT EXISTS pagamenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_prenotazione INTEGER,
        importo REAL,
        stato TEXT,
        tipo TEXT,
        FOREIGN KEY (id_prenotazione) REFERENCES prenotazioni(id)
    );
    """


def init_db():
    """Inizializza il database con lo schema normalizzato e i dati seed."""
    conn = get_connection()
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(get_schema_scripts())
        conn.commit()

        # Seed data separated into its own module seed_data.py
        with conn:
            seed_database(conn)
    finally:
        conn.close()


# =========================
# UTENTI
# =========================

def create_utente(nome, email, password_hash, metodo_pagamento=None):
    """Inserisce un nuovo utente nella tabella utenti."""
    conn = get_connection()
    try:
        username = nome.lower().replace(" ", "_")
        cursor = conn.execute("SELECT COUNT(*) FROM utenti WHERE username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            username = f"{username}_{int(time.time())}"

        conn.execute(
            """
            INSERT INTO utenti
            (username, nome, email, password_hash, metodo_pagamento)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, nome, email, password_hash, metodo_pagamento)
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


def get_utente_by_email(email):
    """Restituisce un utente tramite la sua email."""
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM utenti WHERE email = ?", (email,)).fetchone()
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
# CATEGORIE
# =========================

def create_categoria(nome, icona_path):
    """Crea una nuova categoria."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO categorie (nome, icona_path) VALUES (?, ?)",
            (nome, icona_path)
        )
        conn.commit()
    finally:
        conn.close()


def get_categorie():
    """Restituisce tutte le categorie."""
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM categorie").fetchall()
    finally:
        conn.close()


# =========================
# OGGETTI
# =========================

# pylint: disable=too-many-arguments,too-many-positional-arguments
def create_oggetto(
    nome,
    descrizione,
    categoria,
    disponibilita,
    id_proprietario,
    descrizione_breve=None,
    descrizione_lunga=None,
    immagine_url1=None,
    immagine_url2=None,
    stato=None
    ):
    """Crea un nuovo oggetto inserendolo nella tabella oggetti."""
    conn = get_connection()
    try:
        cursor = conn.execute("SELECT id FROM categorie WHERE nome = ?", (categoria,))
        row = cursor.fetchone()
        if row:
            categoria_id = row["id"]
        else:
            cursor2 = conn.execute(
                "INSERT INTO categorie (nome, icona_path) VALUES (?, ?)",
                (categoria, "📦")
            )
            categoria_id = cursor2.lastrowid

        if stato is None:
            stato = "Disponibile" if int(disponibilita) == 1 else "Prenotato"

        if descrizione_breve is None:
            descrizione_breve = descrizione
        if descrizione_lunga is None:
            descrizione_lunga = descrizione

        conn.execute(
            """
            INSERT INTO oggetti
            (nome, descrizione, descrizione_breve, descrizione_lunga, categoria, categoria_id,
             disponibilita, stato, proprietario_id, id_proprietario, immagine_url1, immagine_url2)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, descrizione, descrizione_breve, descrizione_lunga, categoria, categoria_id,
             int(disponibilita), stato, id_proprietario, id_proprietario,
             immagine_url1, immagine_url2)
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
        stato = "Disponibile" if value else "Prenotato"
        conn.execute(
            "UPDATE oggetti SET disponibilita = ?, stato = ? WHERE id = ?",
            (int(value), stato, obj_id)
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
        with conn:
            conn.execute(
                """
                INSERT INTO prenotazioni
                (oggetto_id, id_oggetto, utente_id, id_richiedente,
                 data_inizio, data_fine, stato_prenotazione, stato)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (id_oggetto, id_oggetto, id_richiedente, id_richiedente,
                 data_inizio, data_fine, "attiva", stato)
            )
            # Aggiorna lo stato dell'oggetto prenotato
            conn.execute(
                "UPDATE oggetti SET disponibilita = 0, stato = 'Prenotato' WHERE id = ?",
                (id_oggetto,)
            )
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
        with conn:
            # If concluse or rifiutata, we free up the object!
            if stato in ("conclusa", "rifiutata", "chiusa"):
                # Find associated object id
                row = conn.execute(
                    "SELECT oggetto_id FROM prenotazioni WHERE id = ?",
                    (prenotazione_id,)
                ).fetchone()
                if row:
                    obj_id = row["oggetto_id"]
                    conn.execute(
                        "UPDATE oggetti SET disponibilita = 1, stato = 'Disponibile' WHERE id = ?",
                        (obj_id,)
                    )
                stato_prenotazione = "conclusa"
            else:
                stato_prenotazione = "attiva"

            conn.execute(
                "UPDATE prenotazioni SET stato = ?, stato_prenotazione = ? WHERE id = ?",
                (stato, stato_prenotazione, prenotazione_id)
            )
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


# =========================
# EFFICIENT JOIN QUERIES
# =========================

def get_oggetti_con_prenotazioni(search_query=None, category_id=None):
    """
    Esegue una query JOIN con categorie e LEFT JOIN con prenotazioni attive per evitare N+1.
    """
    conn = get_connection()
    try:
        query = """
            SELECT
                o.*,
                c.nome as categoria_nome,
                c.icona_path as categoria_icona,
                p.id as pren_id,
                p.data_inizio as pren_data_inizio,
                p.data_fine as pren_data_fine,
                p.stato_prenotazione as pren_stato_prenotazione,
                p.stato as pren_stato,
                p.utente_id as pren_utente_id
            FROM oggetti o
            LEFT JOIN categorie c ON o.categoria_id = c.id
            LEFT JOIN (
                SELECT * FROM prenotazioni
                WHERE id IN (
                    SELECT MAX(id) FROM prenotazioni
                    WHERE stato_prenotazione = 'attiva' OR stato = 'approvata'
                    GROUP BY oggetto_id
                )
            ) p ON o.id = p.oggetto_id
        """
        conditions = []
        params = []
        if search_query:
            conditions.append("(o.nome LIKE ? OR o.descrizione LIKE ?)")
            params.extend([f"%{search_query}%", f"%{search_query}%"])
        if category_id:
            conditions.append("o.categoria_id = ?")
            params.append(int(category_id))

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY o.id ASC"

        rows = conn.execute(query, params).fetchall()
        return rows
    finally:
        conn.close()


def get_oggetto_con_prenotazione_by_id(obj_id):
    """
    Recupera un singolo oggetto con la sua eventuale prenotazione attiva.
    """
    conn = get_connection()
    try:
        query = """
            SELECT
                o.*,
                c.nome as categoria_nome,
                c.icona_path as categoria_icona,
                p.id as pren_id,
                p.data_inizio as pren_data_inizio,
                p.data_fine as pren_data_fine,
                p.stato_prenotazione as pren_stato_prenotazione,
                p.stato as pren_stato,
                p.utente_id as pren_utente_id
            FROM oggetti o
            LEFT JOIN categorie c ON o.categoria_id = c.id
            LEFT JOIN (
                SELECT * FROM prenotazioni
                WHERE oggetto_id = ? AND (stato_prenotazione = 'attiva' OR stato = 'approvata')
                ORDER BY id DESC LIMIT 1
            ) p ON o.id = p.oggetto_id
            WHERE o.id = ?
        """
        row = conn.execute(query, (obj_id, obj_id)).fetchone()
        return row
    finally:
        conn.close()


# Inizializza automaticamente il DB reale se importato
try:
    init_db()
except Exception: # pylint: disable=broad-exception-caught
    pass
