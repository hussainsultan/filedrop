class vagrant::postgresql {
  # Create vagrant postgresql user for dev
  postgresql::role { 'vagrant':
    ensure     => present,
    createdb   => true,
    createrole => true,
    superuser  => true,
  }
}
