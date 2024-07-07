from dotenv import load_dotenv
import os

from const import env_variables


load_dotenv()

if any(key not in os.environ for key in env_variables):
    print(f'Create .env file with following data:\n{env_variables}')
    quit()

TOKEN = os.environ['TOKEN']
DBFILE = os.environ['DBFILE']
