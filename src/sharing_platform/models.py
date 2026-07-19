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
from typing import Optional, List, Any


@dataclass
class Utente:
    """
    Rappresenta un utente della piattaforma.

    Attributes:
        id: Identificativo univoco
        nome: Nome utente
        email: Email di login
        password_hash: Password già hashata
        username: Nome utente per login e visualizzazione
        metodo_pagamento: Token o riferimento al metodo di pagamento
        oggetti: Lista di ID degli oggetti posseduti
    """
    id: int
    nome: str
    email: str
    password_hash: str
    username: Optional[str] = None
    metodo_pagamento: Optional[str] = None
    oggetti: List[int] = field(default_factory=list)

    def __post_init__(self):
        if self.username is None:
            self.username = self.nome.lower().replace(" ", "_")


@dataclass
class Prenotazione: # pylint: disable=too-many-instance-attributes
    """
    Rappresenta una richiesta di prestito.

    Attributes:
        id: Identificativo prenotazione
        id_oggetto: Oggetto richiesto
        id_richiedente: Utente richiedente
        data_inizio: Data inizio prestito
        data_fine: Data fine prestito
        stato: Stato prenotazione (in_attesa, approvata, chiusa, ecc)
    """
    id: int
    id_oggetto: int
    id_richiedente: int
    data_inizio: Any
    data_fine: Any
    stato: str
    oggetto_id: Optional[int] = None
    utente_id: Optional[int] = None
    stato_prenotazione: Optional[str] = None

    def __post_init__(self):
        if self.oggetto_id is None:
            self.oggetto_id = self.id_oggetto
        if self.utente_id is None:
            self.utente_id = self.id_richiedente
        if self.stato_prenotazione is None:
            self.stato_prenotazione = "conclusa" if self.stato in (
                "rifiutata", "conclusa", "chiusa"
            ) else "attiva"


@dataclass
class Oggetto: # pylint: disable=too-many-instance-attributes
    """
    Rappresenta un oggetto disponibile per il prestito.

    Attributes:
        id: Identificativo oggetto
        nome: Nome oggetto
        descrizione: Descrizione dettagliata
        categoria: Categoria merceologica
        disponibilita: Stato disponibilità
        id_proprietario: Proprietario dell'oggetto
        stato: Stato per la UI (Disponibile o Prenotato)
        immagine_url1: Prima immagine dell'oggetto
        immagine_url2: Seconda immagine dell'oggetto
        descrizione_breve: Descrizione breve per la card UI
        descrizione_lunga: Descrizione dettagliata
        prenotazione: L'eventuale ultima prenotazione attiva
        prenotazioni: Lista ID prenotazioni associate
    """
    id: int
    nome: str
    descrizione: str
    categoria: str
    disponibilita: bool
    id_proprietario: int
    stato: Optional[str] = None
    immagine_url1: Optional[str] = None
    immagine_url2: Optional[str] = None
    descrizione_breve: Optional[str] = None
    descrizione_lunga: Optional[str] = None
    categoria_id: Optional[int] = None
    proprietario_id: Optional[int] = None
    prenotazione: Optional[Prenotazione] = None
    prenotazioni: List[int] = field(default_factory=list)

    def __post_init__(self):
        if self.stato is None:
            self.stato = "Disponibile" if self.disponibilita else "Prenotato"
        if self.descrizione_breve is None:
            self.descrizione_breve = self.descrizione
        if self.descrizione_lunga is None:
            self.descrizione_lunga = self.descrizione
        if self.proprietario_id is None:
            self.proprietario_id = self.id_proprietario
        if self.immagine_url1 is None:
            self.immagine_url1 = (
                "https://images.unsplash.com/photo-1504148455328-c376907d081c?q=80&w=600"
            )

    @property
    def immagine_url(self):
        """Restituisce l'url dell'immagine principale."""
        return self.immagine_url1


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
