class Origin(Barrier):
    """
    Class for the origin of replication supercoiling barrier in plasmids. Acts as a solid barrier with no transmission
    of supercoiling. Checks that both given supercoiling regions exist.

    Parameters
    ----------
    label       :   String
        Name of the origin of replication, can be place holder to label which origin of replication is being used.
    local       :   LocalArea
        The local area object holds information on local environments and supercoiling regions for a single circuit.
    sc_cw       :   Int
        The index of the clockwise supercoiling region, should be the first supercoiling region in the plasmid.
    sc_acw      :   Int
        The index of the anti-clockwise supercoiling region, should be the last supercoiling region in the plasmid.
    init_coil   :   Channel
        The Channel for feeding coiling information to the clockwise (initial) supercoiling region. Is not currently
        used.
    """

    def __init__(self, label, local, sc_cw, sc_acw, init_coil):
        self.label = label
        self.supercoiling_clockwise = sc_cw
        self.supercoiling_anticlockwise = sc_acw
        self.init_coil = init_coil
        # check both supercoiling regions present
        local.get_supercoil(self.supercoiling_clockwise)
        local.get_supercoil(self.supercoiling_anticlockwise)

    def update(self):
        """
        Currently the origin of replication performs no action other than defining a barrier between supercoiling
        regions. Its update therefore does nothing.
        """
        pass
