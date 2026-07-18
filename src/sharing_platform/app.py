"""
File: app.py
Author: Marco Sganga
Date: 2026-05-31
"""

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sharing_platform.router import router

app = FastAPI(title="Sharing Platform - Base")

# 1. Inizializzazione del motore Jinja2 puntando alla cartella corretta
templates = Jinja2Templates(directory="src/sharing_platform/templates")

# 2. (Opzionale) Se hai CSS o JS in una cartella static, montala qui
# app.mount("/static", StaticFiles(directory="src/sharing_platform/static"), name="static")

app.include_router(router)

@app.get("/")
def read_root(request: Request):
    """
    Serve index.html usando il motore di template.
    Passiamo 'request' per permettere al template di usare url_for.
    """
    return templates.TemplateResponse("index.html", {"request": request})
