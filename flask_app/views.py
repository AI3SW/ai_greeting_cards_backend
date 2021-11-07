import logging
import time
from pathlib import Path

from flask import Blueprint, current_app, render_template, request
from PIL import Image

from flask_app.commons.util import image_to_base64
from flask_app.model import model_store

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

        # TODO: implement model inference
        # return dummy image
        img_path = (Path(current_app.config["ASSETS_PATH"])
                    / 'dummy/transformed.jpeg').resolve()
        img = Image.open(img_path)
        base64_img = image_to_base64(img)

        response = {'output_img': base64_img}

        end_time = time.time()
        logging.info('Total prediction time: %.3fs.' % (end_time - start_time))

        return response

    except Exception as error:
        logging.exception(error)
        return {'error': 'Error in prediction'}


@blueprint.route('/email', methods=['POST'])
def email():
    logging.info("POST /email")
    req = request.get_json()

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
