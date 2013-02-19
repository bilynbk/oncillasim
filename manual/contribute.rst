.. _contribute:

=========================
 Contribute to |project| 
=========================

Becasue you want to fix some issue, or you want to implement some
missing interface, you may want to contribute to the simulator. It
used to be very cumbersome in the past, but now it is much more
simple.


Requirements
============

Oncly a few requirements are needed :

* liboncilla-webots-dev package. It will install all requirements to compile liboncilla-webots
* git


Getting and building the sources
================================

.. code-block:: sh

   git clone https://redmine.amarsi-project.eu/git/liboncilla-webots.git
   cd liboncilla-webots
   mkdir -p build
   cd build
   cmake ..
   make


Tips : always build the sources from an out-of-source tree, like
presented above. Like this, if you want to remove all generated file,
just delete the build directory.

Using a development version of liboncilla-webots
================================================

Now you have a HEAD version of liboncilla-webots. liboncilla (the
generic interface to the Oncilla robot) is merly an interface rthat
does not implement anything. At startup it will look for an available
backend installed on the system, and load it to actually drive a
robot.

liboncilla-webots is one of such backend (like liboncilla-hw is the
backend for the real robot). By default liboncilla loads a backend
which is installed on the system (which is the cas if you have
liboncilla-webots-dev installed). When running your simulation, you
will have to ask liboncilla to use your backend instead. This could be
done simply by setting the LIBONCILLA_FORCE_BACKEND environment
variable to the path to your version of liboncilla-webots. This should
be done prior to start webots.

.. code-block:: sh

   export LIBONCILLA_FORCE_BACKEND=${path_to_build}/src/liboncilla-webots/liboncilla-webots.so
   webots ${path_to_your_world_file}

How to actually contribute to the project
=========================================

So now you are able to load your own version of liboncilla-webots, and do whatever you want. To contribute to the project, please :

* Check first if your issue is not already reported, and if someone is not already assigned to it : https://redmine.amarsi-project.eu/projects/oncillasim/issues
    * if the issue is still not reported, please create a new one
* before starting to do anything with the code, please create a new branch for this issue with its Id.

.. code-block:: sh

    git checkout -b issue-ID

* Edit some files
* commit changes to your branche with git-commit
* test your changes
* repeat steps above as much as needed
* once you have finished, push the changes to the specific branche

.. code-block:: sh

    git push origin issue-ID

* Send an email, asking for integration of your branch for the next release


