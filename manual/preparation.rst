.. _preparation:

=============
 Preparation
=============

Installing |project|
====================

There are currently two ways to install the |version| version of
|project|:

* |ubuntu| packages
* From source

|ubuntu| Packages
-----------------

Debian packages for several versions of |ubuntu| are available from
the `CoR-Lab package repository
<http://packages.cor-lab.de/ubuntu/dists/>`_. The following repository
source line has to be added to ``/etc/apt/sources.list``::

  deb http://ponyo

where :samp:`RELEASENAME` is the appropriate Ubuntu release name. Now install
the package::

   oncilla-sim

.. note::

   More information can be found `here
   <https://support.cor-lab.org/projects/ciserver/wiki/RepositoryUsage>`_.

From Source
-----------

Installation from source requires `cmake`_ and `rsb`_.

#. The whole source tree of |project| can be obtained via::
   
     https://redmine.amarsi-project.eu/git/oncillasim.git

   .. note::

      In the following commands, :samp:`{prefix}` specifies the target
      directory of the installation.

#. Build and install |project| Library

   .. code-block:: sh

	  mkdir -p build
      cd build
      cmake -DCMAKE_INSTALL_PREFIX=$prefix ..
      make
      make install

.. _`ubuntu manual`:
	http://wiki.ubuntuusers.de/sources.list
