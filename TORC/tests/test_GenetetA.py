from unittest import TestCase
from TORC import Supercoil, GenetetA, SignalError, Channel, LocalArea
from threading import Thread
from queue import Queue


class TestGenetetA(TestCase):

    def test_output_signal(self):
        local = LocalArea()
        cw_supercoil_1_channel = Queue()
        acw_supercoil_1_channel = Queue()
        cw_supercoil_2_channel = Queue()
        acw_supercoil_2_channel = Queue()
        supercoil_1 = Supercoil(cw_supercoil_1_channel, acw_supercoil_1_channel, local)
        supercoil_2 = Supercoil(cw_supercoil_2_channel, acw_supercoil_2_channel, local)
        gene = GenetetA(cw_supercoil_2_channel, supercoil_1, supercoil_2, local)
        # with self.assertRaises(SignalError, msg="Signalled with no listener"):
        #     gene.output_signal()
        try:
            threads = [Thread(target=supercoil_2.coil), Thread(target=gene.output_signal)]
            [x.start() for x in threads]
            [x.join() for x in threads]
        except SignalError:
            self.fail("Failed to listen with signal")

    def test_update(self):
        local = LocalArea()
        cw_supercoil_1_channel = Queue()
        acw_supercoil_1_channel = Queue()
        cw_supercoil_2_channel = Queue()
        acw_supercoil_2_channel = Queue()
        supercoil_1 = Supercoil(cw_supercoil_1_channel, acw_supercoil_1_channel, local)
        supercoil_2 = Supercoil(cw_supercoil_2_channel, acw_supercoil_2_channel, local)
        gene = GenetetA(cw_supercoil_2_channel, supercoil_2, supercoil_1, local)
        threads = [Thread(target=gene.update), Thread(target=supercoil_2.update)]
        [x.start() for x in threads]
        [x.join() for x in threads]
        self.assertEqual(-1, local.get_supercoil(supercoil_2.supercoiling_region), "Did not update region")

    def test_inverted_GenetetA(self):
        local = LocalArea()
        cw_supercoil_1_channel = Queue()
        acw_supercoil_1_channel = Queue()
        cw_supercoil_2_channel = Queue()
        acw_supercoil_2_channel = Queue()
        supercoil_1 = Supercoil(cw_supercoil_1_channel, acw_supercoil_1_channel, local)
        supercoil_2 = Supercoil(cw_supercoil_2_channel, acw_supercoil_2_channel, local)
        gene = GenetetA(acw_supercoil_1_channel, supercoil_2, supercoil_1, local, clockwise=True)
        threads = [Thread(target=gene.update), Thread(target=supercoil_1.update)]
        [x.start() for x in threads]
        [x.join() for x in threads]
        self.assertEqual(-1, local.get_supercoil(supercoil_1.supercoiling_region), "Did not update correct region")
