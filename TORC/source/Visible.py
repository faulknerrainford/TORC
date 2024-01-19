from webcolors import rgb_to_name
from TORC import LocalArea


class Visible:
    """
    Class provides component which tracks the colour of the visual output from any fluorescent proteins produced by the
    system.

    Parameters
    -----------
    local       :   LocalArea
        Tracks the supercoiling and proteins in the circuit
    """

    def __init__(self, local):
        self.label = "visible"
        self.rgb = [0.0, 0.0, 0.0]
        self.colour = "black"
        self.local = local

    def read_signal(self):
        """
        Reads in the signals from the 6 main colour components: red, blue, green, yellow, cyan, magenta. These are then
        combined for use.
        """
        # read from red, blue, green, yellow, magenta, cyan environments.
        if "red" in self.local.get_keys():
            self.rgb[0] = self.local.get_environment("red")
        if "green" in self.local.get_keys():
            self.rgb[1] = self.local.get_environment("green")
        if "blue" in self.local.get_keys():
            self.rgb[2] = self.local.get_environment("blue")
        if "magenta" in self.local.get_keys():
            self.rgb[0] = self.rgb[0] + self.local.get_environment("magenta")*0.5
            self.rgb[2] = self.rgb[2] + self.local.get_environment("magenta")*0.5
        if "yellow" in self.local.get_keys():
            self.rgb[0] = self.rgb[0] + self.local.get_environment("yellow")*0.5
            self.rgb[1] = self.rgb[2] + self.local.get_environment("yellow")*0.5
        if "cyan" in self.local.get_keys():
            self.rgb[1] = self.rgb[0] + self.local.get_environment("cyan")*0.5
            self.rgb[2] = self.rgb[2] + self.local.get_environment("cyan")*0.5
        # Sum to get an RGB colour and normalize
        if max(self.rgb)>0:
            self.rgb = [x/max(self.rgb) for x in self.rgb]

    # noinspection PyTypeChecker
    def check_colour(self):
        """
        Converts the rgb list created in read_signal to a string name of a colour. If it can't match to a named colour
        it will set colour as "Undefined"
        """
        # Match current colour to named colour and return as label/check metric
        try:
            self.colour = rgb_to_name(tuple([int(255*x) for x in self.rgb]))
        except ValueError:
            self.colour = "Undefined"

    def update(self):
        """
        Read in signals from environment and updates colour name.
        """
        self.read_signal()
        self.check_colour()
