class SignalError(ConnectionError):
    """
    Error indicates signal didn't complete
    """
    def __init__(self):
        super(SignalError, self).__init__()


class SendingError(SignalError):
    """
    Signal was not sent or was sent without confirmation of receipt.
    """
    def __init__(self):
        super(SendingError, self).__init__()


class ReceivingError(SignalError):
    """
    Signal was not received before timeout.
    """
    def __init__(self):
        super(ReceivingError, self).__init__()
