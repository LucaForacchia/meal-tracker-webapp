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