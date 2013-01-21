from flask.ext.debugtoolbar import DebugToolbarExtension


def init(app):
    DebugToolbarExtension(app)
