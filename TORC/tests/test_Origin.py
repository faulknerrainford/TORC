from unittest import TestCase
from TORC import Origin, LocalArea, Channel, Supercoil
from queue import Queue


class TestOrigin(TestCase):
    def test_update(self):
        local = LocalArea()
        test_cw = Queue()
        test_acw = Queue()
        with self.assertRaises(TypeError, msg="Generates Origin with out supercoiling regions"):
            origin = Origin("Origin", local, 0, 1)
        supercoil0 = Supercoil(test_cw, test_acw, local)
        supercoil1 = Supercoil(test_cw, test_acw, local)
        origin = Origin("Origin", local, supercoil0, supercoil1)
        self.assertEqual("Origin", origin.label, "Incorrect labelling")


