class Promoter:
    """
    Promoter class increases the amount of protein in the local environment based on the current state of environmental
    proteins and supercoiling. This includes the existence of proteins in the environment both promoting and repressing
    expression.

    Parameters
    -----------
    label           :   String
        Name of the protein being promoted used to ID, in case of multiple promoters of the same type name_i is used
        to number the instances.
    local       :   LocalArea
        Tracks the supercoiling and proteins in the circuit
    region          :   Int
        The supercoiling region the promoter belongs to.
    weak    :   float
        The rate of output when neutrally coiled
    strong          :   float
        The rate of output when negatively coiled
    output_channel    :   JoinableQueue or Channel
        The channel to send output on to the environment component or supercoiling signals
    """

    def __init__(self, label, region, local, weak=0, strong=1, output_channel=None, fluorescent=False, promote=None,
                 repress=None, sc_sensitive=True):
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
        self.local = local
        self.promote = promote
        self.repress = repress
        self.sc_sensitive = sc_sensitive

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
        Checks if repressor active -> returns false
        Checks if promoter protein present -> returns true
        Checks if supercoiling negative and sc_sensitive -> returns true
        """
        current_sc_state = self.local.get_supercoil(self.region)
        if self.coil_state != current_sc_state:
            self.coil_state = current_sc_state
        if self.repress:
            if self.local.get_environment(self.repress) > 0:
                return False
        if self.promote:
            if self.local.get_environment(self.promote) > 0:
                return True
        if self.coil_state == "negative":
            return True
        return False

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
