class python {
  include python::modules
  package { ['python2.7', 'python-pip']:
    ensure => installed,
  }
}

#
# Python base system modules
#
class python::modules {
  package { [ 'python-virtualenv', 'python-dev', ]:
    ensure => 'installed'
  }
}
