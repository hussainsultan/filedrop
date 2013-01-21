class newrelic( $key = '' ) {
  class { 'newrelic::servermon':
    key => $key
  }
}