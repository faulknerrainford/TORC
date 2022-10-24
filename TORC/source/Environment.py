class Environment:
    """
    Environment class tracks presence of a protein in the environment. It signals out the current state of the protein
    in the environment and then updates the contents based on output from other components.

    Parameters
    ----------
    label       :   String
        The name of the protein being tracked.
    content     :   float
        The current amount of protein in the environment.
    decay_rate   :   float
        The linear decay rate of the protein in the environment
    input_queue   :   Queue
        The signal channel for receiving additions of protein to the environment
    """
    environment_dictionary = {}

    def __init__(self, label, content=0, decay_rate=0, input_queue=None, fluorescent=False):
        self.label = label
        self.content = content
        self.decay = decay_rate
        self.input = input_queue
        self.fluorescent = fluorescent
        Environment.environment_dictionary[self.label] = self.content

    def update(self):
        """
        Updates content of the environment by first sending the current state out and then by reading in new input to
        the environment.
        """
        self.send_signal()
        self.read_signal()

    def read_signal(self):
        """
        Reads in any signals on the input queue to add to the current levels and then decays with a catch to prevent
        levels below 0.
        """
        length = self.input.qsize()
        for i in range(length):
            self.content = self.content + self.input.get()
        self.content = max(self.content - self.decay, 0)

    def send_signal(self):
        """
        Updates levels of proteins in the environment using the environment dictionary.
        """
        Environment.environment_dictionary[self.label] = self.content
