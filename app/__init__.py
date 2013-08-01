import os
from os.path import abspath, relpath
from flask import Flask, request_finished, render_template

import assets
import api
import jinja
import logger
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

    logger.init(app)
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

    app.register_blueprint(views.blueprint)
    app.register_blueprint(api.blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/default.html'), 500

    return app
