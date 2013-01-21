from flask.ext.assetslite import Assets, Bundle
from flask.ext.assetslite.filters import cssmin, uglifyjs
from flask.ext.assetslite.filters import less as lessfilter


less = [
    # Pull in all less stylesheets (order is not important)
    'less/*.less',
]

css = [
    # Pull in all CSS stylesheets (order is not important)
    'css/*.css',
    Bundle(less, filters=lessfilter),
]

js = [
    'js/jquery*.js',
    'js/resumable.js',
    'js/default.js',
    # Only included in debug mode
    Bundle('js/less-*.min.js', build=False),
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
