class uglifyjs {
  exec { 'uglifyjs-install':
    command => '/usr/bin/npm install uglify-js -g',
    creates => '/usr/bin/uglifyjs',
    require => Package[npm],
  }
}
