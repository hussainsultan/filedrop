from flask.ext.assetslite import Assets, Bundle
from flask.ext.assetslite.filters import cssmin, uglifyjs


css = [
    # Pull in all CSS stylesheets (order is not important)
    'css/*.css',
]

js = [
    'js/jquery*.js',
    'js/bootstrap.js',
    'js/underscore.js',
    'js/resumable.js',
    'js/app.js',
]


def init(app):
    """
    Initialise assets on the app.
    """
    environment = Assets(app)
    environment.register('css', Bundle(css,
                                       output='assets/css/combined.%s.css',
                                       filters=cssmin))

    environment.register('js', Bundle(js,
                                      output='assets/js/combined.%s.js',
                                      filters=uglifyjs))
    return environment
