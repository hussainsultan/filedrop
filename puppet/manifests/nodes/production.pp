#
# Standalone manifest - for dev Vagrant box.
#
node filedrop inherits default {

  # Nginx
  #nginx::vhost { 'gunicorn':
  #  ensure => present,
  #  app    => '127.0.0.1:8000',
  #  auth   => false,
  #}

  upstart::job { 'gunicorn':
    ensure   => present,
    env  => [['FLASK_CONFIG' => 'config/production.py']],
    # Gunicorn service in Vagrant can't start on init becuase /vagrant isn't
    # get mounted until boot is finished. Puppet will start it instead.
    startup  => true,
  }
}
