from TORC import ReceivingError


class Supercoil:
    """
    Supercoil provides supercoiling regions and globals for their use.

    Parameters
    ----------
    cw_channel  :   Queue
        Queue for receiving signals to update the clockwise coiling state, spent by all transcribing genes.
        component.
    acw_channel :   Queue
        Queue for receiving signals to update the anti-clockwise coiling state, spent by all transcribing genes.
    local       :   LocalArea
        Tracks the supercoiling and proteins in the circuit
    global_sc   : float
        global supercoiling of the plasmid, used to set initial supercoiling values
    relax       : float
        The proportion of relaxation that occurs on update from previous time
    """
    def __init__(self, cw_channel, acw_channel, local, global_sc=0, relax=1):
        self.cw_channel = cw_channel
        self.acw_channel = acw_channel
        self.supercoiling_region = local.add_supercoil(cw_channel, acw_channel)
        self.local = local
        # clockwise and anti-clockwise regions
        self.cw_sc = global_sc
        self.acw_sc = global_sc
        self.relax = relax

    def coil(self):
        """
        Function for listening for a coil signal and updating the supercoiling state of the region in the region list.

        """
        self.cw_sc = self.cw_sc*self.relax
        self.acw_sc = self.acw_sc*self.relax
        # process queue for each channel
        length = self.cw_channel.qsize()
        for i in range(length):
            self.cw_sc = self.cw_sc + self.cw_channel.get()
        length = self.acw_channel.qsize()
        for i in range(length):
            self.acw_sc = self.acw_sc + self.acw_channel.get()
        # update region as sum
        self.local.set_supercoil(self.supercoiling_region, self.cw_sc+self.acw_sc)

    def get_coil_state(self):
        """
        Reads current coil state from the list.

        Returns
        --------
        float
            Current state of the supercoiling region
        """
        return self.local.get_supercoil(self.supercoiling_region)

    def update(self):
        """
        Updates supercoiling region by listening for a change in coil signal.
        """
        self.coil()
