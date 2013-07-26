from atomicfile import AtomicFile
from flask.ext.uploads import UploadSet, configure_uploads, ALL, patch_request_class
from werkzeug.datastructures import FileStorage


def atomic_save(self, dst, buffer_size=16384):
    """Overrides werkzeug's original FileStorage save method to provide
    atomic file save."""
    if type(dst) is str:
        # Create atomic file handle
        handle = AtomicFile(dst, 'wb')
        # Call original method
        self._save_original(handle, buffer_size)
        # Close AtomicFile handle, which will rename the file into place
        handle.close()
    else:
        # Don't change anything if we've been given a stream
        self._save_origin(dst, buffer_size)

# Patch FileStorage.save() to provide an atomic file save operation
#FileStorage._save_original = FileStorage.save
#FileStorage.save = atomic_save


# List of upload sets to be initialised with the app
UPLOAD_SETS = {
    'partial': UploadSet('partial', ALL),
    'repository': UploadSet('repository', ALL),
}


def init(app):
    """
    Attach upload sets to the app and initialise uploads.
    """
    for set in UPLOAD_SETS:
        configure_uploads(app, UPLOAD_SETS[set])
    # Allow uploads up to 20MiB
    patch_request_class(app, size=(20 * 1024 * 1024))
