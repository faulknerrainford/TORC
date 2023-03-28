from unittest import TestCase
from TORC import Origin, LocalArea, Channel, Supercoil


class TestOrigin(TestCase):
    def test_update(self):
        local = LocalArea()
        test_sc, test_bridge = Channel()
        with self.assertRaises(IndexError, msg="Generates Origin with out supercoiling regions"):
            origin = Origin("Origin", local, 0, 1, test_sc)
        supercoil0 = Supercoil(test_sc, local)
        supercoil1 = Supercoil(test_sc, local)
        origin = Origin("Origin", local, 0, 1, test_sc)
        self.assertEqual("Origin", origin.label, "Incorrect labelling")


