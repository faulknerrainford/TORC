from TORC import Barrier


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
    """

    def __init__(self, label, local, sc_cw, sc_acw):
        super(Origin, self).__init__(local, sc_cw, sc_acw)
        self.label = label

    def barrier_check(self):
        return False
