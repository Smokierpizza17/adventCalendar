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

    @app.url_defaults
    def add_static_cache_buster(endpoint, values):
        if (
            endpoint == "static"
            and "filename" in values
            and not values["filename"].startswith("images/")
        ):
            file_path = os.path.join(app.static_folder, values["filename"])
            try:
                values["v"] = int(os.path.getmtime(file_path))
            except OSError:
                pass

    from . import routes

    app.register_blueprint(routes.bp)

    return app
