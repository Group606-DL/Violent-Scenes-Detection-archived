import logging

# TODO: change to debug level to env variable and add file handler
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# create handlers and add formatter
handlers = [logging.StreamHandler()]
for handler in handlers:
    handler.setFormatter(formatter)
    logger.addHandler(handler)
