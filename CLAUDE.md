# japAdvent

A Flask advent calendar. Each day has an image pair — a photo and a photo of a
handwritten note — that stays locked until a predefined unlock time, then
reveals on its own page.

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
  "photo": "day01_photo.png",
  "note": "day01_note.png",
  "month": "December 2026",
  "is_cover": false
}
```

- `unlock_at` is naive local time, interpreted in the `TIMEZONE` config value (default
  `UTC`, override with the `ADVENT_TIMEZONE` env var).
- `photo` and `note` are both filenames under `app/static/images/` — `photo` is the
  photo, `note` is a photo/scan of the handwritten note. Both unlock together.
- `month` groups entries on the grid page (`/`) — entries are grouped in file order,
  not sorted alphabetically, so keep same-month entries contiguous in `days.json`.
- `is_cover` (optional, default `false`) marks an entry as front-matter rather than a
  numbered day: it always renders unlocked regardless of `unlock_at`, and the grid
  shows it as a distinct chip instead of a day number.
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
