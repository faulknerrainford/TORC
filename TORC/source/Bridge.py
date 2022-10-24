from TORC import Environment, Supercoil, SendingError, Channel


class Bridge:
    """
    Bridge class provides the bridge end components and their functions for checking for environment proteins, other
    bridge components and transmitting supercoiling between supercoiling regions.

    Parameters
    ----------
    label : String
        name of protein it looks for in the environment
    sc_acw : int
        anti-clockwise supercoiling regions index
    sc_cw : int
        clockwise supercoiling regions index (should share the queue with this bridge)
    protein_threshold : float
        Required amount of protein in the environment for bridge to be active.
    channel : Channel
        Same channel as held by clockwise supercoiling region used to transmit supercoiling from anti-clockwise to
        clockwise regions
    """
    def __init__(self, label, sc_acw=0, sc_cw=0, channel=None, protein_threshold=0):
        self.label = label
        self.supercoiling_clockwise = sc_cw
        self.supercoiling_anticlockwise = sc_acw
        if channel:
            self.coil_channel = channel
        else:
            self.coil_channel, _ = Channel()
        self.threshold = protein_threshold
        self.bridge_check = None

    def set_bridge_check(self, bridge):
        """
        Set the bridge check variable to point to the other end of bridge

        Parameters
        ----------
        bridge : Bridge
            Other end of bridge
        """
        self.bridge_check = bridge

    def check_state(self):
        """
        Checks the other bridge exists (not None) and has same trigger protein and trigger protein in environment. If
        bridge component correct and protein present return true if not return false.

        Returns
        --------
        boolean
            True if bridge closed/active, False otherwise.
        """
        # Check the other bridge exists (not None) and has same trigger protein and trigger protein in environment
        if self.bridge_check and self.bridge_check.label == self.label and \
                Environment.environment_dictionary[self.label] > self.threshold:
            return True
        else:
            return False

    def coil_in(self):
        """
        Reads and returns the state of the supercoiling regions

        Returns
        --------
        String
            State of the supercoiling region
        """
        # looks up and return anti-clockwise coiling state
        return Supercoil.region_list[self.supercoiling_anticlockwise]

    def coil_out(self, signal):
        """
        Sends the coil signal to the next clockwise supercoiling region.

        Parameters
        ----------
        signal  :   String
            State to update the supercoiling region to.

        Raises
        --------
        SendingError
            Failed to send signal
        """
        # sends a coil signal on coil_queue to supercoiling clockwise
        try:
            self.coil_channel.send(signal)
        except SendingError:
            raise SendingError

    def update(self):
        """
        Checks if the bridge is open and if it is transmits the supercoiling state between the supercoiling regions
        either side.
        """
        if not self.check_state():
            self.coil_out(self.coil_in())
