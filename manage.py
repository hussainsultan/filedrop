import subprocess
from os.path import join
from app import create_app
from flask import current_app
from flask.ext.script import Shell, Manager, Server

manager = Manager(create_app)


def _make_shell_context():
    """
    Shell context: import helper objects here.
    """
    return dict(app=current_app)


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
def maintenance():
    """
    Prune old invites and partial uploads.
    """
    # Delete partial uploads older than 7 days
    subprocess.call(['find',
                     join(current_app.config['UPLOADS_DEFAULT_DEST'], 'partial'),
                     '-type', 'f', '-mtime', '+7', '-delete'])
    # Prune empty dirs
    subprocess.call(['find',
                     join(current_app.config['UPLOADS_DEFAULT_DEST'], 'partial'),
                     '-type', 'd', '-mtime', '+7', '-empty', '-exec', 'rmdir',
                     '\'{}\'', ';'])
    # Delete old unused invites
    subprocess.call(['find',
                     join(current_app.config['UPLOADS_DEFAULT_DEST'], 'slugs'),
                     '-maxdepth', '1', '-type', 'f', '-mtime', '+7', '-size',
                     '0', '-delete'])


if __name__ == '__main__':
    manager.run()
