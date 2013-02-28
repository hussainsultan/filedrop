"""
fabfile bundle config.
"""
import sys
from fabric.api import env
from fabfile.git import branch

env.branch = branch()
env.remote_path = '/srv/www/app'

# Check to see if -u was specified at the command line
for opt in sys.argv:
    if opt.startswith('-u') or opt.startswith('--user'):
        # Set a flag to signifiy -u was specified
        env.custom_user = True
        break

# Use -u parameter if it was specified, otherwise default to deploy user
if not env.get('custom_user', False):
    env.user = 'tobias'
