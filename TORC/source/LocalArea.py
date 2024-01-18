
class LocalArea:
    """
    Container for tracking supercoiling and environmental proteins in a plasmid circuit.
    """

    def __init__(self):
        self.supercoil_regions = []
        self.clockwise_channels = []
        self.anticlockwise_channels = []
        self.environments = {}

    def add_supercoil(self, cw_channel, acw_channel):
        """
        Adds a new supercoiling region tracker to the circuit

        Parameters
        ----------
        cw_channel  :   Queue
            queue for sending cw supercoiling signals to the new supercoiling region
        acw_channel :   Queue
            queue for sending acw supercoiling signals to the new supercoiling region

        Returns
        --------
        ind
            Index of the new supercoiling region.
        """
        self.supercoil_regions = self.supercoil_regions + [0]
        self.clockwise_channels = self.clockwise_channels + [cw_channel]
        self.anticlockwise_channels = self.anticlockwise_channels + [acw_channel]
        return len(self.supercoil_regions)-1

    def add_environment(self, label, value):
        """
        Adds a new protein tracker to the circuit.

        Parameters
        -----------
        label   :   String
            Name of new protein, or colour of protein to be tracked
        value   :   float
            Initial value of protein or colour in the environment
        """
        self.environments[label] = value

    def set_supercoil(self, ind, value):
        """
        Update the state of a supercoil region

        Parameters
        -----------
        ind     :   int
            Index of the supercoiling region wanted
        value   :   String
            The new status of the supercoiling region
        """
        self.supercoil_regions[ind] = value

    def get_supercoil(self, ind):
        """
        Get the current state of a supercoiling region

        Parameters
        ----------
        ind     : int
            Index of the supercoiling region wanted

        Returns
        -------
        float
            Current state of supercoiling in the system
        """
        return self.supercoil_regions[ind]

    def get_supercoil_cw(self, ind):
        """
        Get the cw channel of the supercoiling region

        Parameters
        ----------
        ind : int
            Index of the supercoiling region wanted

        Returns
        -------
        Queue
            The queue for updating clockwise supercoiling for the requested region
        """
        return self.clockwise_channels[ind]

    def get_supercoil_acw(self, ind):
        """
        Get the acw channel of the supercoiling region

        Parameters
        ----------
        ind : int
            Index of the supercoiling region wanted

        Returns
        -------
        Queue
            The queue for updating anticlockwise supercoiling for the requested region
        """
        return self.anticlockwise_channels[ind]

    def set_environment(self, label, value):
        """
        Update the state of a protein

        Parameters
        ----------
        label   :   String
            Name of protein or colour of protein
        value   :   float
            Value of protein in the environment
        """
        self.environments[label] = value

    def get_environment(self, label):
        """
        Get the current level of protein in the environment

        Parameters
        ----------
        label   :   String
            Nome of protein or colour of protein

        Returns
        ---------
        float
            Current level of protein in the environment
        """
        return self.environments[label]

    def get_keys(self):
        """
        Gets list of proteins currently being tracked by the environment

        Returns
        --------
        List<String>
            The names of all proteins currently tracked in the environment.
        """
        return self.environments.keys()
