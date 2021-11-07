from pathlib import Path

from flask import current_app
from flask_marshmallow import Marshmallow
from PIL import Image

from flask_app.commons.util import image_to_base64
from flask_app.database.database import Version, Card

ma = Marshmallow()


class VersionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Version


class CardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Card
        exclude = ('img_path',)

    img = ma.Method("serialize_img")

    def serialize_img(self, obj: Card):
        img_path = (Path(current_app.config["ASSETS_PATH"])
                    / obj.img_path).resolve()
        img = Image.open(img_path)
        return image_to_base64(img)


version_schema = VersionSchema()
card_list_schema = CardSchema(many=True)
