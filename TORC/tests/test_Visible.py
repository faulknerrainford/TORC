from unittest import TestCase
from TORC import Promoter, Supercoil, Environment, Visible


class TestVisible(TestCase):
    def test_read_signal(self):
        # set up environment dictionary test different settings within it
        Environment.environment_dictionary["red"] = 1
        vis = Visible()
        self.assertEqual(vis.rgb, [0.0, 0.0, 0.0], "Incorrect at initialisation")
        vis.read_signal()
        self.assertEqual(vis.rgb, [1.0, 0.0, 0.0], "Not read correctly")
        Environment.environment_dictionary["blue"] = 1
        vis.read_signal()
        self.assertEqual(vis.rgb, [1.0, 0.0, 1.0], "Not combined correctly")
        # reset Environment dictionary after
        del Environment.environment_dictionary["blue"]
        del Environment.environment_dictionary["red"]

    def test_check_colour(self):
        # set the rgb values and test the returned colour name
        vis = Visible()
        self.assertEqual("black", vis.colour, "Incorrect initial colour")
        vis.check_colour()
        self.assertEqual("black", vis.colour, "Incorrect colour id black")
        vis.rgb = [1.0, 0.0, 0.0]
        vis.check_colour()
        self.assertEqual("red", vis.colour, "Incorrect colour id red")
        vis.rgb = [1.0, 0.0, 1.0]
        vis.check_colour()
        self.assertEqual("magenta", vis.colour, "Incorrect colour id magenta")

    def test_update(self):
        # check combination of above for a starting envo state and colour and then changing and updating to check
        #  if read and updated correctly.
        vis = Visible()
        Environment.environment_dictionary["red"] = 1
        vis.read_signal()
        self.assertEqual(vis.rgb, [1.0, 0.0, 0.0], "Not read correctly")
        Environment.environment_dictionary["blue"] = 1
        vis.update()
        self.assertEqual("magenta", vis.colour, "Not updated correctly.")
        # reset Environment dictionary after
        del Environment.environment_dictionary["blue"]
        del Environment.environment_dictionary["red"]
