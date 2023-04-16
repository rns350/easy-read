# Standard Library Imports
import logging, os
from datetime import date

if not os.path.exists('logs'):
    os.mkdir('logs')

# Define the log and date format for the log handlers, and create a Formatter
log_format = f'%(levelname)s | %(asctime)s | {__file__} | line %(lineno)d | %(message)s'
date_format = '%m/%d/%Y %I:%M:%S %p'
formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

# Initialize the stream and file handlers - we will attach these to the logger
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename=f'logs/{date.today()}-logs.txt')

# set the formatter for the handlers to the one created above
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# create the logger and add the details
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
logger.addHandler(stream_handler)
logger.addHandler(file_handler)