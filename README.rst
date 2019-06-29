====
mozio
====

Mozio provider API built as a django app.

View a running instance at http://dev.mozio.com

Note that django-mozio is under development and not yet feature complete.

The latest source code is available at https://gitlab.com/mozio/django-mozio.

* **Developers:** See our [developer guide](django-mozio/blob/develop/README-dev.md)
* **For production:** See our [deployment guide](django-mozio/blob/develop/README-docker.md)


Key features
------------

* To be added


Quick Installation Guide
------------------------
For deployment we use `docker`_ so you need to have docker
running on the host. django-mozio is a django app so it will help if you have
some knowledge of running a django site.

     git clone https://gitlab.com/mozio/django-mozio.git

     cd django-mozio/deployment/

     make build

     # Just to make sure containers are built, not NEEDED to be run

     make deploy

     make permissions

     # Wait a few seconds for the DB to start before to do the next command

     make web

     # Just to make sure web server is spinned up, not NEEDED to be run

     make run

     make migrate

     make collectstatic

     # Finally we can rebuild our search indexes if needed,

     # Note: Not needed for now.

     make rebuildindex

So as to create your admin account:

 ```
  make superuser
 ```

github authentication
---------------------

Create a developer key here:

https://gitlab.com/settings/applications/new

Set the callback and site homepage url to the top of your site e.g.

http://localhost:61202

At http://localhost:61202/en/site-admin/socialaccount/socialapp/add/

Set the key and secret from the github key page.

Backups
-------

If you wish to sync backups, you need to establish a read / write btsync
key on your production server and run one or more btsync clients
with a read only key.

    ```
    cd deployment
    cp btsync-media.env.EXAMPLE btsync-media.env
    cp btsync-db.env.EXAMPLE btsync-db.env
    ```

Now edit the ``btsync-media.env`` and ``btsync-db.env`` files, including
relevant SECRET and DEVICE settings.

Credits
-------

mozio is a owned and being developed by [mozio.com](http://mozio.com).


Thank you
---------

Thank you to the individual contributors who have helped to build *django-mozio*:

* Alison Mukoma: mukomalison@gmail.com | <sonlinux>
* Bakyt Niyazov
* Dmitry Belaventsev
* Frederico Boaventura
