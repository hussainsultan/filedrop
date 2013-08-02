from flask import request

from .auth import is_authenticated


def init(app):
    @app.context_processor
    def debug(debug=app.debug):
        """
        Notify templates that they're in debug mode
        """
        return dict(debug=debug)

    @app.context_processor
    def request_global():
        """
        Make request available in templates
        """
        return dict(request=request)

    @app.context_processor
    def authenticated():
        """
        Whether or not this request is coming from an allowed IP network
        (and hence able to upload files).
        """
        return dict(authenticated=is_authenticated(request))
