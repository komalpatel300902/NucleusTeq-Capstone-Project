# logging_config.py

import logging

def setup_logging():
    logging.basicConfig(
        filename='app.log',
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.NOTSET,
        # handlers=[
        # logging.FileHandler('app.log'),
        # logging.StreamHandler()
    # ]
    )

    # # Optionally, you can add more handlers here if needed
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)
    # console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    # console_handler.setFormatter(console_formatter)
    # return logging.getLogger(__name__)
