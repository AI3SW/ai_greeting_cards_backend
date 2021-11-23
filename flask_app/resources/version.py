import logging

from flask_app.database.database import Version
from flask_app.serialize import version_schema
from flask_restful import Resource

VERSION_ENDPOINT = '/version'


class VersionResource(Resource):
    def get(self):
        logging.info('GET %s', VERSION_ENDPOINT)
        version = Version.query.first_or_404()
        return version_schema.dump(version)
