import logging
import time
from pathlib import Path

from flask import Blueprint, current_app, render_template, request
from PIL import Image

from flask_app.commons.util import pil_to_base64
from flask_app.database.database import Card
from flask_app.model import model_store, simswap

blueprint = Blueprint('blueprint', __name__)


@blueprint.route('/')
def index():
    logging.info("GET /")
    return render_template('index.html')


@blueprint.route('/image', methods=['POST'])
def predict():
    logging.info("POST /image")
    req = request.get_json()

    expected_keys = {'img', 'card_id'}
    if req.keys() != expected_keys:
        missing_keys = expected_keys - req.keys()
        error_msg = f"keys missing from request {missing_keys}"
        logging.exception(error_msg)
        return {'error': error_msg}

    try:
        start_time = time.time()

        # get inputs
        input_base64 = req.get('img')
        card_id = req.get('card_id')

        # get requested card asset in base64 encoded string
        card = Card.query.get_or_404(card_id)
        card_img_path = (Path(current_app.config['ASSETS_PATH'])
                         / card.img_path).resolve()
        card_pil = Image.open(card_img_path)
        card_base64 = pil_to_base64(card_pil)

        # cookie/session handling
        # TODO: generate user id and place in cookie/session

        # model inference
        model: simswap.SimSwapModel = model_store['simswap']
        output_base64: str = model.predict(src_image=input_base64,
                                           ref_img=card_base64)

        ###############     START DATABASE      ###############
        # TODO: implement database section
        # save input and outputs
        # save session

        ###############     END DATABASE        ###############

        # send back response
        response = {'output_img': output_base64}

        end_time = time.time()
        logging.info('Total prediction time: %.3fs.' % (end_time - start_time))

        return response

    except Exception as error:
        logging.exception(error)
        return {'error': 'Error in prediction'}


@blueprint.route('/email', methods=['POST'])
def email():
    logging.info("POST /email")

    try:
        req = request.get_json()
    except Exception as error:
        logging.error(error)
        return {
            'success': False,
            'error': 'email not sent'
        }

    expected_keys = {
        'sender_name', 'sender_email',
        'recipient_name', 'recipient_email', 'message'
    }
    if req.keys() != expected_keys:
        missing_keys = expected_keys - req.keys()
        error_msg = f"keys missing from request {missing_keys}"
        logging.exception(error_msg)
        return {
            'success': False,
            'error': error_msg
        }

    try:
        start_time = time.time()

        # TODO: implement emailing of card
        # return dummy response
        response = {'success': True}

        end_time = time.time()
        logging.info('Total time to email: %.3fs.' % (end_time - start_time))

        return response

    except Exception as error:
        logging.exception(error)
        return {
            'success': False,
            'error': 'email not sent'
        }
