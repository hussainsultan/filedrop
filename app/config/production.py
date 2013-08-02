import socket

DEFAULT_MAIL_SENDER = 'www-data@%s' % socket.getfqdn()

ADMIN_RECIPIENTS = ['devs@tobias.tv']
ERROR_EMAIL = 'devs@tobias.tv'

UPLOADS_ALLOW_NETS = ['192.168.2.0/24']


def auth(request):
    """Custom authenticator."""
    # External forwarder
    if request.remote_addr == '192.168.2.12':
        return False
    else:
        return True

UPLOADS_CUSTOM_AUTH = auth
