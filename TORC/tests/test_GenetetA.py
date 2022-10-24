from unittest import TestCase
from TORC import Supercoil, GenetetA, SignalError, Channel
from threading import Thread


class TestGenetetA(TestCase):

    def test_output_signal(self):
        _, supercoil_1_channel = Channel()
        gene_channel, supercoil_2_channel = Channel()
        supercoil_1 = Supercoil(supercoil_1_channel)
        supercoil_2 = Supercoil(supercoil_2_channel)
        gene = GenetetA(gene_channel, supercoil_1.supercoiling_region)
        with self.assertRaises(SignalError, msg="Signalled with no listener"):
            gene.output_signal()
        try:
            threads = [Thread(target=supercoil_2.coil), Thread(target=gene.output_signal)]
            [x.start() for x in threads]
            [x.join() for x in threads]
        except SignalError:
            self.fail("Failed to listen with signal")

    def test_update(self):
        _, supercoil_1_channel = Channel()
        gene_channel, supercoil_2_channel = Channel()
        supercoil_1 = Supercoil(supercoil_1_channel)
        supercoil_2 = Supercoil(supercoil_2_channel)
        gene = GenetetA(gene_channel, supercoil_1.supercoiling_region)
        threads = [Thread(target=gene.update), Thread(target=supercoil_2.update)]
        [x.start() for x in threads]
        [x.join() for x in threads]
        self.assertEqual("negative", Supercoil.region_list[supercoil_2.supercoiling_region], "Did not update region")

    # def test_transcribe(self):
    #     self.fail()
