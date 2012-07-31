.. _dev:

=================
 Experimentation
=================

Writing own experiments 
=======================

Writing own experiments can easily be done by adapting one of the
:ref:`examples` installed by the :ref:`wizard`. To decide which of the examples
to adapt, consider:

* :ref:`Example 1 <liboncilla:example>`
  uses the lowest API Level 1 for fast access, but want produce
  reusable components for the AMARSi Software Architecture. Use this API Level
  for isolated experiments.
* :ref:`Example 2 <ccaoncilla:ccaexample>`
  provides access with the same speed, but already provides a
  :ref:`CCA <cca>` component, therefore reusable in the  the AMARSi Software
  Architecture. This is the recommended way to develop AMARSi Components.
* :ref:`Example 3 <ccaoncilla:pythonexample>`
  provides access over a remote interface (eg. local network) and also provides
  a :ref:`CCA <cca>` component, therefore reusable in the the AMARSi Software
  Architecture. This is the recommended way to either develop computationally
  expensive C++ components that have to run on a second machine and communicate
  over network. Or to develop components / applciations in Python, Java or
  Common Lisp, that can either run locally or remotely over the network.
