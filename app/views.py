from flask import Blueprint, render_template, request, send_file, abort, \
    redirect
from os.path import abspath, basename

from .auth import private
from .models.slugs import UploadSlug


blueprint = Blueprint('main', __name__, template_folder='templates',
                      static_folder='static')


@blueprint.route('/')
@private
def upload():
    return render_template('upload.html')


@blueprint.route('/invite/')
@private
def invite():
    return render_template('invite.html')


@blueprint.route('/invite/<string:slug_id>')
def invite_upload(slug_id=None):
    slug = None

    # Check for a valid and existing upload invite
    if slug_id is not None:
        slug = UploadSlug(slug_id)
        if (not slug.exists()) or (slug.has_file()):
            return abort(404)

    return render_template('upload.html')


@blueprint.route('/file/<string:slug_id>')
def file(slug_id):
    slug = UploadSlug(slug_id)
    if not slug.has_file():
        abort(404)
    return redirect(request.base_url + '/' + basename(slug.file)), 302


@blueprint.route('/file/<string:slug_id>/<string:filename>')
def file_inline(slug_id, filename):
    slug = UploadSlug(slug_id)
    if not slug.has_file():
        abort(404)

    filepath = abspath(slug.file)
    filename = basename(filepath)

    return send_file(filepath, attachment_filename=filename)
