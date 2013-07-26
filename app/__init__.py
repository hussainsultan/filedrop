import os
from flask import Flask

import assets
import jinja
import logging
import toolbar
import uploads
import views


def create_app(config=None):
    """
    Create and initialise the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('%s/config/default.py' % app.root_path)

    if config:
        app.config.from_pyfile(config)
    elif os.getenv('FLASK_CONFIG'):
        app.config.from_envvar('FLASK_CONFIG')

    logging.init(app)
    jinja.init(app)
    toolbar.init(app)
    uploads.init(app)
    assets.init(app)

    app.register_blueprint(views.main)

    return app
