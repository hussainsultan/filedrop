from flask import current_app, request, abort
from functools import wraps
from ipaddress import ip_address as ip_address_orig
from ipaddress import ip_network as ip_network_orig


def ip_address(address):
    """Wrap ip_network method from ipaddress module to automatically
    force utf8 string (it's required as this library is backported from
    Python 3).
    """
    return ip_address_orig(address.decode('utf8'))


def ip_network(address, strict=True):
    """Wrap ip_network method from ipaddress module to automatically
    force utf8 string (it's required as this library is backported from
    Python 3).
    """
    return ip_network_orig(address.decode('utf8'), strict)


def is_authenticated(request):
    """Returns whether or not the specified IP address is allowed to
    upload files.
    """
    # Defer to custom auth function if one exists
    if current_app.config['UPLOADS_CUSTOM_AUTH'] is not None:
        authed = current_app.config['UPLOADS_CUSTOM_AUTH'](request)
        if authed is not None:
            return authed

    # Check for authentication by IP
    if current_app.config['UPLOADS_ALLOW_NETS'] is not None:
        remote_addr = ip_address(request.remote_addr)
        for allowed_net in current_app.config['UPLOADS_ALLOW_NETS']:
            if remote_addr in ip_network(allowed_net):
                return True

    return False


def private(func):
    """
    Decorator that is responsible for authenticating users based on IP
    address.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if is_authenticated(request):
            return func(*args, **kwargs)
        else:
            abort(403)
    return decorated_view
