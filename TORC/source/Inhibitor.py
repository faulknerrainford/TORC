from queue import Queue


class Inhibitor:
    """
    Manages communication for between two environments to provide the ability to inhibit a protein in the
    environment
    """
    def __init__(self):
        self.list = []
        self.queue = Queue()

    def send(self, u):
        """
        Sends a value to the inhibitor, if it is still waiting on the second value nothing happens otherwise the result
        is calculated and returns using the queue

        Parameter
        ---------
        u : int
            current value of one of the environments
        """
        self.list.append(u)
        if len(self.list) == 2:
            self.list.append(abs(self.list[0]-self.list[1]))
            v = min(self.list)
            self.list = []
            self.queue.put(v)
            self.queue.put(v)

    def get(self):
        """
        Returns the amount to reduce both environments by due to annihilation.

        Return
        ------
        int
            amount to reduce environment by, can not be more than the environments current content.
        """
        return self.queue.get()
