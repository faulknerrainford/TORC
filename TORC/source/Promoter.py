from TORC import Supercoil


class Promoter:
    """
    Promoter class increases the amount of protein in the local environment

    Parameters
    -----------
    label           :   String
        Name of the protein being promoted used to ID, in case of multiple promoters of the same type name_i is used
        to number the instances.
    region          :   Int
        The supercoiling region the promoter belongs to.
    weak    :   float
        The rate of output when neutrally coiled
    strong          :   float
        The rate of output when negatively coiled
    output_channel    :   JoinableQueue or Channel
        The channel to send output on to the environment component or supercoiling signals
    """

    def __init__(self, label, region, weak=0, strong=1, output_channel=None, fluorescent=False):
        self.label = label
        self.gene = label.split("_")[0]
        self.coil_state = "neutral"
        self.weak_signal = weak
        self.strong_signal = strong
        if not isinstance(region, int):
            raise TypeError("Integer supercoiling region must be provided")
        self.region = region
        if not output_channel:
            raise TypeError("An output queue must be provided")
        self.output_channel = output_channel
        self.fluorescent = fluorescent

    def update(self):
        """
        Updates state of promoter including output to the environment and updating coil-state if changed.
        """

        self.input_check()
        if self.input_check():
            self.output_signal("strong")
        else:
            self.output_signal("weak")
            pass

    def input_check(self):
        """
        Checks coiling signal and updates coil_state if it has changed.
        """

        current_sc_state = Supercoil.region_list[self.region]
        if self.coil_state != current_sc_state:
            self.coil_state = current_sc_state
        return True

    def output_signal(self, strength=None):
        """
        Sends correct rate on the output channel

        Parameters
        ----------
        strength    :   String
            indicates if output signal is "weak" or "strong".
        """

        if strength == "weak":
            self.output_channel.put(self.weak_signal)
        elif strength == "strong":
            self.output_channel.put(self.strong_signal)
        else:
            pass
