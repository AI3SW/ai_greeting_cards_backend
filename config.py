LOGGING_CONFIG = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'console': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }, 'file': {
        'class': 'logging.FileHandler',
        'formatter': 'default',
        'filename': './log.log'
    }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}

MODEL_CONFIG = {
    'SIM_SWAP_PREDICT_URL': 'http://10.2.0.202:5001/predict'
}

ASSETS_PATH = './assets'

INPUT_IMG_PATH = "./resources/input_img"
OUTPUT_IMG_PATH = "./resources/output_img"
