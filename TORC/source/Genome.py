from TORC import Circuit


class Genome(Circuit):
    """
    Implements the linear circuits of genomes.

    Parameters
    ----------
    components      :   List<Tuple<String, String>>
        List of components to build onto the plasmid, in type,name tuples.
    environments    :   List<Tuple<String, float>>
        List of initial environment conditions for non-empty starting environments in name, content tuples.
    label           :   String
        Name of the circuit
    local           :   LocalArea
        Local area can be provided to the system with a full start state if needed.
    """
    def __init__(self, components, environments=None, label="circuit1", local=None):
        super(Genome, self).__init__(components, environments, label, local)

    def setup(self):
        """
        Sets up the circuit by building the environments, components and supercoiling regions of the circuit.
        """
        super(Genome, self).setup()
        