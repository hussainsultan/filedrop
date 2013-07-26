import shutil
from glob import iglob
from os import link
from os.path import exists, isfile, join, dirname
from hashlib import sha1
from atomicfile import AtomicFile

from ..helpers import read, mkdir_p


class Repository(object):
    """
    File repository that stores files uniquely by sha1 hash.
    """
    def __init__(self, storage):
        self.storage = storage

    def _exists(self, fhash):
        """Check if file exists (by hash)"""
        # Check file (dir) exists
        return exists(self.storage.path('fhash'))

    def _link(self, fhash, filename):
        """Create a hard link for the specified file/hash and filename
        """
        # Be safe, verify that the file we're linking matches the hash
        for link_src in iglob(self.storage.path('*', folder=fhash)):
            if isfile(link_src):
                # Verify file integrity
                if self.hash(link_src) == fhash:
                    # Link this file
                    target = self.storage.path(filename, folder=fhash)
                    link(link_src, target)
                    return target

        # Could not verify the integrity of the existing files, so we
        # did not link
        return None

    @classmethod
    def hash(cls, fsrc):
        """Calculate hash of specified file"""
        h = sha1()
        for chunk in read(fsrc, chunk_size=134217728):
            h.update(chunk)
        return h.hexdigest()

    def save(self, filename, fsrc):
        """Save the specified file into the respository."""
        # Get hash
        fhash = self.hash(fsrc)

        # See if the file exists and just link it if possible (dedupe)
        if self._exists(fhash):
            link = self._link(fhash, filename)
            if link is not None:
                return link

        # Create the file
        target = self.storage.path(join(fhash, filename))
        mkdir_p(dirname(target))
        with AtomicFile(target, 'wb') as fdst:
            fsrc.seek(0)
            shutil.copyfileobj(fsrc, fdst)

        return target
