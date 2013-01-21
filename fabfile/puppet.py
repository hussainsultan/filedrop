"""
fabfile module containing Puppet-related tasks.
"""
from fabric.decorators import task
from fabric.colors import cyan
from fabfile.utils import do


def check():
    """Syntax check on Puppet config."""
    print(cyan('\nChecking puppet syntax...'))
    do('find puppet -type f -name \'*.pp\' |xargs puppet parser validate')


@task
def run():
    """Apply Puppet manifest."""
    check()
    print(cyan('\nApplying puppet manifest...'))
    do('sudo /usr/bin/puppet apply --modulepath="/srv/www/app/puppet/modules" "/srv/www/app/puppet/manifests/site.pp"')
