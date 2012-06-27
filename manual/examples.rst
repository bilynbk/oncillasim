.. _examples:

==========
 Examples
==========

When setting up a new project with the :ref:`Project Wizard <wizard>` it will
come with a set of example to learn the usage of the simulation environment.

All following examples will execute a simple sine movement by moving the
:ref:`L1 and L2 joints <liboncilla:l1l2>` of the robot. You can sart the
examples by opening the world files *worlds/Example...* in your project created
by the :ref:`Project Wizard <wizard>`. (*Start Webots* -> *Open World*)

The examples should be properly set up and compiled by the Project Wizard, and
should all perform the same movement.

<Description of the API Layers>

Example 1: Simple Sine Movement
===============================


You should see the robot performing a simple walking movement, which is not a
necessarily meaningful walking gate. *;)*

For more information on the example and how to change and extend it, see
:ref:`liboncilla: Simple Sine Movement <liboncilla:example>`.

Example 2: Simple Sine Movement Component
=========================================

The second example will do exactly the same as Example 1, but is written as a
:ref:`CCA <cca>` component and therefore ready for usage in the AMARSi Software
Architecture.

...

For more information on the example and how to change and extend it, see
:ref:`cca-oncilla: Simple Sine Movement Component <ccaoncilla:simpleexample>`.

Example 3: External Components / Streaming 
==========================================

The third example will do exactly the same as Example 1 and 2, but is written as
an external Python Script, that communicates with the Simulator over the
middleware :ref:`RSB <rsb>` (Robotics Service Bus).

...

For more information on the example and how to change and extend it, see
:ref:`cca-oncilla: Python Simple Sine Movement <ccaoncilla:pythonexample>`.

Example 4: Recording and Replaying Movements 
============================================

The fourth example will replay a previously recorded movement over the
middleware :ref:`RSB <rsb>` (Robotics Service Bus) by using :ref:`RSBag Tools
<rsbag>`.

...

For more information on the example and how to change and extend it, see
:ref:`cca-oncilla: Replaying Simple Sine Movement <ccaoncilla:rsbagexample>`.
