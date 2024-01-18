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
    local           :   LocalArea
        Tracks the supercoiling and proteins in the circuit
    region          :   Int
        The supercoiling region the promoter belongs to.
    weak            :   float
        The rate of output when neutrally coiled
    strong          :   float
        The rate of output when negatively coiled
    output_channel  :   JoinableQueue or Channel
        The channel to send output on to the environment component or supercoiling signals
    fluorescent     :   Boolean
        Indicates if the promoters gene produces RNA for a fluorescent protein
    promote         :   Environment
        Indicated a transcription factor which the promoter responds to by increasing production
    repress         :   Environment
        Indicates a transcription factor which the promoter responds to by decreasing production
    sc_sensitive    :   Boolean
        Indicates if the promoter responds strongly to the supercoiling state
    sc_rate         :   float
        The rate at which the promoter and gene produce supercoiling (positive downstream, negative upstream)
    clockwise       :   Boolean
        Indicates the orientation of the promoter and gene on a plasmid (right on a genome)
    """

    def __init__(self, label, region, local, weak=0, strong=1, output_channel=None, fluorescent=False, promote=None,
                 repress=None, sc_sensitive=True, sc_rate=0, clockwise=True):
        self.label = label
        self.gene = label.split("_")[0]
        self.coil_state = 0
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
        self.sc_rate = sc_rate
        self.clockwise = clockwise

    def update(self):
        """
        Updates state of promoter including output to the environment and updating coil-state if changed.
        """
        self.state_update()
        if self.input_check():
            self.output_signal("strong")
        else:
            self.output_signal("weak")

    def state_update(self):
        """
        Checks and updates the supercoiling state of the promoter.
        """
        current_sc_state = self.local.get_supercoil(self.region)
        if self.coil_state != current_sc_state:
            self.coil_state = current_sc_state

    def input_check(self):
        """
        Checks coiling signal and updates coil_state if it has changed.
        Checks if repressor active -> returns false
        Checks if promoter protein present -> returns true
        Checks if supercoiling negative and sc_sensitive -> returns true
        """
        if self.repress:
            if self.local.get_environment(self.repress) > 0:
                return False
        if self.promote:
            if self.local.get_environment(self.promote) > 0:
                return True
        if self.coil_state < 0 and self.sc_sensitive:
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
            # output + and - sc to region
            if self.clockwise:
                self.local.get_supercoil_cw(self.region).put(self.sc_rate)
                self.local.get_supercoil_acw(self.region).put(-1*self.sc_rate)
            else:
                self.local.get_supercoil_cw(self.region).put(-1*self.sc_rate)
                self.local.get_supercoil_acw(self.region).put(self.sc_rate)



