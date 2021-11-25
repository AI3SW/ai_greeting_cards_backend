import logging
from logging.config import dictConfig
from pathlib import Path

from config import LOGGING_CONFIG
from flask import Flask
from flask_cors import CORS

dictConfig(LOGGING_CONFIG)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    # flask-cors
    CORS(app, resources=r'/*')

    # init model store
    from flask_app.model import init_model_store
    try:
        init_model_store(app)
    except Exception:
        logging.exception('Unable to init model store. Raising error.')
        raise

    # register blueprints
    from flask_app.views import blueprint
    app.register_blueprint(blueprint)

    # register db
    from flask_app.database import db
    db.init_app(app)

    # register serializer
    from flask_app.serialize import ma
    ma.init_app(app)

    # register api resources
    from flask_restful import Api

    from flask_app.resources.card import CARDS_ENDPOINT, CardListResource
    from flask_app.resources.version import VERSION_ENDPOINT, VersionResource

    api = Api(app)
    api.add_resource(CardListResource, CARDS_ENDPOINT)
    api.add_resource(VersionResource, VERSION_ENDPOINT)

    # create resources directory if needed
    Path(app.config["INPUT_IMG_PATH"]).mkdir(exist_ok=True, parents=True)
    Path(app.config["OUTPUT_IMG_PATH"]).mkdir(exist_ok=True, parents=True)

    return app
