import logging
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, current_app, render_template, request, session
from PIL import Image

from flask_app.commons.util import base64_to_pil, pil_to_base64
from flask_app.database import db
from flask_app.database.database import Card, InputImg, OutputImg, Session
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

        db_start_time = time.time()

        ##### save images #####
        input_img, output_img = _save_images(input_base64, output_base64)

        # add and commit images in SQLAlchemy format
        # Need to do commit to db first so that we can get input and output image's id
        db.session.add_all([input_img, output_img])
        db.session.commit()
        ##### end save images #####

        ##### save user and session #####
        # TODO: generate and save user
        session_obj = Session(user_id="dummy_user_id",
                              card_id=card_id,
                              input_img_id=input_img.id,
                              output_img_id=output_img.id,
                              start_time=datetime.fromtimestamp(start_time, timezone.utc))

        db.session.add(session_obj)
        db.session.commit()
        ##### save user and session #####

        db_end_time = time.time()
        logging.info('Total databasing time: %.3fs.' %
                     (db_end_time - db_start_time))

        ###############     END DATABASE        ###############

        # cache file path of output_img
        session['output_img'] = output_img.file_path

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

        # get file path of output image
        output_img_path = session.get('output_img')

        if output_img_path:
            response = {'success': True}

            end_time = time.time()
            logging.info('Total time to email: %.3fs.' %
                         (end_time - start_time))

            session.clear()

            return response

        else:
            error_msg = f"No output image was found for current web session."
            logging.exception(error_msg)
            return {
                'success': False,
                'error': error_msg
            }

    except Exception as error:
        logging.exception(error)
        return {
            'success': False,
            'error': 'email not sent'
        }


def _save_images(input_base64, output_base64):
    # process input
    input_pil = base64_to_pil(input_base64)
    input_file_path = Path(current_app.config['INPUT_IMG_PATH']) \
        / f'{uuid.uuid4()}.jpg'
    input_pil.save(input_file_path)
    input_img = InputImg(file_path=str(input_file_path.resolve()))

    # process output
    output_pil = base64_to_pil(output_base64)
    output_file_path = Path(current_app.config['OUTPUT_IMG_PATH']) \
        / f'{uuid.uuid4()}.jpg'
    output_pil.save(output_file_path)
    output_img = OutputImg(file_path=str(output_file_path.resolve()))
    return input_img, output_img
