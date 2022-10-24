from unittest import TestCase
from TORC import GenetetA, SignalError, Supercoil, Promoter, Channel
from queue import Queue
from threading import Thread


class TestPromoter(TestCase):

    def test_update_sequential(self):
        sc_channel, _ = Channel()
        supercoil = Supercoil(sc_channel)
        test_out_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, output_channel=test_out_queue)
        promoter.update()
        self.assertEqual("neutral", promoter.coil_state, "coil state incorrect")
        Supercoil.region_list[supercoil.supercoiling_region] = "negative"
        promoter.update()
        self.assertEqual("negative", promoter.coil_state, "coil state updated failed")

    def test_update_concurrent(self):
        sc_channel_1, _ = Channel()
        supercoil_1 = Supercoil(sc_channel_1)
        sc_channel_2, gene_channel = Channel()
        gene = GenetetA(gene_channel, supercoil_1.supercoiling_region)
        supercoil_2 = Supercoil(sc_channel_2)
        test_out_queue = Queue()
        promoter = Promoter("leu500", supercoil_2.supercoiling_region, output_channel=test_out_queue)
        circuit = [supercoil_2, gene, promoter]
        promoter.update()
        self.assertEqual("neutral", promoter.coil_state, "coil state incorrect")
        for i in range(2):
            try:
                threads = [Thread(target=x.update) for x in circuit]
                [x.start() for x in threads]
                [x.join() for x in threads]
            except SignalError:
                self.fail("Update failed for supercoiling, gene and promoter")
        self.assertEqual("negative", promoter.coil_state, "coil state update failed")

    def test_input_check(self):
        sc_channel, _ = Channel()
        supercoil = Supercoil(sc_channel)
        test_out_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, output_channel=test_out_queue)
        promoter.input_check()
        self.assertEqual("neutral", promoter.coil_state, "coil state incorrect")
        Supercoil.region_list[supercoil.supercoiling_region] = "negative"
        promoter.input_check()
        self.assertEqual("negative", promoter.coil_state, "coil state update failed")

    def test_output_signal(self):
        sc_channel, _ = Channel()
        supercoil = Supercoil(sc_channel)
        test_out_queue = Queue()
        promoter = Promoter("red", supercoil.supercoiling_region, output_channel=test_out_queue, fluorescent=True)
        promoter.output_signal("weak")
        self.assertEqual(0, promoter.output_channel.get(), "Incorrect weak signal")
        promoter.output_signal("strong")
        self.assertEqual(1, promoter.output_channel.get(), "Incorrect strong signal")
