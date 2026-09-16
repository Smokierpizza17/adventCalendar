from flask import Blueprint, abort, render_template

from . import calendar_data

bp = Blueprint("calendar", __name__)


@bp.route("/")
def index():
    current_time = calendar_data.now()
    days = load_days_with_state(current_time)
    return render_template("index.html", days=days)


@bp.route("/day/<int:day_id>")
def day(day_id):
    entry = calendar_data.get_day(day_id)
    if entry is None:
        abort(404)

    current_time = calendar_data.now()
    if not entry.is_unlocked(current_time):
        return render_template("day.html", day=entry, locked=True)

    return render_template("day.html", day=entry, locked=False)


def load_days_with_state(current_time):
    return [
        {"day": d, "unlocked": d.is_unlocked(current_time)}
        for d in calendar_data.load_days()
    ]
