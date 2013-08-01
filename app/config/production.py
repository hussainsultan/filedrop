import socket

DEFAULT_MAIL_SENDER = 'www-data@%s' % socket.getfqdn()

ADMIN_RECIPIENTS = ['devs@tobias.tv']
ERROR_EMAIL = 'devs@tobias.tv'

UPLOADS_ALLOW_NETS = ['192.168.2.0/24']
