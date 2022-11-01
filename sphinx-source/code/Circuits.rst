#########
Circuits
#########

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
