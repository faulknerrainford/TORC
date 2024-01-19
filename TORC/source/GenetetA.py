from TORC import Promoter, Barrier


class GenetetA(Promoter, Barrier):
    """
    Gene component, causes supercoiling for region attached by Channel.

    Parameters
    ----------
    channel                 :   Queue
        Queue to output supercoiling
    cw_supercoil_region     :   Supercoil
        Region of supercoiling negative supercoiling is generated in, this is the region clockwise of the gene.
    acw_supercoil_region    :   Supercoil
        Region of supercoiling the gene is in, this is the region anti-clockwise of the gene.
    local                   :   LocalArea
        Tracks the supercoiling and proteins in the circuit
    sc_strength             :   int
        The amount of supercoiling to generate upstream
    clockwise               :   Boolean
        The orientation of the gene, defaults to anticlockwise, if modified cw and acw sc regions need to be
        the other way around
    """
    gene_instance_count = 0

    def __init__(self, channel, cw_supercoil_region, acw_supercoil_region, local, sc_strength=-1, clockwise=False):
        if clockwise:
            Promoter.__init__(self, "tetA", cw_supercoil_region.supercoiling_region, local, clockwise=clockwise,
                              output_channel=local.get_supercoil_acw(acw_supercoil_region.supercoiling_region))
        else:
            Promoter.__init__(self, "tetA", acw_supercoil_region.supercoiling_region, local, clockwise=clockwise,
                              output_channel=local.get_supercoil_cw(cw_supercoil_region.supercoiling_region))
        Barrier.__init__(self, local, cw_sc_region=cw_supercoil_region, acw_sc_region=acw_supercoil_region)
        self.id = "Gene_" + self.label + "_" + str(GenetetA.gene_instance_count)
        self.sc_strength = sc_strength

    def update(self):
        Promoter.update(self)
        Barrier.update(self)

    def barrier_check(self):
        return False

    def input_check(self):
        return True

    def output_signal(self, strength=None):
        """
        Sends negative signal to supercoil via provided channel. Waits for confirmation of receipt before exit.

        Raises
        -------
        SendingError: SignalError
            Indicated the signal was not received and so was cleared from pipe.
        """
        if strength == "strong":
            self.output_channel.put(self.sc_strength)
