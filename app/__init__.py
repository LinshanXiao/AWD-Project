from flask import Flask

application = Flask(__name__)
application.config['SECRET_KEY'] = 'our_secret_key_here'

import app.routes



