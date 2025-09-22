from flask import Flask
import os

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.pardir, 'static'),
    template_folder=os.path.join(os.path.pardir, 'templates')
)

from asr_to_sign import routes