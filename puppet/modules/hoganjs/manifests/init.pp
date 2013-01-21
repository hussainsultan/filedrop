class hoganjs {
  exec { 'hoganjs-install':
    command => '/usr/bin/npm install hogan.js --global',
    creates => '/usr/local/bin/hulk',
    require => Package[npm],
  }
}
