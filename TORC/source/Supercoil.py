import _queue
from TORC import ReceivingError, Channel


class Supercoil:
    """
    Supercoil provides supercoiling regions and globals for their use.

    Globals
    -------
    super_coil_index : int
        integer indicating current number of regions and number value of the next to be created.
    region_list : List<String>
        List with the coiling state of each supercoiling region.

    Parameters
    ----------
    receiving_queue : JoinableQueue
        Queue for receiving signals to update the coiling state, normally sent by gene, block or bridge component.
    """
    super_coil_index = 0
    region_list = []

    def __init__(self, channel):
        self.channel = channel
        self.supercoiling_region = self.super_coil_index
        Supercoil.region_list.append("neutral")
        Supercoil.super_coil_index = Supercoil.super_coil_index + 1

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
            Supercoil.region_list[self.supercoiling_region] = update

    def get_coil_state(self):
        """
        Reads current coil state from the list.

        Returns
        --------
        String
            Current state of the supercoiling region
        """
        return self.region_list[self.supercoiling_region]

    def update(self):
        """
        Updates supercoiling region by listening for a change in coil signal.
        """
        try:
            self.coil()
        except ReceivingError:
            pass
