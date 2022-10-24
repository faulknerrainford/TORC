from unittest import TestCase
from TORC import GenetetA, Supercoil, Channel, SignalError
from threading import Thread


class TestSupercoil(TestCase):

    def test_get_coil_state(self):
        sc_channel, _ = Channel()
        supercoil = Supercoil(sc_channel)
        self.assertEqual(Supercoil.region_list[supercoil.supercoiling_region], supercoil.get_coil_state(),
                         "Incorrect coiling state")
        supercoil.region_list[supercoil.supercoiling_region] = "Test"
        self.assertEqual(supercoil.get_coil_state(), "Test", "Incorrect test state")

    def test_coil(self):
        sc_channel_1, _ = Channel()
        sc_channel_2, gene_channel = Channel()
        supercoil_1 = Supercoil(sc_channel_1)
        gene = GenetetA(gene_channel, supercoil_1.supercoiling_region)
        supercoil_2 = Supercoil(sc_channel_2)
        self.assertEqual("neutral", supercoil_2.get_coil_state(), "Incorrect coil state at start")
        circuit = [supercoil_2, gene]
        with self.assertRaises(SignalError, msg="Listened with no signal"):
            supercoil_2.coil()
        try:
            threads = [Thread(target=supercoil_2.coil), Thread(target=gene.output_signal)]
            [x.start() for x in threads]
            [x.join() for x in threads]
        except SignalError:
            self.fail("Failed to listen with signal")
        self.assertEqual("negative", supercoil_2.get_coil_state(), "Incorrect coil state after update")

    # def test_region_update(self):
    #     self.fail()
    #
    # def test_get_coil_state(self):
    #     self.fail()

    def test_update(self):
        sc_channel_1, _ = Channel()
        sc_channel_2, gene_channel = Channel()
        supercoil_1 = Supercoil(sc_channel_1)
        gene = GenetetA(gene_channel, supercoil_1.supercoiling_region)
        supercoil_2 = Supercoil(sc_channel_2)
        circuit = [gene, supercoil_2]
        self.assertEqual("neutral", supercoil_2.get_coil_state(), "Incorrect coiling state at start")
        supercoil_2.update()
        self.assertEqual("neutral", supercoil_2.get_coil_state(), "Coiling updating incorrectly.")
        threads = [Thread(target=x.update) for x in circuit]
        [x.start() for x in threads]
        [x.join() for x in threads]
        self.assertEqual("negative", supercoil_2.get_coil_state(), "Did not update region")
