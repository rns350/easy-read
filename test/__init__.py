import os, sys

from easy_reed._logger import logger
logger.error("Hello")

parent = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(parent, "easy_reed"))