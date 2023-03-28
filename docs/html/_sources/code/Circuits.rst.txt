#########
Circuits
#########

Circuits in TORC are divided into two subclasses: Plasmid and Genome. This is dictated but the shape of the DNA. In
Plasmids the DNA is circular with the first and last supercoiling regions connected (but not propagated) by an origin of
replication. The Genome is a linear segment of DNA, currently this operates with a first and last supercoiling regions
which are not effected by the DNA outside the segment being modelled.

Circuit
--------

.. autoclass:: TORC.Circuit
    :members:

Examples
---------

The *leu-500 promoter* "supercoiling sensor'' circuit can be implemented as:

.. code-block::
    :caption: *leu-500 promoter* "supercoiling sensor" circuit without lac in environment

    leu_500_no_lac = Circuit([("tetA"), ("CF", "red"), ("bridge", "lac"), ("CF", "blue"), ("bridge", "lac")],
                          environments=[("lac", 0)])

.. code-block::
    :caption: *leu-500 promoter* "supercoiling sensor" circuit with lac in environment

    leu_500_with_lac = Circuit([("tetA"), ("CF", "red"), ("bridge", "lac"), ("CF", "blue"), ("bridge", "lac")],
                          environments=[("lac", 20)])

Plasmid
---------

.. autoclass:: TORC.Plasmid
    :members:

Genome
------

.. autoclass:: TORC.Genome
    :members:
