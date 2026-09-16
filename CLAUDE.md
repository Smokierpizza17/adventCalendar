# japAdvent

A Flask advent calendar. Each day has a photo + note pair that stays locked until
a predefined unlock time, then reveals on its own page.

## Structure

- `run.py` — dev entry point (`flask --app run run` or `python run.py`)
- `app/__init__.py` — app factory (`create_app`), reads config from env vars
- `app/routes.py` — two routes: `/` (grid of days) and `/day/<id>` (locked/unlocked view)
- `app/calendar_data.py` — loads `data/days.json`, computes lock state via `Day.is_unlocked`
- `data/days.json` — the day entries (see format below)
- `app/templates/`, `app/static/` — Jinja templates and static assets (CSS, images)
  - Flask's default `templates/`/`static/` folders live inside the `app` package, not the project root
- `app/static/images/` — put day photos here (filenames referenced from `data/days.json`)

## Day entry format (`data/days.json`)

```json
{
  "id": 1,
  "unlock_at": "2026-12-01T00:00:00",
  "title": "Day 1",
  "image": "day01.jpg",
  "note": "The note text shown once unlocked."
}
```

- `unlock_at` is naive local time, interpreted in the `TIMEZONE` config value (default
  `Asia/Tokyo`, override with the `ADVENT_TIMEZONE` env var).
- `image` is a filename under `app/static/images/`.
- Add/edit entries directly in this file — there's no admin UI or database.

## Running locally

```
python -m venv venv
venv\Scripts\activate        # PowerShell: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py                # http://127.0.0.1:5000
```

## Notes

- No database — `days.json` is the single source of truth, loaded fresh on every
  request (fine at this scale; revisit if the calendar grows much beyond ~24 days
  or needs concurrent edits).
- `tzdata` is a required dependency on Windows: the stdlib `zoneinfo` module has no
  system tz database to fall back on there, so `ZoneInfo(...)` raises without it.
- Lock state is computed by comparing `now()` (in `TIMEZONE`) against each entry's
  `unlock_at` — there's no way to bypass this except changing the system clock or
  the config, which is intentional for a calendar like this.
