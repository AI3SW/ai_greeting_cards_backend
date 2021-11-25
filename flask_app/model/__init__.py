import logging
import time

from flask_app.model.simswap import SimSwapModel

model_store = {}


def init_model_store(app):
    logging.info('Loading model store...')
    start_time = time.time()

    model_store['simswap'] = SimSwapModel()
    model_store['simswap'].init_model(app.config)
    end_time = time.time()

    logging.info('Total time taken to load model store: %.3fs.' %
                 (end_time - start_time))
