class puppet::sudoers {
  file { '/etc/sudoers.d/puppet':
      owner   => root,
      group   => root,
      mode    => 440,
      content => "tobias ALL = (root) NOPASSWD : /usr/bin/puppet apply --modulepath='/srv/www/app/puppet/modules' '/srv/www/app/puppet/manifests/site.pp'\n",
    }
}
