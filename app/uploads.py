from flask.ext.uploads import configure_uploads
from flask.ext.uploads import UploadSet, ALL, patch_request_class


partial = UploadSet('partial', ALL)
files = UploadSet('files', ALL)
tmp = UploadSet('tmp', ALL)

# List of upload sets to be initialised with the app
upload_sets = [
    partial,
    files,
    tmp,
]


def init(app):
    """
    Attach upload sets to the app and initialise uploads.
    """
    for set in upload_sets:
        configure_uploads(app, set)
    # Allow uploads up to 20MiB
    patch_request_class(app, size=(20 * 1024 * 1024))
