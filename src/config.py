# Python модули
from dotenv import load_dotenv

import os
import logging


# Локальные модули
from const import env_variables


# Чтение переменных окружения из.env файла
load_dotenv(override=True)

if any(key not in os.environ for key in env_variables):
    logging.fatal(f'Create .env file with following data:\n{env_variables}')
    quit()

BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_USERNAME = os.environ['BOT_USERNAME']
DBFILE = os.environ['DBFILE']
IMAGES_PATH = os.environ['IMAGEMAPS_PATH']
RCON_HOST = os.environ['RCON_HOST']
RCON_PORT = os.environ['RCON_PORT']
RCON_PASSWORD = os.environ['RCON_PASSWORD']
ACCESS_CHECK_FREQUENCY = os.environ['ACCESS_CHECK_FREQUENCY']


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d.%m.%y [%H:%M:%S]"
)

for logger in logging.root.manager.loggerDict:
    if 'aiogram' in logger:
        logging.getLogger(logger).setLevel(logging.INFO)
