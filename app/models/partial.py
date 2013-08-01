from glob import glob
from os import unlink, rmdir
from os.path import isfile, getsize, join
from werkzeug.utils import secure_filename

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class PartialUpload(object):
    """
    """

    chunk_suffix = "_part_"

    def __init__(self, storage, kwargs, folder=None):
        """
        Expected kwargs are:

        resumableChunkNumber:
        resumableFilename:
        resumableTotalSize:
        """
        self.storage = storage
        self.kwargs = kwargs

        self.folder = folder
        if self.folder is None:
            self.folder = ''

        # Read arguments
        self.chunk_id = self.kwargs.get('resumableChunkNumber').zfill(4)
        self.filename = secure_filename(self.kwargs.get('resumableFilename'))
        self.target_size = int(self.kwargs.get('resumableTotalSize'))

    @property
    def chunks(self):
        """Return list of all stored chunks."""
        return glob(self._chunk_filepath('*'))

    @property
    def chunk_filename(self):
        """Return filename for this chunk. Chunk identifier can be
        overridden but defaults to the current chunk.

        Eg.: foo.mp3_345634_part_0003
        """
        return self._chunk_filename(self.chunk_id)

    @property
    def chunk_filepath(self):
        """Full path to this chunk."""
        return self._chunk_filepath(self.chunk_id)

    @property
    def file(self):
        """Return file handle for the complete file."""
        if not self.is_complete:
            raise Exception('Chunk(s) still missing')
        data = StringIO()
        for chunk in self.chunks:
            data.write(open(chunk).read())
        data.seek(0)
        return data

    def _chunk_filename(self, chunk_id):
        """Return filename for chunk with the specified chunk_id.

        Eg.: foo.mp3_345634_part_ID
        """
        return '%s%s%s%s' % (
            self.filename,
            self.kwargs.get('resumableTotalSize'),
            self.chunk_suffix,
            chunk_id
        )

    def _chunk_filepath(self, chunk_id):
        """Full path chunk with the specified id."""
        return self.storage.path(join(self.folder, self._chunk_filename(chunk_id)))

    def is_complete(self):
        """Checks if all chunks have been uploaded."""
        return int(self.kwargs.get('resumableTotalSize')) == self.chunks_size()

    #def save(self, fdst):
    #    """Combine all chunks into one file."""
    #    if self.exists():
    #        raise Exception('File already exists')
    #    if not self.is_complete():
    #        raise Exception('Missing chunks')
    #
    #    for chunk in self.chunks:
    #        with open(chunk, 'rb') as c:
    #            copyfileobj(c, fdst)

    def chunk_exists(self):
        """Checks if the requested chunk or complete file exists."""
        return isfile(self.chunk_filepath)

    def chunks_size(self):
        """Gets current size of all uploaded chunks."""
        size = 0
        for chunk in self.chunks:
            size += getsize(chunk)
        return size

    def delete_chunks(self):
        """Delete all chunks."""
        [unlink(chunk) for chunk in self.chunks]
        try:
            rmdir(self._chunk_filepath(''))
        except OSError:
            pass

    def process_chunk(self, file):
        """Save data at this chunk location."""
        if not self.chunk_exists():
            self.storage.save(file, folder=self.folder,
                              name=self.chunk_filename)
