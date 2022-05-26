from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['ENVIRONMENT_VAR'] = []
app.config['TOTALS_DICT'] = {}

from app import routes, models