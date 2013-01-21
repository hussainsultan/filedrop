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
