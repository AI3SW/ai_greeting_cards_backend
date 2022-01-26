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
    'SIM_SWAP_PREDICT_URL': 'http://<SIMSWAP_IP>/predict'
}

ASSETS_PATH = './assets'

INPUT_IMG_PATH = "./resources/input_img"
OUTPUT_IMG_PATH = "./resources/output_img"

# redis config
SESSION_TYPE = 'redis'

# Config for sending email
MAIL_DEBUG = False

##########                      Mailtrap                    ##########
##########  We use Mailtrap for development and testing     ##########
# MAIL_SERVER = 'smtp.mailtrap.io'
# MAIL_PORT = 2525
# MAIL_USE_TLS = True

##########                      SendGrid                    ##########
# https://sendgrid.com/blog/sending-emails-from-python-flask-applications-with-twilio-sendgrid/
MAIL_SERVER = 'smtp.sendgrid.net'
MAIL_PORT = 587
MAIL_USE_TLS = False
