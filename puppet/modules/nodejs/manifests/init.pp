class nodejs {
  package { ["nodejs", "npm"]:
    ensure => installed,
  }

  # other packages we need, e.g. g++ to compile node-expat
  package { ["g++", "libexpat1-dev"]:
    ensure => installed,
  }
}
