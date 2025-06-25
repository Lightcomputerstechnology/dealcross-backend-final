import os
import re
from termcolor import colored

MODELS_DIR = "models"
pattern = re.compile(r'ForeignKeyField\s*
