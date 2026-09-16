# Advent Calendar

A small Flask advent calendar. Each day reveals an image pair once its unlock time has passed.

## Features

- Grid page (`/`) showing all days, grouped by month, with locked/unlocked state
- Per-day page (`/day/<id>`) that reveals the two pictures once unlocked
- Unlock times are timezone-aware and configurable
- An optional "cover" entry for front-matter that isn't a numbered day
- No database — everything is driven by a single `data/days.json` file

## Requirements

- Python 3.12+
- See [requirements.txt](requirements.txt): Flask, python-dotenv, tzdata, Pillow

## Setup

```
python -m venv venv
venv\Scripts\activate        # PowerShell: venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy data\days.example.json data\days.json   # first run only
```

Then drop your own images into `app/static/images/` and edit `data/days.json`
to reference them (see format below).

## Running

```
python run.py                # http://127.0.0.1:5000
```

or equivalently:

```
flask --app run run
```

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

- `unlock_at` is naive local time, interpreted in the `TIMEZONE` config value
  (default `UTC`, override with the `ADVENT_TIMEZONE` env var).
- `photo` and `note` are both filenames under `app/static/images/` — `photo`
  is the photo, `note` is a photo/scan of the handwritten note. Both unlock
  together.
- `month` groups entries on the grid page (`/`) — entries are grouped in file
  order, not sorted alphabetically, so keep same-month entries contiguous.
- `is_cover` (optional, default `false`) marks an entry as front-matter
  rather than a numbered day: it always renders unlocked regardless of
  `unlock_at`, and the grid shows it as a distinct chip instead of a day
  number.
- Add/edit entries directly in this file — there's no admin UI or database.

## Thumbnails

The grid page uses square, low-res thumbnails instead of full-size photos.
Regenerate them whenever you add or change a day's photo:

```
python scripts/generate_thumbnails.py [--force] [--size 480]
```

This reads `data/days.json` and writes cropped thumbnails to
`app/static/images/thumbs/`, skipping any that are already up to date unless
`--force` is passed.

## Deployment

For production (e.g. running on a Raspberry Pi), serve the app with
[gunicorn](https://gunicorn.org/) instead of the Flask dev server, managed by
systemd, and reverse-proxied through Caddy.

```
pip install gunicorn
gunicorn -w 2 -b 127.0.0.1:8000 'app:create_app()'
```

**systemd unit** (`/etc/systemd/system/japadvent.service`):

```ini
[Unit]
Description=japAdvent
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/japAdvent
Environment=ADVENT_TIMEZONE=UTC
ExecStart=/home/pi/japAdvent/venv/bin/gunicorn -w 2 -b 127.0.0.1:8000 'app:create_app()'
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl enable --now japadvent
```

**Caddy** (add to your existing `Caddyfile`):

```
advent.example.com {
    reverse_proxy 127.0.0.1:8000
}
```

## Configuration

Set these as environment variables (a `.env` file works via python-dotenv):

| Variable            | Default                  | Purpose                                   |
| ------------------- | ------------------------ | ------------------------------------------ |
| `SECRET_KEY`         | `dev`                     | Flask secret key                           |
| `ADVENT_DATA_FILE`   | `data/days.json`          | Path to the day entries file               |
| `ADVENT_TIMEZONE`    | `UTC`                     | Timezone used to interpret `unlock_at` and display times |

> **Windows note:** `tzdata` is a required dependency — the stdlib `zoneinfo`
> module has no system tz database to fall back on there, so `ZoneInfo(...)`
> raises without it.

## Project structure

```
run.py                       # dev entry point
app/
  __init__.py                 # app factory (create_app), reads config from env vars
  routes.py                   # / (grid of days) and /day/<id> (locked/unlocked view)
  calendar_data.py             # loads data/days.json, computes lock state
  templates/, static/          # Jinja templates and static assets
  static/images/               # day photos (gitignored, see below)
data/
  days.example.json            # template for days.json
  days.json                    # your real data (gitignored)
scripts/
  generate_thumbnails.py       # prerenders grid thumbnails
```

## User data

`data/days.json` and everything under `app/static/images/` (except
`.gitkeep`) are gitignored — they hold real unlock dates, titles, and
personal photos. Copy `data/days.example.json` to `data/days.json` and add
your own images to populate the calendar locally.

## Notes

- `days.json` is loaded fresh on every request — fine at this scale, but
  revisit if the calendar grows much beyond ~24 days or needs concurrent
  edits.
- There's no way to bypass the unlock time except changing the system clock
  or the config — intentional for a calendar like this.

This readme was generated by Claude.
