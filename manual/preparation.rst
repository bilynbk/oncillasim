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

Debian packages for |ubuntu| are available from the `CoR-Lab package
repository <http://packages.cor-lab.de/>`_ , `Biorob
repository <http://biorob2.epfl.ch/users/tuleu/ubuntu>`_ and
`Cyberbotics repositiory <http://www.cyberbotics.com/debian>`_.

In order to install these repositories in your system, please proceed
like this::

  eval `cat /etc/lsb-release` && echo deb http://biorob2.epfl.ch/users/tuleu/ubuntu $DISTRIB_CODENAME main | sudo tee /etc/apt/sources.list.d/biorob-tuleu.list
  eval `cat /etc/lsb-release` && echo deb http://packages.cor-lab.de/ubuntu $DISTRIB_CODENAME main         | sudo tee /etc/apt/sources.list.d/cor-lab.list
  echo deb http://www.cyberbotics.com/debian/ binary-i386/   | sudo tee     /etc/apt/sources.list.d/cyberbotics.list
  echo deb http://www.cyberbotics.com/debian/ binary-amd64/  | sudo tee -a  /etc/apt/sources.list.d/cyberbotics.list
  wget -O - http://biorob2.epfl.ch/users/tuleu/ubuntu/gpg.key | sudo apt-key add -
  wget -O - https://webdav.cor-lab.de/server_keys/packages.cor-lab.de_server_key.txt | sudo apt-key add -
  wget -O - http://www.cyberbotics.com/Cyberbotics.asc | sudo apt-key add -

Then install :doc:`NemoMath <nemomath>`.

Then you can install the packages needed for the simulator::

  sudo aptitude update
  sudo aptitude install oncilla-sim liboncilla-dev liboncilla-webots-dev webots

Now you are ready to use :ref:`oncilla-sim-wizard <wizard>` utility to
launch the simulator.
