from TORC import SignalError, SendingError, Promoter, Barrier


class GenetetA(Promoter, Barrier):
    """
    Gene component, causes supercoiling for region attached by Channel.

    Parameters
    ----------
    channel: ChannelEnd
        channel and event used to signal the supercoiling region clockwise of the gene. Matching end should be provided
        as the receiving channel to supercoil.
    supercoil_region: int
        Region of supercoiling the gene is in, this is the region anti-clockwise of the gene.
    local       :   LocalArea
        Tracks the supercoiling and proteins in the circuit
    """
    gene_instance_count = 0

    def __init__(self, channel, supercoil_region, local, sc_strength=-1):
        super(GenetetA, self).__init__("tetA", supercoil_region, local, output_channel=channel)
        self.id = "Gene_" + self.label + "_" + str(GenetetA.gene_instance_count)
        self.sc_strength = sc_strength

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
