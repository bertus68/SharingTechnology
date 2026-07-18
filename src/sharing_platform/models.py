"""
File: model.py
Author: Marco Sganga
Date: 2026-05-31

Domain layer del sistema di sharing economy.
Contiene le entità principali dell'applicazione.

Questo modulo NON contiene logica di business o accesso al database,
ma solo strutture dati coerenti con il dominio.
"""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Utente:
    """
    Rappresenta un utente della piattaforma.

    Attributes:
        id: Identificativo univoco
        nome: Nome utente
        email: Email di login
        password_hash: Password già hashata
        metodo_pagamento: Token o riferimento al metodo di pagamento
        oggetti: Lista di ID degli oggetti posseduti
    """
    id: int
    nome: str
    email: str
    password_hash: str
    metodo_pagamento: Optional[str] = None
    oggetti: List[int] = field(default_factory=list)


@dataclass
class Oggetto:
    """
    Rappresenta un oggetto disponibile per il prestito.

    Attributes:
        id: Identificativo oggetto
        nome: Nome oggetto
        descrizione: Descrizione dettagliata
        categoria: Categoria merceologica
        disponibilita: Stato disponibilità
        id_proprietario: Proprietario dell'oggetto
        prenotazioni: Lista ID prenotazioni associate
    """
    id: int
    nome: str
    descrizione: str
    categoria: str
    disponibilita: bool
    id_proprietario: int
    prenotazioni: List[int] = field(default_factory=list)


@dataclass
class Prenotazione:
    """
    Rappresenta una richiesta di prestito.

    Attributes:
        id: Identificativo prenotazione
        id_oggetto: Oggetto richiesto
        id_richiedente: Utente richiedente
        data_inizio: Data inizio prestito
        data_fine: Data fine prestito
        stato: Stato prenotazione (in_attesa, approvata, rifiutata, chiusa)
    """
    id: int
    id_oggetto: int
    id_richiedente: int
    data_inizio: str
    data_fine: str
    stato: str


@dataclass
class Pagamento:
    """
    Rappresenta un pagamento o una penale.

    Attributes:
        id: Identificativo pagamento
        id_prenotazione: Prenotazione associata
        importo: Importo transazione
        stato: Stato pagamento
        tipo: Tipo pagamento (penale, deposito, fee)
    """
    id: int
    id_prenotazione: int
    importo: float
    stato: str
    tipo: str
