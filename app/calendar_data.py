import json
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import current_app


@dataclass
class Day:
    id: int
    unlock_at: datetime
    title: str
    image: str
    note: str

    def is_unlocked(self, now: datetime) -> bool:
        return now >= self.unlock_at


def _tz() -> ZoneInfo:
    return ZoneInfo(current_app.config["TIMEZONE"])


def load_days() -> list[Day]:
    with open(current_app.config["DATA_FILE"], encoding="utf-8") as f:
        raw = json.load(f)

    tz = _tz()
    days = [
        Day(
            id=entry["id"],
            unlock_at=datetime.fromisoformat(entry["unlock_at"]).replace(tzinfo=tz),
            title=entry["title"],
            image=entry["image"],
            note=entry["note"],
        )
        for entry in raw
    ]
    return sorted(days, key=lambda d: d.unlock_at)


def get_day(day_id: int) -> Day | None:
    return next((d for d in load_days() if d.id == day_id), None)


def now() -> datetime:
    return datetime.now(_tz())
