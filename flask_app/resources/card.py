import logging

from flask_app.database.database import Card
from flask_app.serialize import card_list_schema
from flask_restful import Resource

CARDS_ENDPOINT = '/cards'


class CardListResource(Resource):
    def get(self):
        logging.info('GET %s', CARDS_ENDPOINT)
        # cards = Card.query.all()
        # TODO: remove returning of dummy data
        cards = [
            Card(id=1, name='dummy_1', img_path='dummy/raw.jpg'),
            Card(id=2, name='dummy_2', img_path='dummy/raw.jpg')
        ]

        return {"cards": card_list_schema.dump(cards)}
