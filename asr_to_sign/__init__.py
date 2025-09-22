from flask import Flask

app = Flask(__name__)

from asr_to_sign import routes