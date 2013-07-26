from flask import current_app
from os import urandom, symlink, readlink, unlink
from os.path import join, exists, islink
from zbase62 import zbase62


class UploadSlug(object):
    """
    An upload slug represents a pointer to a file. A slug can be bound
    or unbound; a bound slug points to a file, whilst an unbound slug
    is a placeholder for a file that may be uploaded in the future.
    """
    def __init__(self, id=None, file=None, storage_dir=None):
        if storage_dir is not None:
            self.storage_dir = storage_dir.rstrip('/')
        else:
            self.storage_dir = current_app.config.get('APP_SLUG_STORAGE_DIR')

        self.id = id if id is not None else self._generate_unique_slug()

    @property
    def file(self):
        """Return path of the file bound to this slug. If this slug is
        unbound, returns None.
        """
        if not self.has_file():
            return None
        else:
            return readlink(self.path)

    @property
    def path(self):
        """Full path to this slug."""
        return join(self.storage_dir, self.id)

    def _generate_unique_slug(self):
        """Generate unique identifier for this slug."""
        unique_id = zbase62.b2a(urandom(24))
        while exists(join(self.storage_dir, unique_id)):
            unique_id = zbase62.b2a(urandom(24))
        return unique_id

    def exists(self):
        """Whether or not this slug exists yet."""
        return exists(self.path)

    def has_file(self):
        """Whether or not this slug is bound to a file."""
        return islink(self.path)

    def link(self, file, force=False):
        """Bind/link this slug to a file."""
        if (not force) and self.has_file():
            raise Exception('Slug already linked')

        if self.exists():
            unlink(self.path)
            symlink(file, self.path)

    def reserve(self):
        """Reserve this slug, ie. create it but in an unbound state."""
        open(self.path, 'a').close()
