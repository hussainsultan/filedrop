import socket

# no debugging by default - this is overriden in runserver for local dev
DEBUG = False

# override with something sensible
SECRET_KEY = 'SecretKeyForSessionSigning'

# Email address that emails originate from. Make sure it's real, you own it,
# and SPF allows you to send from it.
DEFAULT_MAIL_SENDER = 'vagrant@%s' % socket.getfqdn()

# General email address for admins and errors
ADMIN_RECIPIENTS = ['vagrant@localhost']
ERROR_EMAIL = None

# Database connection string
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://@/app'

# Default/base uploads destination
UPLOADS_DEFAULT_DEST = 'app/data'

# Better file handling for downloads
USE_X_SENDFILE = True

# Storage dir for slug symlinks
APP_SLUG_STORAGE_DIR = 'app/data/slugs'

# Restrict access to file upload by IP address
UPLOADS_ALLOW_NETS = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '127.0.0.1']

# Custom auth function
UPLOADS_CUSTOM_AUTH = None
