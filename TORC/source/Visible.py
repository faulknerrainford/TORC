from webcolors import rgb_to_name
from TORC import Environment


class Visible:
    """
    Class provides component which tracks the colour of the visual output from any fluorescent proteins produced by the
    system.
    """

    def __init__(self):
        self.label = "visible"
        self.rgb = [0.0, 0.0, 0.0]
        self.colour = "black"
        pass

    def read_signal(self):
        """
        Reads in the signals from the 6 main colour components: red, blue, green, yellow, cyan, magenta. These are then
        combined for use.
        """
        # read from red, blue, green, yellow, magenta, cyan environments.
        if "red" in Environment.environment_dictionary.keys():
            self.rgb[0] = Environment.environment_dictionary["red"]
        if "green" in Environment.environment_dictionary.keys():
            self.rgb[1] = Environment.environment_dictionary["green"]
        if "blue" in Environment.environment_dictionary.keys():
            self.rgb[2] = Environment.environment_dictionary["blue"]
        if "magenta" in Environment.environment_dictionary.keys():
            self.rgb[0] = self.rgb[0] + Environment.environment_dictionary["magenta"]*0.5
            self.rgb[2] = self.rgb[2] + Environment.environment_dictionary["magenta"]*0.5
        if "yellow" in Environment.environment_dictionary.keys():
            self.rgb[0] = self.rgb[0] + Environment.environment_dictionary["yellow"]*0.5
            self.rgb[1] = self.rgb[2] + Environment.environment_dictionary["yellow"]*0.5
        if "cyan" in Environment.environment_dictionary.keys():
            self.rgb[1] = self.rgb[0] + Environment.environment_dictionary["cyan"]*0.5
            self.rgb[2] = self.rgb[2] + Environment.environment_dictionary["cyan"]*0.5
        # Sum to get an RGB colour and normalize
        self.rgb = [x/max(self.rgb) for x in self.rgb]
        pass

    # noinspection PyTypeChecker
    def check_colour(self):
        """
        Converts the rgb list created in read_signal to a string name of a colour.
        """
        # Match current colour to named colour and return as label/check metric
        self.colour = rgb_to_name(tuple([int(255*x) for x in self.rgb]))
        pass

    def update(self):
        """
        Read in signals from environment and updates colour name.
        """
        self.read_signal()
        self.check_colour()
        # TODO: output an updated version of the output colour to terminal to track output
        pass
