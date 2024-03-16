import numpy as np
from scipy.stats import norm


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
    threshold       :   float
        Value used for threshold for transcription coiling
    sc_sensitive    :   Boolean
        Indicates if the promoter responds strongly to the supercoiling state
    sc_rate         :   float
        The rate at which the promoter and gene produce supercoiling (positive downstream, negative upstream)
    clockwise       :   Boolean
        Indicates the orientation of the promoter and gene on a plasmid (right on a genome)
    """

    def __init__(self, label, region, local, weak=0, strong=1, output_channel=None, fluorescent=False, promote=None,
                 repress=None, sc_sensitive=True, sc_rate=0, clockwise=True, threshold=0, rate_dist="threshold",
                 gradient=1):
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
        self.threshold = threshold
        self.sc_sensitive = sc_sensitive
        self.sc_rate = sc_rate
        self.clockwise = clockwise
        self.rate_dist = rate_dist
        self.gradient = gradient

    def update(self):
        """
        Updates state of promoter including output to the environment and updating coil-state if changed.
        """
        self.state_update()
        status = self.input_check()
        output = self.rate_calc(status)
        self.output_signal(output)

    def state_update(self):
        """
        Checks and updates the supercoiling state of the promoter.
        """
        current_sc_state = self.local.get_supercoil(self.region)
        if self.coil_state != current_sc_state:
            self.coil_state = current_sc_state

    def input_check(self):
        """
        Collects information on current state of transcription factors environments for repression, promotion and the
        current supercoiling state of the promoter.

        Returns
        -------
        dict
            dict with information on repression, promotion and supercoiling if relevant.
        """
        status = {}
        if self.repress:
            status["repress"] = self.local.get_environment(self.repress)
        if self.promote:
            status["promote"] = self.local.get_environment(self.promote)
        status["supercoiling"] = self.coil_state
        return status

    def rate_calc(self, status):
        """
        Calculate the rate of transcription based on repression, promotion and supercoiling levels.

        Threshold
        ----------
        The threshold function acts as a digital switch between the weak and strong signal activated when a promoting
        transcription factor is above the given threshold and the repressing transcription factor is not. (Unless the
        promoter is supercoiling sensitive, in which case this is activated when supercoiling is below the threshold.)

        Sigmoid
        -------

        Normal
        ------

        Parameters
        ----------
        status  :   dict
            dict with information on repression, promotion and supercoiling if relevant.

        Returns
        -------
        float
            rate of transcription for output signal
        """
        # TODO: add options based on mean and dist type and parameter for dist (pos second param needed) for poisson
        #  dist, negative binomial
        if self.rate_dist == "threshold":
            # threshold
            if self.sc_sensitive and status["supercoiling"] < self.threshold:
                return self.strong_signal
            elif "repress" in status.keys() and status["repress"] > self.threshold:
                return self.weak_signal
            elif "promote" in status.keys() and status["promote"] > self.threshold:
                return self.strong_signal
            else:
                return self.weak_signal
        elif self.rate_dist == "sigmoid":
            # sigmoid function
            if self.sc_sensitive:
                x = status["supercoiling"]
            else:
                x = status["promote"]
            x_prime = self.gradient*x-self.threshold
            y = 1/(1 + np.exp(-x_prime))
            y_range = self.strong_signal - self.weak_signal
            y_prime = y*y_range + self.weak_signal
            return y_prime
        elif self.rate_dist == "normal":
            # normal function
            if self.sc_sensitive:
                x = status["supercoiling"]
            else:
                x = status["promote"]
            y = norm.pdf(x, self.threshold, self.gradient)*(2.5*(self.strong_signal-self.weak_signal))+self.weak_signal
            return y
        else:
            return self.weak_signal

    def output_signal(self, strength=None):
        """
        Sends correct rate on the output channel

        Parameters
        ----------
        strength    :   float
            output strength, rate of transcription, also applied to rate of supercoiling
        """
        self.output_channel.put(strength)
        # output + and - sc to region
        if strength > 0:
            sc_strength = strength * self.sc_rate
            if self.clockwise:
                self.local.get_supercoil_cw(self.region).put(sc_strength)
                self.local.get_supercoil_acw(self.region).put(-1*sc_strength)
            else:
                self.local.get_supercoil_cw(self.region).put(-1*sc_strength)
                self.local.get_supercoil_acw(self.region).put(sc_strength)



