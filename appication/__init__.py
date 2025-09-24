from flask import Flask
from .extensions import db, ma
from .routes import bp


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object("config")

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(bp)
    return app