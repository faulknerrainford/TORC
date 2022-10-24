###############################
Package setup and maintenance
###############################

Requirements
============

These need listing in the requirements file and the setup.py file.

To install requirements:

pip install -r requirements.txt


Version
==========

Needs updating in the setup.py and the top level __init__.py

Updating Package Local
========================
Run pip install . in top package to check install is clean.

Run python setup.py check to make sure the package is correct for distribution.

Run python setup.py sdist to create the source distribution.

Run python setup.py bdist_wheel --universal

Distributing
==============

See instructions on testing on testpypi and further distributing.

Testing
========

Info on the creation and use of tests:

https://www.jetbrains.com/help/pycharm/testing.html

https://realpython.com/python-testing/

Before first release
=======================

Set up PyPI and testPyPI accounts
Set up tox to run tests on multiple python versions and update version statement in setup.
(Don't add Tox to git)