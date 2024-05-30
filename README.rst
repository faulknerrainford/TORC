RandomBooleanCircuits
=================================================

This package was built to explore plasmid circuits for synthetic biology. Using and abstract model of supercoiling and
gene regulation. It implements the systems found in:
1. Rainford, P. F., Mogre, A., Velasco-Berrelleza, V., Dorman, C. J., Harris, S., Kr ̈oger, C., and Stepney, S. (2023).
A π-calculus model of supercoiling DNA circuits. In ALIFE 2023: Ghost in the Machine: Proceedings of the 2023
Artificial Life Conference. direct.mit.edu.
2. Rainford, P. F., Velasco-Berrelleza, Mogre, A., V., Dorman, C. J., Harris, S., Kr ̈oger, C., and Stepney, S. (2024).
Parameterising a Computational model of Supercoiling in Plasmid DNA with Biophysics modelling. In ALIFE 2024 Copenhagen
Proceedings of the 2024 Artificial Life Conference. direct.mit.edu.

#########
Set Up
#########

We provide details of the requirements for the package and how to find and download or install TORC.

Requirements
============

If installing the TORC dependencies will be installed automatically. Otherwise you will need:

- python 3.9-3.12
- Sphinx 5.3.0+
- numpy 1.23.4+
- matplotlib 3.6.0+
- setuptools 60.9.3+
- webcolors 1.12+
- scipy 1.10.1+
- pandas 2.2.0+
- seaborn 0.13.2+
- sklearn 1.4.1+

Installation
============

The code for TORC-ALife2024 can be found in the TORC GitHub repository:
https://github.com/faulknerrainford/TORC/tree/TORC-ALife-2024

Replication
===========

The random searches used in the Rainford. et al 2024 are implemented in TORC/TORC/source/Parameterisation.
The RandomSearch.py file will run any of the random searches used in the paper but the limits for parameters or the
values for fixed parameters need to be edited before running. All values used in paper are available but will need to
be commented in or out for the appropriate run.

Comparison data from the physics model is provided compressed along with output from the random search in
TORC/Experiment_Data/Paper Data. In Experiment_Data we also provide the png files for all figures.

Analysis of the data and comparison with TORCPhysics data is done using
TORC/TORC/source/Parameterisation/RandomSearchAnalysis.py where the full analysis pipline is laid out in main.


