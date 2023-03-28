from TORC import Circuit


class Plasmid(Circuit):
    """
    Implements the circular circuits on plasmids. Adds an origin of replication which connects first and last #
    supercoiling regions, does not transmit coiling between them.

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
        super(Plasmid, self).__init__(components, environments, label, local)

    def setup(self):
        """
        Sets up the circuit by building the environments, components and supercoiling regions of the circuit. Connects
        the final supercoiling region to the first with an origin of replication component.
        """
        super(Plasmid, self).setup()
        # set up origin of replication and link from final supercoiling region to initial supercoiling region
        components, coil, sc_index = self.create_barrier("origin", None, len(self.local.supercoil_regions)-1,
                                                         self.init_coil)
        self.circuit_components = self.circuit_components + components
