"""
Module: seed_data.py
Description: Example and seed data for Lendly.
"""

CATEGORIE_SEED = [
    ("Fai-da-te", "🛠️"),
    ("Fotografia", "📷"),
    ("Mobilità", "🚲"),
    ("Elettronica", "💻"),
    ("Giardinaggio", "🏡")
]

UTENTI_SEED = [
    ("admin", "Amministratore", "admin@sharing.it", "pbkdf2:sha256:...", "PayPal"),
    ("mario", "Mario Rossi", "mario@rossi.it", "pbkdf2:sha256:...", "Carta"),
    ("luigi", "Luigi Verdi", "luigi@verdi.it", "pbkdf2:sha256:...", None)
]

DESC_BOSCH = (
    "Trapano cordless professionale con valigetta e doppia batteria, "
    "ideale per forare legno, metallo e plastica. Mandrino autoserrante da 13 mm."
)
DESC_SONY = (
    "La fotocamera Sony Alpha 7 III offre prestazioni eccezionali grazie al "
    "sensore retroilluminato da 24.2 MP, stabilizzazione a 5 assi e video 4K."
)
DESC_XIAOMI = (
    "Bicicletta elettrica pieghevole Xiaomi Smart E-bike. Leggera, compatta, "
    "con tre modalità di assistenza alla pedalata e fari LED integrati."
)

OGGETTI_SEED_RAW = [
    (
        "Trapano Avvitatore Bosch",
        "Trapano cordless professionale con due batterie",
        "Trapano cordless professionale con valigetta e doppia batteria.",
        DESC_BOSCH,
        "Fai-da-te",
        "mario",
        "Disponibile",
        "https://images.unsplash.com/photo-1504148455328-c376907d081c?q=80&w=600",
        "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?q=80&w=600",
        1
    ),
    (
        "Fotocamera Sony Alpha 7 III",
        "Fotocamera Mirrorless Full-Frame solo corpo",
        "Mirrorless Full-Frame ideale per foto e video di alta qualità.",
        DESC_SONY,
        "Fotografia",
        "luigi",
        "Prenotato",
        "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=600",
        "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?q=80&w=600",
        0
    ),
    (
        "Bicicletta Elettrica Xiaomi",
        "E-bike pieghevole con autonomia fino a 45km",
        "E-bike pieghevole, ottima per muoversi agilmente in città.",
        DESC_XIAOMI,
        "Mobilità",
        "admin",
        "Disponibile",
        "https://images.unsplash.com/photo-1485965120184-e220f721d03e?q=80&w=600",
        "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?q=80&w=600",
        1
    )
]


def seed_database(conn) -> None:
    """Seeds the database connection with initial example/demo data."""
    # Seed categorie
    cursor = conn.execute("SELECT COUNT(*) FROM categorie")
    if cursor.fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO categorie (nome, icona_path) VALUES (?, ?)",
            CATEGORIE_SEED
        )

    # Seed utenti
    cursor = conn.execute("SELECT COUNT(*) FROM utenti")
    if cursor.fetchone()[0] == 0:
        conn.executemany(
            """
            INSERT INTO utenti (username, nome, email, password_hash, metodo_pagamento)
            VALUES (?, ?, ?, ?, ?)
            """,
            UTENTI_SEED
        )

    # Seed oggetti
    cursor = conn.execute("SELECT COUNT(*) FROM oggetti")
    if cursor.fetchone()[0] == 0:
        cat_rows = conn.execute("SELECT id, nome FROM categorie").fetchall()
        cat_map = {row["nome"]: row["id"] for row in cat_rows}
        user_rows = conn.execute("SELECT id, username FROM utenti").fetchall()
        user_map = {row["username"]: row["id"] for row in user_rows}

        oggetti_seed = []
        for o in OGGETTI_SEED_RAW:
            oggetti_seed.append((
                o[0],  # nome
                o[1],  # descrizione
                o[2],  # descrizione_breve
                o[3],  # descrizione_lunga
                cat_map.get(o[4], 1),  # categoria_id
                o[4],  # categoria
                user_map.get(o[5], 1),  # proprietario_id
                user_map.get(o[5], 1),  # id_proprietario
                o[6],  # stato
                o[7],  # immagine_url1
                o[8],  # immagine_url2
                o[9]   # disponibilita
            ))

        conn.executemany(
            """
            INSERT INTO oggetti (
                nome, descrizione, descrizione_breve, descrizione_lunga,
                categoria_id, categoria, proprietario_id, id_proprietario,
                stato, immagine_url1, immagine_url2, disponibilita
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            oggetti_seed
        )

        # Seed an active reservation for the booked camera
        camera_row = conn.execute("SELECT id FROM oggetti WHERE nome LIKE '%Sony%'").fetchone()
        if camera_row:
            camera_id = camera_row["id"]
            conn.execute(
                """
                INSERT INTO prenotazioni (
                    oggetto_id, id_oggetto, utente_id, id_richiedente,
                    data_inizio, data_fine, stato_prenotazione, stato
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (camera_id, camera_id, user_map.get("mario", 2), user_map.get("mario", 2),
                 "2026-06-01", "2026-06-15", "attiva", "approvata")
            )
