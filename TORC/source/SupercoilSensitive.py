from TORC import Promoter


class SupercoilSensitive(Promoter):
    """
    Fluorescent class increases the amount of visible list of a particular colour in the local environment

    Parameters
    -----------
    colour          :   String
        Name of the colour being produced used to ID, in case of multiple Fluorescent of the same type colour_i is used
        to number the instances.
    region          :   Int
        The supercoiling region the fluorescent belongs to.
    local           :   LocalArea
        Tracks the supercoiling and proteins in the circuit
    weak            :   float
        The rate of output when neutrally coiled
    strong          :   float
        The rate of output when negatively coiled
    output_channel  :   JoinableQueue
        The channel to send output on to the visible component
    """

    def __init__(self, colour, region, local, weak=0, strong=1, output_channel=None, fluorescent=False, clockwise=True,
                 sc_rate=0, threshold=0):
        super(SupercoilSensitive, self).__init__(colour, region, local, weak, strong, output_channel, fluorescent,
                                                 clockwise=clockwise, sc_rate=sc_rate, threshold=threshold)

    def input_check(self):
        """
        Checks coiling signal and updates coil_state if it has changed.

        Returns
        --------
        boolean
            If the input is correct to produce strong rather than weak output.
        """
        # super(SupercoilSensitive, self).input_check()
        return {"supercoiling": self.coil_state}
