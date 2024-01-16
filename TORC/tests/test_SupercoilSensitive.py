from unittest import TestCase
from TORC import GenetetA, SignalError, Supercoil, Channel, SupercoilSensitive, LocalArea
from queue import Queue
from threading import Thread


class TestSupercoilSensitive(TestCase):

    def test_update_sequential(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = SupercoilSensitive("red", supercoil.supercoiling_region, local, output_channel=test_out_queue)
        promoter.update()
        self.assertEqual(0, promoter.coil_state, "coil state incorrect")
        self.assertEqual(0, promoter.output_channel.get(), "Incorrect weak signal")
        local.set_supercoil(supercoil.supercoiling_region, -1)
        promoter.update()
        self.assertEqual(-1, promoter.coil_state, "coil state updated failed")
        self.assertEqual(1, promoter.output_channel.get(), "Incorrect strong signal")

    def test_update_concurrent(self):
        local = LocalArea()
        cw_channel_1 = Queue()
        acw_channel_1 = Queue()
        supercoil_1 = Supercoil(cw_channel_1, acw_channel_1, local)
        cw_channel_2 = Queue()
        acw_channel_2 = Queue()
        supercoil_2 = Supercoil(cw_channel_2, acw_channel_2, local)
        gene = GenetetA(cw_channel_2, supercoil_1.supercoiling_region, local)
        test_out_queue = Queue()
        promoter = SupercoilSensitive("blue", supercoil_2.supercoiling_region, local, output_channel=test_out_queue)
        circuit = [supercoil_2, gene, promoter]
        promoter.update()
        self.assertEqual(0, promoter.coil_state, "coil state incorrect")
        self.assertEqual(0, test_out_queue.get(), "Incorrect weak signal")
        for i in range(2):
            try:
                threads = [Thread(target=x.update) for x in circuit]
                [x.start() for x in threads]
                [x.join() for x in threads]
            except SignalError:
                self.fail("Update failed for supercoiling, gene and promoter")
        self.assertEqual(-1, promoter.coil_state, "coil state update failed")
        test_out_queue.get()
        self.assertEqual(1, test_out_queue.get(), "Incorrect strong signal")

    def test_input_check(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        ss_promoter = SupercoilSensitive("green", supercoil.supercoiling_region, local, output_channel=test_out_queue)
        self.assertEqual(0, ss_promoter.coil_state, "coil state incorrect")
        self.assertFalse(ss_promoter.input_check(), "Incorrect check with neutral coil state.")
        local.set_supercoil(supercoil.supercoiling_region, -1)
        ss_promoter.state_update()
        self.assertEqual(-1, ss_promoter.coil_state, "coil state update failed")
        self.assertTrue(ss_promoter.input_check(), "Incorrect check with negative coil state.")
