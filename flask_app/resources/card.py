import logging

from flask_app.database.database import Card
from flask_app.serialize import card_list_schema
from flask_restful import Resource

CARDS_ENDPOINT = '/cards'


class CardListResource(Resource):
    def get(self):
        logging.info('GET %s', CARDS_ENDPOINT)

        cards: list = Card.query.all()

        if cards:
            return {"cards": card_list_schema.dump(cards)}
        else:
            return {"error": "No cards found in database"}
