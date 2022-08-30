###############################
Package setup and maintanence
###############################

Requirements
============

These need listing in the requirements file and the setup.py file.

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

