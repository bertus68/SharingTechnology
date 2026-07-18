# Sharing Technologies

## Description
**sharing-platform-app** è un'applicazione Python (basata su FastAPI) progettata come piattaforma di condivisione. Il progetto include una pipeline di CI/CD automatizzata su GitLab che si occupa dell'intero ciclo di vita del software: compilazione di un eseguibile autonomo, testing, analisi statica del codice e pubblicazione automatica dei rilasci.

---

## Struttura del Progetto
* `src/sharing_platform/`: Contiene il codice sorgente dell'applicazione core.
  * `app.py`: L'entry-point principale dell'applicazione.
* `tests/`: Suite di test unitari e di integrazione (gestiti tramite `pytest`).

---

## Sviluppo Locale e Installazione

### Requisiti
* **Python 3.13** (o versione compatibile)
* Dipendenze di sistema per la compilazione (es. `binutils` su sistemi Linux)

### Setup Ambiente
1. Clona il repository e posizionati nella cartella principale:
   ```bash
   cd sharing-technologies
   ```
2. Crea e attiva un ambiente virtuale:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Su Windows: .venv\Scripts\activate
   ```
3. Installa le dipendenze richieste:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Esecuzione Test e Qualità del Codice
Prima di effettuare un commit, è consigliabile verificare localmente lo stato del codice:

* **Eseguire i test:**
  ```bash
  PYTHONPATH=src pytest tests/
  ```
* **Verificare lo stile del codice (Linter):**
  ```bash
  pip install pylint
  PYTHONPATH=src pylint src/sharing_platform/
  ```

---

## Generazione del Binario Locale
Per compilare l'applicazione in un unico file eseguibile autonomo (senza costringere l'utilizzatore finale a installare Python), viene utilizzato **PyInstaller**:

```bash
pip install pyinstaller
PYTHONPATH=src python -m PyInstaller --onefile --name=sharing-platform-app src/sharing_platform/app.py
```
L'eseguibile compilato sarà generato all'interno della cartella `dist/`.

---

## Pipeline CI/CD (GitLab)
Il progetto integra una pipeline DevOps configurata in `.gitlab-ci.yml` suddivisa nei seguenti stage, attiva sui branch `main` e `basic`:

1. **Build**: Compila l'eseguibile standalone per Linux usando PyInstaller.
2. **Test**: Esegue automaticamente i test di regressione con `pytest`.
3. **QA**: Monitora la qualità e la conformità stilistica del codice tramite `pylint`.
4. **Deploy**: In caso di successo e push sui branch abilitati, esegue un doppio rilascio parallelo:
   * **Pacchetto Python (PyPI):** Genera i sorgenti (`.tar.gz`) e la Wheel (`.whl`) caricandoli nel *GitLab Package Registry*.
   * **Eseguibile Singolo:** Carica il file binario standalone compilato nel *GitLab Generic Package Registry*.

---

## Download & Rilascio

### Opzione A: Eseguibile Standalone (Consigliato per utenti finali)
Non richiede l'installazione di Python. Scarica l'eseguibile unico per Linux direttamente dal Generic Package Registry:
* Link di download: https://gitlab.com/Marcolino88/sharing-technologies/-/packages/generic/sharing-platform-binaries/0.1.0/sharing-platform-app

Una volta scaricato da terminale, assegna i permessi di esecuzione e avvialo:
chmod +x sharing-platform-app
./sharing-platform-app

### Opzione B: Pacchetto Python (Per sviluppatori o integrazioni)
Se preferisci installarlo como libreria all'interno del tuo ambiente virtuale Python, puoi configurare pip per attingere al registro privato di GitLab:

pip install sharing-platform-app --extra-index-url https://gitlab.com/api/v4/projects/82482895/packages/pypi/simple

---

## Come creare una nuova versione/release ufficiale
Il progetto è configurato per creare le release in modo completamente automatico. Quando decidi che il codice sul branch main è pronto e stabile:

1. Crea un tag locale con la versione (es. v0.1.0):
   git tag v0.1.0

2. Invia il tag su GitLab:
   git push origin v0.1.0

La pipeline intercetterà il tag, eseguirà i test e creerà in automatico la pagina formale sotto la sezione Deploy -> Releases di GitLab, agganciandoci direttamente il link all'eseguibile aggiornato.

---

## Autori e Licenza
* **Autore:** Marco Sganga
* **Stato del Progetto:** In sviluppo attivo.

