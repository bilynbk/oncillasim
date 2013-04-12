.. _help:

=================
 Troubleshooting
=================

Support
=======

If problem occur, please check if the issue is known and solved below. Otherwise
you can get help on teh AMARSi Oncilla Mailinglist:
https://lists.techfak.uni-bielefeld.de/cor-lab/mailman/listinfo/amarsi-oncilla

If you are sure that you ran into a bug, please consider filing a bug report at:
https://redmine.amarsi-project.eu/projects/oncillasim/issues

Known issues
============

make: *** No rule to make target
--------------------------------

During compilation of an example or your own Webots controller you see the
following error:: 

  Makefile:7: /resources/projects/default/controllers/Makefile.include: No such file or directory
  make: *** No rule to make target `/resources/projects/default/controllers/Makefile.include'.  Stop.

**Solution:** You need to set the
:ref:`environment variable <http://en.wikipedia.org/wiki/Environment_variable>`
``WEBOTS_HOME`` so that your system can find Webots' ``Makefile.include``.
``WEBOTS_HOME`` needs to be set to the root folder of your Webots installation,
usually this is ``/usr/local/webots``. In this case type::

  export WEBOTS_HOME=/usr/local/webots

and try again.

No backend for liboncilla were found
------------------------------------

Make sure that you have a Webots version below 7.0 installed, for example the
latest stable 6.x version (e.g. 6.4.4). Compatibility with Webots >= 7.0 might
be added in upcoming releases of |project|.

Reset of the simulation doesn`t work
------------------------------------

Make sure that you have a Webots version below 7.0 installed, for example the
latest stable 6.x version (e.g. 6.4.4). Compatibility with Webots >= 7.0 might
be added in upcoming releases of |project|.
