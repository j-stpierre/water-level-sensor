from dotenv import dotenv_values
from os import path
import sys

config = dotenv_values(path.join(sys.path[0], ".env")) 