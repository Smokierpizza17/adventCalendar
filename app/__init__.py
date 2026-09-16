import os

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DATA_FILE=os.environ.get(
            "ADVENT_DATA_FILE",
            os.path.join(app.root_path, "..", "data", "days.json"),
        ),
        TIMEZONE=os.environ.get("ADVENT_TIMEZONE", "UTC"),
    )

    from . import routes

    app.register_blueprint(routes.bp)

    return app
