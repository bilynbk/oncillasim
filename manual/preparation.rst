.. _preparation:

==============
 Installation
==============

Installing |project|
====================

There are currently two ways to install the |version| version of
|project|:

* |ubuntu| packages
* From source (undocumented yet, but uses python setup.py standard packaging)

|ubuntu| Packages
-----------------

.. warning:: Package are curently only released for **Ubuntu Precise LTS 12.04**.

Debian packages for |ubuntu| are available from the `CoR-Lab package
repository <http://packages.cor-lab.de/>`_  and the `Biorob
repository <http://biorob2.epfl.ch/users/tuleu/ubuntu>`_.

In order to install these repositories in your system, please proceed
like this::

  eval `cat /etc/lsb-release` && echo deb http://biorob2.epfl.ch/users/tuleu/ubuntu precise main testing | sudo tee /etc/apt/sources.list.d/biorob-tuleu.list
  eval `cat /etc/lsb-release` && echo deb http://packages.cor-lab.de/ubuntu precise main testing | sudo tee /etc/apt/sources.list.d/cor-lab.list
  wget -O - http://biorob2.epfl.ch/users/tuleu/ubuntu/gpg.key | sudo apt-key add -
  wget -O - https://webdav.cor-lab.de/server_keys/packages.cor-lab.de_server_key.txt | sudo apt-key add -
  

The Simulator is based on the `Webots <http://www.cyberbotics.com/overview>`_
Simulator by Cyberbotics and requires a ``Webots PRO`` License. If you don't
have an appropriate license, you can also
`register at Cyberbotics <http://www.cyberbotics.com/my_account/register>`_ to
obtain free 30 day trial version of the ``Webots PRO`` License.

.. note::

   Currently |project| is compatible with Webots versions lower than 7.0. You
   can download older Webots 6.x versions (e.g. 6.4.4, scroll down for debian
   packages) `here <http://www.cyberbotics.com/archive/linux/>`_.

Then you can install the Simulator::

  sudo aptitude update
  sudo aptitude install oncilla-sim-0.2

Now you are ready to use :ref:`Project Wizard <wizard>` utility to
launch the simulator.

