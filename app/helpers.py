import os
import errno
from flask import flash


def flash_errors(form):
    """
    Based on http://flask.pocoo.org/snippets/12/
    """
    for field, errors in form.errors.iteritems():
        for error in errors:
            flash('<strong>%s</strong>: %s' % (
                getattr(form, field).label.text,
                error
            ), 'error')


def read(fhandle, chunk_size=1024):
    """Lazy function (generator) to read a file object piece by piece."""
    while True:
        data = fhandle.read(chunk_size)
        if not data:
            break
        yield data


def mkdir_p(path):
    """
    Ensures a directory path exists, and creates it if it doesn't.
    `mkdir -p` for Python.
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
