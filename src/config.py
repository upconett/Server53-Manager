from dotenv import load_dotenv
import os

from const import env_variables

load_dotenv()

if any(key not in os.environ for key in env_variables):
    print(f'Create .env file with following data:\n{env_variables}')
    quit()

BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_USERNAME = os.environ['BOT_USERNAME']
DBFILE = os.environ['DBFILE']
IMAGES_PATH = os.environ['IMAGEMAPS_PATH']
RCON_HOST = os.environ['RCON_HOST']
RCON_PORT = os.environ['RCON_PORT']
RCON_PASSWORD = os.environ['RCON_PASSWORD']
