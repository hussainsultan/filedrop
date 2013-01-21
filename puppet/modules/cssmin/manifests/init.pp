class cssmin {
  package {'cssmin':
    ensure   => installed,
    provider => pip,
    require  => Package[python-pip],
  }
}
