from flask import Blueprint, render_template, request, Response
from os import rename, unlink
from glob import glob
from shutil import copyfileobj
from os.path import basename, dirname, realpath, isfile
from werkzeug import secure_filename
from tempfile import NamedTemporaryFile

from app.uploads import partial, files, tmp


main = Blueprint(basename(dirname(realpath(__file__))), __name__,
                 template_folder='templates',
                 static_folder='static')


def getarg(request, arg):
    val = request.args.get(arg)
    if val is None:
        val = request.form.get(arg)
        if val is None:
            return None
    return val


@main.route('/')
def index():
    return render_template('welcome.jinja')


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    """Accept and save file"""

    data = {
        'chunk_number': int(getarg(request, 'resumableChunkNumber')),
        'chunk_size': int(getarg(request, 'resumableChunkSize')),
        'total_size': int(getarg(request, 'resumableTotalSize')),
        'identifier': getarg(request, 'resumableIdentifier'),
        'filename': getarg(request, 'resumableFilename'),
    }

    chunk_filename = secure_filename('%(identifier)s.%(chunk_number)s.part' % data)

    # If this is a GET request, Resumable.js is asking us whether this
    # chunk has already been uploaded or not.
    if request.method == 'GET':

        # If the chunk exists, we indicate a positive response with HTTP
        # 200. If it doesn't we send an HTTP 404.
        if isfile(partial.path(chunk_filename)):
            return Response(status=200)
        else:
            return Response(status=404)

    # If this is a POST request, Resumable.js is uploading a chunk of
    # the file.
    if request.method == 'POST':

        file = request.files['file']

        # Write out file to temporary dir in the filesystem, then move
        # it into the 'partial' dir (to ensure operation is atomic).
        tmp.save(file, name=chunk_filename)
        rename(tmp.path(chunk_filename), partial.path(chunk_filename))

    # Check for all chunks completed and construct file
    uploaded_chunks = glob('%s.*' % partial.path(data['identifier']))
    uploaded_size = len(uploaded_chunks) * data['chunk_size']

    if uploaded_size >= data['total_size'] - data['chunk_size'] + 1:

        # Create new file in a temporary location
        tempfile = NamedTemporaryFile(delete=False, dir=tmp.path(''))

        # Concatenate all chunks into the new temp file
        for chunk in uploaded_chunks:
            copyfileobj(open(chunk, 'rb'), tempfile)
        tempfile.close()

        # Move the full file into place
        filename = secure_filename(data['filename'])
        rename(tempfile.name, files.path(filename))

        # Delete partial chunks
        for chunk in uploaded_chunks:
            unlink(chunk)

    return Response(status=200)
