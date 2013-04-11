import os
import subprocess
from app import create_app
from flask import current_app
from flask.ext.script import Shell, Manager, Server

manager = Manager(create_app)


@manager.command
def mustache_compile():
    """
    Pre-compiles all Mustache templates in the Jinja environment
    """
    result = set()

    # get any mustache templates in the main app
    all_templates = current_app.jinja_loader.list_templates()

    for template_name in all_templates:
        if template_name.endswith('mustache'):
            template_path = os.path.realpath(os.path.join(current_app.root_path, current_app.template_folder, template_name))
            result.add(template_path)

    # get all the blueprint mustache templates
    for name, blueprint in current_app.blueprints.iteritems():
        loader = blueprint.jinja_loader
        if loader is not None:
            for template_name in loader.list_templates():
                if template_name.endswith('mustache'):
                    template_path = os.path.realpath(os.path.join(blueprint.root_path, blueprint.template_folder, template_name))
                    result.add(template_path)

    if result:
        args = list(result)
        args.insert(0, 'hulk')

        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        path = os.path.realpath(os.path.join(current_app.root_path, current_app._static_folder, 'assets', 'tmp', 'mustache-compiled-templates.min.js'))
        with open(path, 'w') as f:
            f.write(stdout)


def _make_shell_context():
    """
    Shell context: import helper objects here.
    """
    from app.extensions.db import db
    return dict(app=current_app, db=db)


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

if __name__ == "__main__":
    manager.run()
