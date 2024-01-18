from TORC import SendingError, Channel, Barrier


class Bridge(Barrier):
    """
    Bridge class provides the bridge end components and their functions for checking for environment proteins, other
    bridge components and transmitting supercoiling between supercoiling regions.

    Parameters
    ----------
    label               :   String
        name of protein it looks for in the environment
    local               :   LocalArea
        container tracking supercoiling and protein production within the circuit.
    cw_sc_region        :   Supercoil
        anti-clockwise supercoiling regions index
    acw_sc_region       :   Supercoil
        clockwise supercoiling regions index (should share the queue with this bridge)
    protein_threshold   :   float
        Required amount of protein in the environment for bridge to be active.
    """
    def __init__(self, label, local, cw_sc_region, acw_sc_region, protein_threshold=0):
        super(Bridge, self).__init__(local, cw_sc_region, acw_sc_region)
        self.label = label
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

    def barrier_check(self):
        """
        Checks the other bridge exists (not None) and has same trigger protein and trigger protein in environment. If
        bridge component correct and protein present return true if not return false.

        Returns
        --------
        Boolean
            True if bridge closed/active, False otherwise.
        """
        # Check the other bridge exists (not None) and has same trigger protein and trigger protein in environment
        if self.bridge_check and self.bridge_check.label == self.label and \
                self.local.get_environment(self.label) > self.threshold:
            return False
        else:
            return True

    # def coil_in(self):
    #     """
    #     Reads and returns the state of the supercoiling regions
    #
    #     Returns
    #     --------
    #     String
    #         State of the supercoiling region
    #     """
    #     # looks up and return anti-clockwise coiling state
    #     return self.local.get_supercoil(self.supercoiling_anticlockwise)
    #
    # def coil_out(self, signal):
    #     """
    #     Sends the coil signal to the next clockwise supercoiling region.
    #
    #     Parameters
    #     ----------
    #     signal  :   String
    #         State to update the supercoiling region to.
    #
    #     Raises
    #     --------
    #     SendingError
    #         Failed to send signal
    #     """
    #     # sends a coil signal on coil_queue to supercoiling clockwise
    #     try:
    #         self.coil_channel.send(signal)
    #     except SendingError:
    #         raise SendingError

    # def update(self):
    #     """
    #     Checks if the bridge is open and if it is transmits the supercoiling state between the supercoiling regions
    #     either side.
    #     """
    #     if not self.check_state():
    #         self.coil_out(self.coil_in())
