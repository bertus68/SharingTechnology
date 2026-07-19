# TODO List - Sharing Platform

Questo documento raccoglie lo storico e la pianificazione degli sviluppi futuri, delle ottimizzazioni ingegneristiche e dei miglioramenti funzionali previsti per la piattaforma digitale di prestito tra privati.

---

## 1. Funzionalità Applicative (Sviluppo Core)

- [ ] **Sistema di Recensioni e Feedback Bidirezionale**
  - Implementare recensioni asincrone (1-5 stelle con testo) rilasciabili solo al termine di una prenotazione, per calcolare il punteggio di affidabilità pubblica di prosumer e proprietari.
- [ ] **Chat Interna Cifrata**
  - Integrare un modulo di messaggistica interna (WebSocket o Server-Sent Events) per permettere la trattativa e il coordinamento logistico direttamente in-app, proteggendo la privacy dell'utente (senza scambiare numeri di telefono o email personali).
- [ ] **Gestione Categorie Avanzata**
  - Aggiungere un'area amministrativa per la creazione, modifica ed eliminazione delle categorie direttamente dalla UI, con selezione personalizzata dell'icona emoji o caricamento di icone vettoriali (SVG).
- [ ] **Pannello di Amministrazione per Controversie**
  - Costruire una dashboard dedicata agli amministratori per visualizzare le segnalazioni degli utenti, esaminare le evidenze fotografiche dello stato dell'oggetto e dirimere i rimborsi o gli sblocchi dei depositi cauzionali.

---

## 2. Integrazioni e Logistica

- [ ] **Geolocalizzazione e Mappe Interattive**
  - Integrare una mappa interattiva (es: OpenStreetMap / Leaflet o Google Maps API) per filtrare e visualizzare la prossimità geografica degli oggetti disponibili rispetto alla posizione dell'utente.
- [ ] **Integrazione Gateway di Pagamento Reale (Escrow)**
  - Configurare e collegare l'SDK di Stripe (Stripe Connect) per gestire i flussi finanziari reali (pre-autorizzazioni per cauzione, ricariche, addebiti per penali e trasferimento fondi) in modalità di escrow fiduciario centralizzato.
- [ ] **Integrazione Spedizioni Nazionali**
  - Collaborare con provider di spedizione (es: Sendcloud, Packlink API) per automatizzare la generazione di etichette di spedizione prepagate per prestiti non di prossimità fisica.

---

## 3. Ottimizzazioni Tecniche e Infrastruttura

- [ ] **Migrazione del Database (PostgreSQL)**
  - Transire da SQLite a PostgreSQL in produzione per superare i limiti di concorrenza in scrittura (locking del file DB) e abilitare il supporto nativo a indici geografici (PostGIS).
- [ ] **Sessioni JWT (JSON Web Token)**
  - Migrare l'autenticazione basata su cookie semplice a una gestione tramite JWT con tempi di scadenza deterministici, rotazione dei refresh token e blocco in blacklist in caso di logout o violazione sicurezza.
- [ ] **Introduzione di Caching Layer (Redis)**
  - Utilizzare Redis per archiviare le sessioni attive e applicare caching sul catalogo degli oggetti più ricercati, alleggerendo la pressione sul database relazionale.

---

## 4. Quality Assurance e Pipeline CI/CD

- [ ] **Test End-to-End (E2E) con Playwright**
  - Scrivere una suite completa di test automatizzati per simulare i percorsi completi dell'utente (registrazione -> caricamento oggetto -> ricerca -> prenotazione -> approvazione -> restituzione) sul browser reale.
- [ ] **Dockerizzazione e Deploy Cloud**
  - Creare un file `Dockerfile` ottimizzato (multi-stage build) per pacchettizzare l'applicazione FastAPI in un container leggero e pronto al deploy su Kubernetes o servizi cloud serverless (AWS ECS, Google Cloud Run).
- [ ] **Monitoraggio e Centralizzazione dei Log**
  - Integrare un sistema di logging centralizzato (es: Sentry, Prometheus e Grafana) per monitorare lo stato di salute delle API, intercettare tempestivamente eccezioni non gestite nel backend e tenere traccia delle transazioni critiche.
