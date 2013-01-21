from flask import Blueprint, render_template
from os.path import basename, dirname, realpath
main = Blueprint(basename(dirname(realpath(__file__))), __name__,
                      template_folder='templates',
                      static_folder='static')


@main.route('/')
def index():
    return render_template('welcome.jinja')
