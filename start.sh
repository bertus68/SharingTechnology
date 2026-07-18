#!/bin/bash

# Configura il PYTHONPATH puntando alla cartella src
export PYTHONPATH=src

# Avvia Uvicorn indicando il modulo corretto
uvicorn sharing_platform.app:app --reload

