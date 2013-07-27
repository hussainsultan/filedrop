import os
from os.path import abspath, relpath
from flask import Flask, request_finished

import assets
import jinja
import logging
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
    uploads.init(app)
    assets.init(app)

    # Add request hook to change x-sendfile to x-accel-redirect (for nginx)
    @request_finished.connect_via(app)
    def nginx_sendfile_patch(sender, response):
        if 'X-Sendfile' in response.headers:
            filepath = '/' + relpath(response.headers['X-Sendfile'],
                                     abspath(app.config['UPLOADS_DEFAULT_DEST']))
            response.headers['X-Accel-Redirect'] = filepath
            del response.headers['X-Sendfile']

    app.register_blueprint(views.main)

    return app
