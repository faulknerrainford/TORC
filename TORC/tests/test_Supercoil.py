from unittest import TestCase
from TORC import GenetetA, Supercoil, Channel, SignalError, LocalArea
from threading import Thread
from queue import Queue


class TestSupercoil(TestCase):

    def test_get_coil_state(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        self.assertEqual(local.get_supercoil(supercoil.supercoiling_region), supercoil.get_coil_state(),
                         "Incorrect coiling state")
        local.set_supercoil(supercoil.supercoiling_region, "Test")
        self.assertEqual(supercoil.get_coil_state(), "Test", "Incorrect test state")

    def test_coil(self):
        local = LocalArea()
        cw_channel_1 = Queue()
        acw_channel_1 = Queue()
        cw_channel_2 = Queue()
        acw_channel_2 = Queue()
        supercoil_1 = Supercoil(cw_channel_1, acw_channel_1, local)
        gene = GenetetA(cw_channel_2, supercoil_1.supercoiling_region, local)
        gene2 = GenetetA(acw_channel_2, supercoil_1.supercoiling_region, local)
        supercoil_2 = Supercoil(cw_channel_2, acw_channel_2, local)
        self.assertEqual(0, supercoil_2.get_coil_state(), "Incorrect coil state at start")
        circuit = [supercoil_2, gene]
        gene.output_signal()
        supercoil_2.coil()
        self.assertEqual(-1, supercoil_2.get_coil_state(), "Incorrect coil state after update")
        gene2.output_signal(4)
        supercoil_2.coil()
        self.assertEqual(3, supercoil_2.get_coil_state(), "Incorrect updates from combined directional input")

    # def test_region_update(self):
    #     self.fail()
    #
    # def test_get_coil_state(self):
    #     self.fail()

    def test_update(self):
        local = LocalArea()
        cw_channel_1 = Queue()
        acw_channel_1 = Queue()
        cw_channel_2 = Queue()
        acw_channel_2 = Queue()
        supercoil_1 = Supercoil(cw_channel_1, acw_channel_1, local)
        gene1 = GenetetA(cw_channel_2, supercoil_1.supercoiling_region, local)
        supercoil_2 = Supercoil(cw_channel_2, acw_channel_2, local)
        circuit = [gene1, supercoil_2]
        self.assertEqual(0, supercoil_2.get_coil_state(), "Incorrect coiling state at start")
        supercoil_2.update()
        self.assertEqual(0, supercoil_2.get_coil_state(), "Coiling updating incorrectly.")
        threads = [Thread(target=x.update) for x in circuit]
        [x.start() for x in threads]
        [x.join() for x in threads]
        self.assertEqual(-1, supercoil_2.get_coil_state(), "Did not update region")
