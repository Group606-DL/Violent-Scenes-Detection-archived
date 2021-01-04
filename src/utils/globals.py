import logging
import configparser

# Read local `config.ini` file.
config = configparser.ConfigParser()
config.read('./config.ini')

# TODO: Add file handler
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(config['LOG']['LEVEL']))

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# create handlers and add formatter
handlers = [logging.StreamHandler()]
for handler in handlers:
    handler.setFormatter(formatter)
    logger.addHandler(handler)
