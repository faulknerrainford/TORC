from unittest import TestCase
from TORC import Genome


class TestGenome(TestCase):
    def test_setup(self):
        circuit = Genome([("tetA"), ("CF", "red"), ("bridge", "lac"), ("CF", "blue"), ("bridge", "lac")],
                         environments=[("lac", 0)])
        circuit.setup()
        # check correct number of supercoil regions
        self.assertEqual(4, len(circuit.local.supercoil_regions), "Incorrect number of supercoiling regions created")
        # check correct environments
        self.assertEqual(sorted(["lac", "red", "blue"]), sorted(circuit.local.get_keys()),
                         "Incorrect Environment setup")
        self.assertEqual(13, len(circuit.circuit_components), "Incorrect component list")

    def test_run(self):
        circuit0 = Genome([("tetA"), ("CF", "red"), ("bridge", "lac"), ("CF", "blue"), ("bridge", "lac")],
                          environments=[("lac", 0)])
        circuit0.setup()
        circuit0.run(10)
        # check visible correct
        self.assertEqual("Undefined", circuit0.visible.colour, "Incorrect output colour, no lac")
        circuit20 = Genome([("tetA"), ("CF", "red"), ("bridge", "lac"), ("CF", "blue"), ("bridge", "lac")],
                           environments=[("lac", 20)])
        circuit20.setup()
        circuit20.run(10)
        # check correct environments and visible correct
        self.assertEqual("red", circuit20.visible.colour, "Incorrect output colour, with lac")
