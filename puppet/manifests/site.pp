import 'lib/*.pp'
import 'nodes/*.pp'

#
# Modules included for all nodes.
#
node default {

  include cssmin
  include fabric
  include git
  include hoganjs
  include less
  include nginx
  include nodejs
  include postfix
  include postgresql
  include puppet::sudoers
  include python
  include pil
  include sass
  include sudo
  include uglifyjs
  include users

  # Create postgresql user for the app
  postgresql::role { 'www-data':
    ensure => present,
  }
  postgresql::role { 'tobias':
    ensure     => present,
    createdb   => true,        # This user creates the
    grant      => 'www-data',  # app database.
  }
}

#
# Base class for externally hosted production nodes.
#
node site inherits default {

  # Firewall
  class { 'ferm':
    public_ports => [
      'http',
      'https',
    ],
  }

  # Newrelic server monitoring
  class { 'newrelic::servermon':
    key => '3c11e611ab565cd0936ed88137ba555ca1500dc0'
  }
}
