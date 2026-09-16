"""Prerender square, low-res grid thumbnails for each day's photo.

Reads data/days.json, and for every entry's "photo" produces a center-cropped
square thumbnail in app/static/images/thumbs/, used by the grid page instead
of the full-size image. Run this whenever you add or change a day's photo.

Usage:
    python scripts/generate_thumbnails.py [--force] [--size 480]
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "days.json"
IMAGES_DIR = ROOT / "app" / "static" / "images"
THUMBS_DIR = IMAGES_DIR / "thumbs"

DEFAULT_SIZE = 480


def generate(size: int, force: bool) -> None:
    with open(DATA_FILE, encoding="utf-8") as f:
        days = json.load(f)

    THUMBS_DIR.mkdir(parents=True, exist_ok=True)

    photos = sorted({entry["photo"] for entry in days})
    made, skipped, missing = 0, 0, []

    for photo in photos:
        src = IMAGES_DIR / photo
        dst = THUMBS_DIR / photo

        if not src.exists():
            missing.append(photo)
            continue

        if not force and dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            skipped += 1
            continue

        with Image.open(src) as img:
            img = ImageOps.exif_transpose(img)
            thumb = ImageOps.fit(img, (size, size), Image.LANCZOS)
            if thumb.mode in ("RGBA", "P") and dst.suffix.lower() in (".jpg", ".jpeg"):
                thumb = thumb.convert("RGB")
            thumb.save(dst, quality=80)
        made += 1

    print(f"Generated {made}, skipped {skipped} (up to date), missing {len(missing)}.")
    if missing:
        print("Missing source images:")
        for photo in missing:
            print(f"  {photo}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="regenerate even if thumb is up to date")
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE, help="thumbnail edge length in pixels")
    args = parser.parse_args()

    if not DATA_FILE.exists():
        print(f"Data file not found: {DATA_FILE}", file=sys.stderr)
        sys.exit(1)

    generate(args.size, args.force)


if __name__ == "__main__":
    main()
