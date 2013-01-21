class ferm ( $template = 'default', $public_ports = '' ) {

  package { 'ferm':
    ensure => 'installed',
  }

  file { "/etc/ferm/ferm.conf":
    content => template("ferm/ferm.conf.${template}.erb"),
    require => Package[ferm]
  }

  exec { "ferm-reload":
    command     => '/etc/init.d/ferm reload',
    require     => Package["ferm"],
    subscribe   => File["/etc/ferm/ferm.conf"],
    refreshonly => true
  }
}
