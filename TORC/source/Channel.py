from threading import Event
from queue import Queue, Empty
from TORC import SendingError, ReceivingError


# noinspection PyPep8Naming
def Channel():
    """
    Function creates two objects with matching queues and events to use for channel ends.

    Returns
    --------
    ChannelEnd
        One end of the channel
    ChannelEnd
        Other end of the channel
    """
    event = Event()
    queue = Queue()
    return ChannelEnd(queue, event), ChannelEnd(queue, event)


class ChannelEnd:
    """
    Provides send and receive functions both of which require the confirmation from the other to complete
    successfully.

    Parameters
    ----------
    queue : Queue
        Transmits data through the channel
    event : Event
        Confirms receipt of the data
    """

    def __init__(self, queue, event):
        self.event = event
        self.queue = queue

    def send(self, data):
        """
        Sends data with the confirmation of receipt.

        Parameters
        -----------
        data : Object
            Information to transmit on channel

        Raises
        -------
        SendingError
            Transmission failed.
        """
        self.queue.put(data)
        self.event.wait(1)
        if not self.event.is_set():
            if not self.queue.empty():
                self.queue.get()
            raise SendingError

    def recv(self):
        """
        Receives data transmitted over channel and sends confirmation.

        Returns
        --------
        data    :   Object
            data received over channel

        Raises
        -------
        ReceivingError
            Failed to receive data.
        """
        try:
            data = self.queue.get(timeout=2)
            self.event.set()
            return data
        except Empty:
            raise ReceivingError
