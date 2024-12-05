from unittest import TestCase
from TORC import GenetetA, SignalError, Supercoil, Promoter, LocalArea, Environment, Barrier
from queue import Queue
from threading import Thread


class TestPromoter(TestCase):

    def test_update_sequential(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, local, output_channel=test_out_queue)
        promoter.update()
        self.assertEqual(0, promoter.coil_state, "coil state incorrect")
        local.set_supercoil(supercoil.supercoiling_region, -1)
        promoter.update()
        self.assertEqual(-1, promoter.coil_state, "coil state updated failed")

    def test_update_concurrent(self):
        local = LocalArea()
        cw_channel_1 = Queue()
        acw_channel_1 = Queue()
        supercoil_1 = Supercoil(cw_channel_1, acw_channel_1, local)
        cw_channel_2 = Queue()
        acw_channel_2 = Queue()
        supercoil_2 = Supercoil(cw_channel_2, acw_channel_2, local)
        gene = GenetetA(cw_channel_2, supercoil_2, supercoil_1, local)
        test_out_queue = Queue()
        promoter = Promoter("leu500", supercoil_2.supercoiling_region, local, output_channel=test_out_queue)
        circuit = [supercoil_2, gene, promoter]
        promoter.update()
        self.assertEqual(0, promoter.coil_state, "coil state incorrect")
        for i in range(2):
            try:
                threads = [Thread(target=x.update) for x in circuit]
                [x.start() for x in threads]
                [x.join() for x in threads]
            except SignalError:
                self.fail("Update failed for supercoiling, gene and promoter")
        self.assertEqual(-1, promoter.coil_state, "coil state update failed")

    def test_input_check_sc_sensitive(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, local, output_channel=test_out_queue)
        promoter.input_check()
        self.assertEqual(0, promoter.coil_state, "coil state incorrect")
        # local.set_supercoil(supercoil.supercoiling_region, -1)
        supercoil.cw_sc = -1
        supercoil.coil()
        promoter.state_update()
        ret = promoter.input_check()
        self.assertEqual(-1, promoter.coil_state, "coil state update failed")
        self.assertEqual(-1, ret["supercoiling"], "sc sensitive promoter check failed")

    def test_input_check_protein_promoted(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                            promote="protein", sc_sensitive=False)
        Environment("protein", local, content=10)
        ret = promoter.input_check()
        self.assertEqual(10, ret["promote"], "protein promoter check failed")

    def test_input_check_repressed(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                            promote="protein", repress="repressor", sc_sensitive=False)
        repressor = Environment("repressor", local, content=10)
        Environment("protein", local, content=10)
        ret = promoter.input_check()
        self.assertEqual(10, ret["repress"], "repressor check failed with content")
        repressor.content = 0
        repressor.send_signal()
        ret = promoter.input_check()
        self.assertEqual(0, ret["repress"], "repressor check failed without content")

    def test_output_signal(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                            fluorescent=True)
        promoter.output_signal(0)
        self.assertEqual(0, promoter.output_channel.get(), "Incorrect weak signal")
        promoter.output_signal(1)
        self.assertEqual(1, promoter.output_channel.get(), "Incorrect strong signal")

    def test_output_supercoiling(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                            fluorescent=True, sc_rate=3)
        promoter.output_signal(1)
        supercoil.coil()
        self.assertEqual(3, supercoil.cw_sc, "Incorrect local supercoiling after transcription")
        self.assertEqual(-3, supercoil.acw_sc, "Incorrect local supercoiling after transcription")

    def test_promoter_inversion_supercoiling(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                            fluorescent=True, sc_rate=3, clockwise=False)
        promoter.output_signal(1)
        supercoil.coil()
        self.assertEqual(3, supercoil.acw_sc, "Incorrect local supercoiling after transcription")
        self.assertEqual(-3, supercoil.cw_sc, "Incorrect local supercoiling after transcription")

    def test_rate_calc_threshold(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                            rate_dist="threshold", threshold=0.5, sc_sensitive=False)
        self.assertEqual(0, promoter.rate_calc({"promote": 0.2}), "Incorrect for below threshold")
        self.assertEqual(1, promoter.rate_calc({"promote": 0.8}), "Incorrect for above threshold")
        self.assertEqual(0, promoter.rate_calc({"promote": 0.5}), "Incorrect at threshold")

    def test_rate_calc_sigmoid(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                            rate_dist="sigmoid", threshold=0.5, sc_sensitive=False)
        self.assertLess(promoter.rate_calc({"promote": 0}), 0.5, "Incorrect for below threshold, sigmoid")
        self.assertGreater(promoter.rate_calc({"promote": 1}), 0.5, "Incorrect for above threshold, sigmoid")
        self.assertEqual(promoter.rate_calc({"promote": 0.5}), 0.5, "Incorrect for at threshold, sigmoid")

    def test_rate_calc_normal(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_out_queue = Queue()
        promoter = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                            rate_dist="normal", threshold=0.5, sc_sensitive=False)
        self.assertLess(promoter.rate_calc({"promote": 0}), 1, "Incorrect for below mean, normal")
        self.assertLess(promoter.rate_calc({"promote": 1}), 1, "Incorrect for above mean, normal")
        # noinspection PyTypeChecker
        self.assertAlmostEqual(1, promoter.rate_calc({"promote": 0.5}), 1,
                               "Incorrect for at mean, normal")
        promoter = Promoter("red", supercoil.supercoiling_region, local, weak=0.2, strong=0.8,
                            output_channel=test_out_queue, rate_dist="normal", threshold=0.5, sc_sensitive=False)
        self.assertLess(promoter.rate_calc({"promote": 0}), 0.8, "Incorrect for below mean, scaled normal")
        self.assertLess(promoter.rate_calc({"promote": 1}), 0.8, "Incorrect for above mean, scaled normal")
        self.assertAlmostEqual(0.8, promoter.rate_calc({"promote": 0.5}), 2, "Incorrect for at mean, scaled normal")

    def test_read_through_setup(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        test_out_queue = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        promoter = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                            rate_dist="normal", threshold=0.5, sc_sensitive=True, terminator=False)
        self.assertIsInstance(promoter.output_read_through, Queue, "No output_read_through queue made")

    def test_add_read_through_check(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        test_out_queue = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        barrier = Barrier(local, supercoil, supercoil, "Lac")
        promoterA = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                             rate_dist="normal", threshold=0.5, sc_sensitive=True, terminator=False)
        promoterB = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                             rate_dist="normal", threshold=0.5, sc_sensitive=True, terminator=False)
        promoterC = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                             rate_dist="normal", threshold=0.5, sc_sensitive=True, terminator=True)
        promoterB.add_read_through_check(promoterC)
        self.assertIsNone(promoterB.input_read_through, "read through queue acquired from terminated promoter")
        promoterB.add_read_through_check(promoterA, [barrier])
        self.assertIsNotNone(promoterB.input_read_through, "No input_read_through channel picked up")
        self.assertIsInstance(promoterB.input_read_through, Queue, "Incorrect input_read_through, must be queue")
        self.assertEqual(promoterB.input_read_through, promoterA.output_read_through, "Incorrect queue acquired")
        self.assertIsInstance(promoterB.read_through_barriers, list, "Barriers not added")

    def test_read_though_output(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        test_out_queue = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        promoterA = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                             rate_dist="normal", threshold=0.5, sc_sensitive=True, terminator=False)
        promoterA.output_signal(1)
        # check queue
        self.assertIsNotNone(promoterA.output_read_through.get(), "No read_through_output sent")
        promoterA.output_signal(0)
        self.assertTrue(promoterA.output_read_through.empty(), "read_through_output sent with no output")
        promoterA.terminator = True
        promoterA.output_signal(1)
        self.assertTrue(promoterA.output_read_through.empty(), "Read through output sent from terminated promoter")

    def test_read_through_check(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        test_out_queue = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        promoterA = Promoter("red", supercoil.supercoiling_region, local, output_channel=test_out_queue,
                             rate_dist="normal", threshold=0.5, sc_sensitive=True, terminator=False)
        promoterB = Promoter("red", supercoil.supercoiling_region, local,
                             output_channel=test_out_queue, rate_dist="normal", threshold=0.5, sc_sensitive=True,
                             terminator=False)
        barrier = Barrier(local, supercoil, supercoil, "Lac")
        local.barriers[barrier.label] = False
        promoterB.add_read_through_check(promoterA, [barrier.label])
        status = promoterB.input_check()
        self.assertNotIn("read_through", status.keys(), "Read through status set with no input from queue")
        promoterB.input_read_through.put(1)
        status = promoterB.input_check()
        self.assertTrue(status["read_through"], "Incorrect read through status with input and no barriers")
        # check for active barrier
        local.barriers[barrier.label] = True
        promoterB.input_read_through.put(1)
        status = promoterB.input_check()
        self.assertNotIn("read_through", status.keys(), "Read through status set with barriers")
        # check queue cleared
        self.assertTrue(promoterB.input_read_through.empty(), "Read through queue not cleared with barrier")
        # check for repression working
        local.barriers[barrier.label] = False
        promoterB.repress = "red"
        local.environments["red"] = 1
        promoterB.input_read_through.put(1)
        status = promoterB.input_check()
        self.assertNotIn("read_through", status.keys(), "Read through status set with repression")
        self.assertTrue(promoterB.input_read_through.empty(), "Read through queue not cleared with repression")
