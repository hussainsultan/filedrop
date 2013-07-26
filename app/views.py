from flask import Blueprint, render_template, request, Response, jsonify, \
    send_file, abort
from os.path import abspath, basename

from .models.slugs import UploadSlug
from .models.partial import PartialUpload
from .models.repository import Repository
from .uploads import UPLOAD_SETS


main = Blueprint('main', __name__, template_folder='templates',
                 static_folder='static')


@main.route('/')
def index():
    return render_template('welcome.jinja')


@main.route('/upload', methods=['GET'])
def upload_resume():
    """Called when resumable.js is checking for the presence of already-
    uploaded chunks.
    """
    r = PartialUpload(UPLOAD_SETS['partial'], request.args)
    if r.chunk_exists():
        return Response('chunk exists', status=200)
    else:
        return Response('chunk not found', status=404)


@main.route('/upload', methods=['POST'])
def upload_post():
    """Called when resumable.js sends a chunk for upload.
    """
    # In order to proceed, the user must be uploading to a valid slug
    slug_id = request.form.get('slug', None)
    if slug_id is None:
        return Response('no slug id provided', status=500)

    slug = UploadSlug(slug_id, None)
    if (not slug.exists()) or (slug.has_file()):
        return Response('upload slug invalid', status=403)

    # Create a partial upload check/set. Store these chunks in a folder unique
    # to this particular upload slug.
    r = PartialUpload(storage=UPLOAD_SETS['partial'], kwargs=request.form,
                      folder=slug.id)

    if r.chunk_exists():
        return Response('chunk exists', status=200)

    # Save chunk to partial upload storage
    chunk = request.files['file']
    r.process_chunk(chunk)

    # Check for a completed file
    if r.is_complete():

        # Save file to repository
        file_repo = Repository(UPLOAD_SETS['repository'])
        filepath = file_repo.save(r.filename, r.file)

        # Link slug to file
        slug.link(filepath)

        # DONE MATE!
        return Response('file is complete', status=200)

    return Response('chunk uploaded', status=200)


# TODO: Make sure this can only be accessed by trusted users
@main.route('/api/request-slug')
def request_slug():
    slug = UploadSlug()
    slug.reserve()
    return jsonify(response={'id': slug.id})


@main.route('/file/<string:slug_id>')
def file(slug_id):
    slug = UploadSlug(slug_id)
    if not slug.has_file():
        abort(404)

    filepath = abspath(slug.file)
    filename = basename(filepath)

    return send_file(filepath, as_attachment=True, attachment_filename=filename)
