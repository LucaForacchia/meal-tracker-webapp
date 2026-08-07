# MealTracker WebApp — Roadmap

Ultimo aggiornamento: 2026-08-06 (sessione Codewhale)

---

## ✅ Completato (sessione 2026-08-03/06)

- [x] **Form inserimento mobile-first** — layout compatto, Chi+Tipo e Dessert+Note affiancati, heading ridotto, CSS touch target 48px, data preimpostata a oggi
- [x] **Toggle "Nuova settimana"** — sostituita checkbox nativa con Bootstrap custom-switch (label + interruttore iOS-style)
- [x] **Bug Start week** — corretto: prima inviava sempre `true` (controllava presenza chiave, non valore)
- [x] **Feedback inserimento** — flash message dopo submit (successo ✓ / errore), redirect POST→GET per evitare ri-submit
- [x] **Dessert sempre visibile** — rimosso toggle checkbox, ora campo normale con placeholder "Opzionale"
- [x] **`app.secret_key`** — aggiunta in `main.py` (necessaria per `flash()`)
- [x] **Test suite** — 12 test pytest in `tests/test_meal_insertion.py` (GET, start_week, dessert, flash)
- [x] **Rimosso codice morto** — `time.sleep(0.5)`, `raise Exception`, `<head>` illegale dentro `<body>`, `myFunction()`/`myCheck`

---

## 🔲 PWA — Rendi l'app installabile sulla home del telefono

**Priorità**: Alta  
**File coinvolti**: `src/static/` (nuovi), `src/templates/base.html`, `src/main.py`

**Cosa fare**:
- Creare `manifest.json` con nome app, icona, colore tema, `display: standalone`
- Aggiungere `<link rel="manifest">` in `base.html`
- Service worker basilare (`sw.js`) con cache delle risorse statiche (CSS/JS Bootstrap da CDN, template)
- Registrare il service worker in `base.html`
- L'app resta online-only (cache solo risorse statiche, non dati)

**Perché**: aprire il browser e digitare l'IP ogni volta è scomodo; installata in home screen sembra un'app nativa.

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

- **Backend**: il backend (`meal-tracker:0.2.0`) è gestito separatamente; le modifiche qui sono solo lato webapp
- **Test**: eseguire sempre `pytest tests/ -v` prima e dopo ogni modifica
- **Ambiente dev**: `bash run-for-test.sh` (porta 15002, debug mode)
- **Docker build**: `bash script-docker-build.sh` per creare l'immagine
