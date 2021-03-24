from dotenv import dotenv_values
from os import path

ROOT_DIR = path.dirname(path.abspath(".env"))
config = dotenv_values(path.join(ROOT_DIR, ".env")) 
