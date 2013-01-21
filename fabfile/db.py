"""
fabfile module for managing database-related tasks.
"""
from fabric.api import task
from fabric.context_managers import settings, hide
from fabric.colors import cyan
from fabfile.utils import do
from fabfile.virtualenv import venv_path

DB = {
    'name': 'app',
    'user': 'www-data',
}


@task
def build():
    """Initialise and migrate database to latest version."""
    print(cyan('\nUpdating database...'))

    # Ensure database exists
    if not _pg_db_exists(DB['name']):
        do('createdb -O \'%(user)s\' \'%(name)s\'' % DB)

    # Ensure versions folder exists
    do('mkdir -p db/versions')

    # Run migrations
    do('%s/bin/alembic -c db/alembic.ini upgrade head' % venv_path)


@task
def generate(message=None):
    """Generates a new Alembic revision based on DB changes."""
    args = ''
    if message:
        args = '-m "%s"' % message
    do('%s/bin/alembic -c db/alembic.ini revision --autogenerate %s' % (venv_path, args))


def _pg_db_exists(database):
    """
    Helper function to check if the postgresql database exists.
    """
    with settings(hide('running', 'warnings'), warn_only=True):
        return do('psql -tAc "SELECT 1 FROM pg_database WHERE datname = \'%s\'" postgres |grep -q 1' % database, capture=True).succeeded
