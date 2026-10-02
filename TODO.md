# MealTracker WebApp — Roadmap

Ultimo aggiornamento: 2026-10-02

---

## ✅ Completato

### Release 1.1.0 (2026-10-02)

- [x] **Vai a data** nella vista settimanale — selettore di data, settimana che contiene la data (backend ≥ 0.3.0), "Data fuori periodo tracciato" fuori periodo
- [x] **Avviso copia non aggiornata** — "Non connesso al server. Copia del gg/mm hh:mm" quando il service worker mostra la pagina in cache
- [x] **Python 3.13.12** e dipendenze bloccate (`requirements.txt`, `requirements-dev.txt`)

### Release 1.0.0 (2026-08-07)

- [x] **PWA — app installabile sulla home del telefono** — `manifest.json`, service worker `sw.js` (cache-first per statici/CDN, network-first per le navigazioni), icone 192/512/maskable, `display: standalone`; i dati del backend restano online-only

### Sessione 2026-08-03/06 (release 0.6.0)

- [x] **Form inserimento mobile-first** — layout compatto, Chi+Tipo e Dessert+Note affiancati, heading ridotto, CSS touch target 48px, data preimpostata a oggi
- [x] **Toggle "Nuova settimana"** — sostituita checkbox nativa con Bootstrap custom-switch (label + interruttore iOS-style)
- [x] **Bug Start week** — corretto: prima inviava sempre `true` (controllava presenza chiave, non valore)
- [x] **Feedback inserimento** — flash message dopo submit (successo ✓ / errore), redirect POST→GET per evitare ri-submit
- [x] **Dessert sempre visibile** — rimosso toggle checkbox, ora campo normale con placeholder "Opzionale"
- [x] **`app.secret_key`** — aggiunta in `main.py` (necessaria per `flash()`)
- [x] **Test suite** — 12 test pytest in `tests/test_meal_insertion.py` (GET, start_week, dessert, flash)
- [x] **Rimosso codice morto** — `time.sleep(0.5)`, `raise Exception`, `<head>` illegale dentro `<body>`, `myFunction()`/`myCheck`

---

## 🔲 Allineare la versione Python col backend

**Priorità**: Bassa  
La webapp è su Python 3.13.12 (release 1.1.0); il backend è ancora su 3.11.7 e il suo aggiornamento è un TODO del backend. Quando verrà fatto, tenere le due versioni allineate.

---

## 🔲 Vista settimanale mobile-friendly

**Priorità**: Alta  
**File coinvolti**: `src/templates/week_view.html`

**Cosa fare**:
- Sostituire la tabella Bootstrap orizzontale (scroll laterale su mobile, colonne strette) con **card verticali** (una card per pasto)
- Aggiungere frecce/swipe per navigare tra settimane (oggi sono link "Previous"/"Next" con URL manuali)
- Pulsante "Vai a settimana corrente"
- Pulsante delete più grande e accessibile
- Navigazione tra settimane senza ricaricare l'intera pagina (AJAX o URL parameter + render lato server)

**Perché**: la tabella attuale è illeggibile su schermi stretti.

---

## 🔲 Gestione errori robusta

**Priorità**: Media  
**File coinvolti**: `src/infrastructure/blueprints/meal_controller.py`

**Cosa fare**:
- Sostituire `except:` nudo in `week_meals()` con handling specifico (ConnectionError, Timeout, HTTPError)
- Messaggi di errore descrittivi invece di "Il backend non è d'accordo"
- Gestire il caso "backend offline" con un messaggio gentile + retry automatico
- Gestire timeout sulle chiamate HTTP (oggi `requests.get/post` senza timeout → può bloccare l'app indefinitamente)
- Aggiungere `timeout=5` a tutte le chiamate `requests` in `backend_integration.py`

**Perché**: oggi se il backend non risponde l'app crasha o mostra messaggi incomprensibili.

---

## 🔲 Pulizia codice e separazione responsabilità

**Priorità**: Media  
**File coinvolti**: `meal_controller.py`, `backend_integration.py`, `config.py`, `learning/`, `base.html`

**Cosa fare**:
- Spostare `requests.post` di inserimento pasto dal controller nel `BackendIntegration` (c'è ancora il TODO nel codice che lo chiede)
- Consolidare `load_config()` — oggi è chiamata sia a livello modulo che via `get_config()`
- Rimuovere cartella `learning/` dal repo (contiene esperimenti, non fa parte dell'app)
- Rimuovere CSS commentato in `base.html` (prima riga del link Bootstrap 4.4.1)
- Estrarre stringhe italiane in costanti o file separato (primo passo verso i18n)
- Aggiungere type hints ai metodi di `BackendIntegration`

**Perché**: debito tecnico accumulato rende ogni modifica più rischiosa del necessario.

---

## 🔲 Miglioramenti minori

**Priorità**: Bassa

- [ ] **Filtri frequenze senza refresh** — la pagina frequenze oggi fa `location.reload()` a ogni click; usare `fetch()` + DOM update
- [ ] **Ordinamento tabella frequenze** — oggi i risultati sono in ordine dal backend, non riordinabili
- [ ] **Conferma cancellazione via POST** — oggi la delete passa per GET con query params (vulnerabile a CSRF, browser pre-fetching)
- [ ] **Validazione lato client** — il campo "Pasto" ha `required` HTML5, ma nessun feedback visivo personalizzato
- [ ] **Dark mode** — media query `prefers-color-scheme: dark` per usare l'app di sera senza accecarsi

---

## Note

- **Backend**: il backend (`meal-tracker:0.3.0`, richiesto dalla 1.1.0 per `?date=`) è gestito separatamente; le modifiche qui sono solo lato webapp
- **Test**: eseguire sempre `.venv/bin/python -m pytest tests/ -v` prima e dopo ogni modifica
- **Ambiente dev**: `bash run-for-testing.sh` (porta 15002, debug mode; avvia un backend di prova via `deployment/docker-compose.yml`, solo per test)
- **Docker build**: `bash script-docker-build.sh` per creare l'immagine
