============
 Oncilla-sim
============

Oncilla-sim is a collection of tools to help user to install Oncilla simulator.

How to develop on the app
=========================

Please use pip and virtualenv ::
    
    mkvirtualenv oncilla-sim --no-site-packages 
    workon oncilla-sim
    pip install -r requirements.txt

It will install lot of tools for TDD and BDD

Make good use of sniffer : just launch it and it will run the tests
when needed.

also use lettuce ::

    cd test && lettuce


