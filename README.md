Filedrop
========

Filedrop is a web-based file sharing service. Users upload files and then
receive a unique, private URL to share the file with other users.

Home:

![Screenshot of home page](https://raw.github.com/tobiasandtobias/filedrop/master/docs/source/_static/screenshots/Screen Shot 2013-08-06 at 09.11.25.png)

After uploading:

![Screenshot after file uploaded](https://raw.github.com/tobiasandtobias/filedrop/master/docs/source/_static/screenshots/Screen Shot 2013-08-06 at 09.11.37.png)


Features
--------

* Bootstrap 3
* Uses [Resumable.js](https://github.com/23/resumable.js), for HTML5 uploading in chunks
* Filesystem-only storage (no database required)
* File de-duplication
* Features fit for an intranet:
    * Configurable auth
    * Invite URLs; allow external users to upload files on a per-invite basis


Getting started
---------------

1. Check out this repository:

        git clone https://github.com/tobiasandtobias/filedrop.git

2. Run the development environment (requires [Vagrant](http://vagrantup.com/)):

        cd filedrop
        vagrant up

3. Point your web browser at:

        http://localhost:8080/


Contributing
------------

Feedback, bug reports and pull requests welcome.
