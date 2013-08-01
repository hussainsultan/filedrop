import subprocess
from os.path import join, abspath, dirname
from app import create_app
from flask import current_app
from flask.ext.script import Shell, Manager, Server

manager = Manager(create_app)


def _make_shell_context():
    """
    Shell context: import helper objects here.
    """
    from app.db import db
    from app.ldapconn import ldap
    return dict(app=current_app, db=db, ldap=ldap)


manager.add_option('--flask-config', dest='config', help='Specify Flask config file', required=False)
manager.add_command('shell', Shell(make_context=_make_shell_context))
manager.add_command('runserver', Server(host='0.0.0.0'))


@manager.command
def build():
    """
    Build static assets.
    """
    from app.assets import init
    environment = init(current_app)
    environment.build_all()


@manager.command
def compile_templates():
    """
    Compile JS templates.
    """
    static_folder = join(abspath(dirname(__file__)), 'app', 'static')
    template_output_file = join(static_folder, 'assets', 'tmp', 'templates.js')
    template_dir = join(static_folder, 'js', 'app', 'templates')
    # Truncate file and open for writing
    with open(template_output_file, 'w') as output_file:
        # Build 'em templates
        subprocess.call(['nunjucks-precompile', template_dir], stdout=output_file)


if __name__ == '__main__':
    manager.run()
