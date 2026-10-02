## [1.1.0] - 2026-10-02
Requires backend >= 0.3.0 (`GET /meal/week?date=`).

## Added
- "Vai a data" button on the weekly view: opens the date picker and shows the week containing the chosen date; dates outside the tracked period show the backend message "Data fuori periodo tracciato" with a link back to the last week
- Banner "Non connesso al server. Copia del gg/mm hh:mm" when the page shown is the copy cached by the service worker (server not reachable): pages carry their render time, `/ping` checks reachability on load and when the app comes back to foreground
- Tests for the weekly view, the date lookup and the reachability check

## Changed
- Service worker cache renamed to `mealtracker-v2`: pages cached by 1.0.0 are dropped
- Python upgraded from 3.10 to 3.13.12, identical in Docker (`python:3.13.12-slim`), local (_.python-version_) and tests
- All dependencies locked: runtime in _requirements.txt_ (Flask 3.1.3, requests 2.34.2, ...), test tools in _requirements-dev.txt_; local development uses a `.venv` matching the Docker image

## Fixed
- Weekly view with a non-integer `week-number` crashed (500): it now shows the error message

## [1.0.0] - 2026-08-07
## Added
- First stable release — app installable as a PWA from the phone home screen
- PWA support: web app manifest (`/manifest.json`), service worker (`/sw.js`) and generated app icons (192x192, 512x512, maskable)
- App installable on the home screen (display: standalone, theme color matching the navbar)
- Service worker cache strategy: cache-first for static assets/CDN libraries, network-first for navigations with fallback to the last visited page (app shell); backend data stays online-only

## [0.6.0] - 2026-08-06
## Added
- Mobile-first meal insertion form (compact layout, fits in one screen on mobile)
- Date field pre-filled with today's date
- "New Week" toggle switch (Bootstrap custom-switch) replacing the checkbox
- Flash feedback (success/error) after meal insertion
- app.secret_key support (via SECRET_KEY env var with dev fallback)
- Test suite: 12 pytest tests in tests/test_meal_insertion.py
- Roadmap file (TODO.md) tracking future improvements

## Fixed
- Start Week always sent as `true` even when not toggled (checked key presence instead of value)
- Broken Jinja block in insertion.html (`% block style %` missing braces)
- Illegal `<head>` tag inside `<body>` in insertion.html
- RuntimeError on flash() due to missing app.secret_key

## Changed
- Dessert and Notes fields always visible (no checkbox to reveal dessert)
- Chi+Tipo and Dessert+Note fields side by side (col-6)
- POST /meals/ now redirects after insertion (prevents re-submit on refresh)
- Removed artificial time.sleep(0.5) after insertion

## Removed
- Dead code: myFunction()/myCheck checkbox logic, commented-out bootstrap CSS link

## [0.5.3] - 2025-05-29
## Fixed
- Autocomplete scripts now automatically discards null value

## [0.5.2] - 2025-03-06
## Added
- Filtering meals count for participants
- Backend version in the welcome page

## Changed
- Extended meals list to 100 items

## [0.5.1] - 2025-03-06
## Removed
- Useless replacement page (currently handled manually)

## [0.4.0] - 2023-09-26 


## [0.3.0] - 2023-03-02
## Added
- Dessert handling

## Removed
- Get last meal