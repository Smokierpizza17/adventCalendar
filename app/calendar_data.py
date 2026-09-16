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
    photo: str
    note: str
    month: str
    is_cover: bool = False

    def is_unlocked(self, now: datetime) -> bool:
        return self.is_cover or now >= self.unlock_at


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
            photo=entry["photo"],
            note=entry["note"],
            month=entry["month"],
            is_cover=entry.get("is_cover", False),
        )
        for entry in raw
    ]
    return sorted(days, key=lambda d: d.unlock_at)


def get_day(day_id: int) -> Day | None:
    return next((d for d in load_days() if d.id == day_id), None)


def now() -> datetime:
    return datetime.now(_tz())
