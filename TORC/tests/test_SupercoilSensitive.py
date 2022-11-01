from unittest import TestCase
from TORC import GenetetA, SignalError, Supercoil, Channel, SupercoilSensitive, LocalArea
from queue import Queue
from threading import Thread


class TestSupercoilSensitive(TestCase):

    def test_update_sequential(self):
        local = LocalArea()
        sc_channel, _ = Channel()
        supercoil = Supercoil(sc_channel, local)
        test_out_queue = Queue()
        promoter = SupercoilSensitive("red", supercoil.supercoiling_region, local, output_channel=test_out_queue)
        promoter.update()
        self.assertEqual("neutral", promoter.coil_state, "coil state incorrect")
        self.assertEqual(0, promoter.output_channel.get(), "Incorrect weak signal")
        local.set_supercoil(supercoil.supercoiling_region, "negative")
        promoter.update()
        self.assertEqual("negative", promoter.coil_state, "coil state updated failed")
        self.assertEqual(1, promoter.output_channel.get(), "Incorrect strong signal")

    def test_update_concurrent(self):
        local = LocalArea()
        sc_channel_1, _ = Channel()
        supercoil_1 = Supercoil(sc_channel_1, local)
        sc_channel_2, gene_channel = Channel()
        gene = GenetetA(gene_channel, supercoil_1.supercoiling_region, local)
        supercoil_2 = Supercoil(sc_channel_2, local)
        test_out_queue = Queue()
        promoter = SupercoilSensitive("blue", supercoil_2.supercoiling_region, local, output_channel=test_out_queue)
        circuit = [supercoil_2, gene, promoter]
        promoter.update()
        self.assertEqual("neutral", promoter.coil_state, "coil state incorrect")
        self.assertEqual(0, test_out_queue.get(), "Incorrect weak signal")
        for i in range(2):
            try:
                threads = [Thread(target=x.update) for x in circuit]
                [x.start() for x in threads]
                [x.join() for x in threads]
            except SignalError:
                self.fail("Update failed for supercoiling, gene and promoter")
        self.assertEqual("negative", promoter.coil_state, "coil state update failed")
        self.assertEqual(1, test_out_queue.get(), "Incorrect strong signal")

    def test_input_check(self):
        local = LocalArea()
        sc_channel, _ = Channel()
        supercoil = Supercoil(sc_channel, local)
        test_out_queue = Queue()
        ss_promoter = SupercoilSensitive("green", supercoil.supercoiling_region, local, output_channel=test_out_queue)
        self.assertEqual("neutral", ss_promoter.coil_state, "coil state incorrect")
        self.assertFalse(ss_promoter.input_check(), "Incorrect check with neutral coil state.")
        local.set_supercoil(supercoil.supercoiling_region, "negative")
        ss_promoter.input_check()
        self.assertEqual("negative", ss_promoter.coil_state, "coil state update failed")
        self.assertTrue(ss_promoter.input_check(), "Incorrect check with negative coil state.")
