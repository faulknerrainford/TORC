from TORC import ReceivingError


class Supercoil:
    """
    Supercoil provides supercoiling regions and globals for their use.

    Parameters
    ----------
    channel :   JoinableQueue
        Queue for receiving signals to update the coiling state, normally sent by gene, block or bridge component.
    local   :   LocalArea
        Tracks the supercoiling and proteins in the circuit
    """

    def __init__(self, channel, local):
        self.channel = channel
        self.supercoiling_region = local.add_supercoil()
        self.local = local

    def coil(self):
        """
        Function for listening for a coil signal and updating the supercoiling state of the region in the region list.

        Raises
        ------
        ReceivingError: SignalError
            Indicates that a signal was listened for but not received.
        """
        try:
            update = self.channel.recv()
        except ReceivingError:
            raise ReceivingError
        if update:
            self.local.set_supercoil(self.supercoiling_region, update)

    def get_coil_state(self):
        """
        Reads current coil state from the list.

        Returns
        --------
        String
            Current state of the supercoiling region
        """
        return self.local.get_supercoil(self.supercoiling_region)

    def update(self):
        """
        Updates supercoiling region by listening for a change in coil signal.
        """
        try:
            self.coil()
        except ReceivingError:
            pass
