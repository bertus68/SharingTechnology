"""
FILE: router.py
Author: Jules (Extended from Marco Sganga)
Date: 2026-05-31
"""

from typing import Optional, Any
from fastapi import APIRouter, Request, Form, HTTPException, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

from sharing_platform.database import (
    create_utente,
    get_utenti,
    get_utente_by_email,
    get_categorie,
    create_oggetto,
    get_oggetti_con_prenotazioni,
    get_oggetto_con_prenotazione_by_id,
    create_prenotazione
)
from sharing_platform.models import Utente, Oggetto, Prenotazione

router = APIRouter()

templates = Jinja2Templates(directory="src/sharing_platform/templates")


# =========================
# HELPER FOR USER SESSION
# =========================

def get_logged_in_user(request: Request) -> Optional[Utente]:
    """Recupera l'utente attualmente loggato tramite cookie."""
    email = request.cookies.get("user_email")
    if email:
        row = get_utente_by_email(email)
        if row:
            return Utente(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                password_hash=row["password_hash"],
                metodo_pagamento=row["metodo_pagamento"]
            )
    return None


# =========================
# MAPPING UTILS
# =========================

def row_to_oggetto(row: Any) -> Oggetto:
    """Mappa una riga di database SQLite (Row) all'oggetto del dominio Oggetto."""
    pren = None
    keys = row.keys() if hasattr(row, "keys") else []

    if "pren_id" in keys and row["pren_id"] is not None:
        user_id_val = 0
        if "pren_utente_id" in keys:
            user_id_val = row["pren_utente_id"]
        elif "id_richiedente" in keys:
            user_id_val = row["id_richiedente"]
        elif "utente_id" in keys:
            user_id_val = row["utente_id"]

        pren = Prenotazione(
            id=row["pren_id"],
            id_oggetto=row["id"],
            id_richiedente=user_id_val,
            data_inizio=row["pren_data_inizio"],
            data_fine=row["pren_data_fine"],
            stato=row["pren_stato"] or "in_attesa"
        )

    # pylint: disable=unexpected-keyword-arg
    return Oggetto(
        id=row["id"],
        nome=row["nome"],
        descrizione=row["descrizione"] or "",
        categoria=row["categoria"] or "",
        disponibilita=bool(row["disponibilita"]),
        id_proprietario=row["id_proprietario"] or 0,
        stato=row["stato"] or "Disponibile",
        immagine_url1=row["immagine_url1"],
        immagine_url2=row["immagine_url2"],
        descrizione_breve=row["descrizione_breve"],
        descrizione_lunga=row["descrizione_lunga"],
        categoria_id=row["categoria_id"] if "categoria_id" in keys else None,
        proprietario_id=row["proprietario_id"] if "proprietario_id" in keys else None,
        prenotazione=pren
    )


# =========================
# SYSTEM UI ROUTES
# =========================

@router.get("/", response_class=HTMLResponse)
def index_route(request: Request, search: Optional[str] = None, category: Optional[int] = None):
    """Renderizza la home page con filtri e lista oggetti."""
    user = get_logged_in_user(request)
    categorie = get_categorie()

    rows = get_oggetti_con_prenotazioni(search_query=search, category_id=category)
    oggetti = [row_to_oggetto(row) for row in rows]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "user": user,
            "oggetti": oggetti,
            "categorie": categorie,
            "search_query": search or "",
            "category_filter": category
        }
    )


@router.get("/oggetti/crea", response_class=HTMLResponse)
def create_oggetto_form(request: Request):
    """Renderizza il form per aggiungere un nuovo oggetto."""
    user = get_logged_in_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    categorie = get_categorie()
    return templates.TemplateResponse(
        request=request,
        name="create_oggetto.html",
        context={
            "request": request,
            "user": user,
            "categorie": categorie
        }
    )


# pylint: disable=too-many-arguments,too-many-positional-arguments,unexpected-keyword-arg
@router.post("/oggetti/crea")
def handle_create_oggetto(
    request: Request,
    nome: str = Form(...),
    descrizione_breve: str = Form(...),
    descrizione_lunga: str = Form(...),
    categoria: str = Form(...),
    immagine_url1: Optional[str] = Form(None),
    immagine_url2: Optional[str] = Form(None)
):
    """Crea un nuovo oggetto e reindirizza alla home."""
    user = get_logged_in_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    create_oggetto(
        nome=nome,
        descrizione=descrizione_breve,
        categoria=categoria,
        disponibilita=True,
        id_proprietario=user.id,
        descrizione_breve=descrizione_breve,
        descrizione_lunga=descrizione_lunga,
        immagine_url1=immagine_url1,
        immagine_url2=immagine_url2
    )
    return RedirectResponse(url="/", status_code=303)


@router.get("/oggetti/{obj_id}", response_class=HTMLResponse)
def details_route(obj_id: int, request: Request):
    """Dettaglio di un singolo oggetto."""
    user = get_logged_in_user(request)
    row = get_oggetto_con_prenotazione_by_id(obj_id)
    if not row:
        raise HTTPException(status_code=404, detail="Oggetto non trovato")

    oggetto = row_to_oggetto(row)
    return templates.TemplateResponse(
        request=request,
        name="details.html",
        context={
            "request": request,
            "user": user,
            "oggetto": oggetto
        }
    )


@router.post("/oggetti/{obj_id}/prenota")
def handle_prenota_oggetto(
    obj_id: int,
    request: Request,
    data_inizio: str = Form(...),
    data_fine: str = Form(...)
):
    """Crea una richiesta di prenotazione per un oggetto."""
    user = get_logged_in_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    create_prenotazione(
        id_oggetto=obj_id,
        id_richiedente=user.id,
        data_inizio=data_inizio,
        data_fine=data_fine,
        stato="approvata"
    )
    return RedirectResponse(url=f"/oggetti/{obj_id}", status_code=303)


# =========================
# LOGIN / LOGOUT / REGISTER
# =========================

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    """Pagina di login e registrazione."""
    user = get_logged_in_user(request)
    if user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request, "error": None}
    )


@router.post("/login")
def handle_login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...)
):
    """Gestisce il login utente."""
    user_row = get_utente_by_email(email)
    if not user_row:
        # Se non esiste, lo registriamo al volo per semplicità di test / demo!
        username = email.split("@")[0]
        create_utente(nome=username.capitalize(), email=email, password_hash=password)
        user_row = get_utente_by_email(email)

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_email", value=email)
    return response


@router.get("/logout")
def handle_logout(response: Response):
    """Effettua il logout dell'utente."""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_email")
    return response


# =========================
# API COMPATIBILITY ROUTES FOR TESTS
# =========================

@router.get("/api/utenti")
def api_get_utenti():
    """Ritorna tutti gli utenti in formato JSON (per compatibilità test)."""
    utenti_rows = get_utenti()
    return [dict(row) for row in utenti_rows]


@router.post("/api/utenti")
async def api_create_utente(request: Request):
    """Crea un utente in formato JSON (per compatibilità test)."""
    try:
        data = await request.json()
        nome = data["nome"]
        email = data["email"]
        password_hash = data["password_hash"]
        metodo_pagamento = data.get("metodo_pagamento")
    except KeyError as e:
        # crash in 500 come richiesto dal test_create_utente_route_missing_fields
        raise HTTPException(status_code=500, detail=f"Campo mancante: {e}") from e

    create_utente(nome, email, password_hash, metodo_pagamento)
    return {"status": "ok"}
