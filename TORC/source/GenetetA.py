from TORC import SignalError, SendingError, Promoter


class GenetetA(Promoter):
    """
    Gene component, causes supercoiling for region attached by Channel.

    Parameters
    ----------
    channel: ChannelEnd
        channel and event used to signal the supercoiling region. Matching end should be provided as the receiving
        channel to supercoil.
    """
    gene_instance_count = 0

    def __init__(self, channel, supercoil_region):
        super(GenetetA, self).__init__("tetA", supercoil_region, output_channel=channel)
        self.id = "Gene_" + self.label + "_" + str(GenetetA.gene_instance_count)

    def output_signal(self, strength=None):
        """
        Sends negative signal to supercoil via provided channel. Waits for confirmation of receipt before exit.

        Raises
        -------
        SendingError: SignalError
            Indicated the signal was not received and so was cleared from pipe.
        """
        try:
            self.output_channel.send("negative")
        except SignalError:
            raise SendingError

