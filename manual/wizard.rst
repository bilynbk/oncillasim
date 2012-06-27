.. _wizard:

==========================
 |project| Project Wizard
==========================

The |project| project wizard will help you set up the proper projects structure
for the `Webots`_ Simulation and will also add and compile running
:ref:`examples` to the project.

The wizard will help you **creating** new projects and **updating** existing
projects to get more recent versions of the examples. For that it will 
check out the latest sources into a template folder, and then create or update
projects from that.

Usage
=====

To learn about the basic usage and command line arguments, type:

.. code-block:: sh

   ./oncilla-sim-wizard -h

Create Project
--------------

Create a project will set up a working environment for the `Webots`_ Simulator
and add running :ref:`examples` for execution. Choose an empty path for setting
up a new project by:

.. code-block:: sh

   ./oncilla-sim-wizard create /your/new/project/path

After that, you find a number of world files in the folder *worlds/*,
corresponding controllers in the folder *controllers/* and some infrastructure.
Start with the examples as described :ref:`here <examples>`.

.. _`Webots`:
    http://www.cyberbotics.com/overview

Update Project
--------------

In case you already have an existing project and want to update it, either
because there is a newer version or because you project isn`t working any more,
the Wizard will help you with that, too.
**Note:** The update will *not* destroy or change any of the project files
without asking.

.. code-block:: sh

   ./oncilla-sim-wizard update /your/existing/project/path

.. _`Webots`:
    http://www.cyberbotics.com/overview
