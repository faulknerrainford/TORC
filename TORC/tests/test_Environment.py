from unittest import TestCase
from TORC import Promoter, Supercoil, Environment, SignalError, Channel, LocalArea, Inhibitor
from queue import Queue
from threading import Thread


class TestEnvironment(TestCase):
    def test_read_signal_no_decay(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_in_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, local, output_channel=test_in_queue)
        environment = Environment("leu500", local, input_queue=test_in_queue)
        promoter.output_signal("strong")
        promoter.output_signal("strong")
        content = environment.content
        environment.read_signal()
        self.assertEqual(content+(promoter.strong_signal*2), environment.content,
                         "Incorrect read from queue of input signal")
        self.assertTrue(test_in_queue.empty(), "Queue not cleared after read")

    def test_read_signal_decay(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_in_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, local, output_channel=test_in_queue)
        environment = Environment("leu500", local, decay_rate=0.5, input_queue=test_in_queue)
        promoter.output_signal("strong")
        promoter.output_signal("strong")
        content = environment.content
        environment.read_signal()
        self.assertEqual(content+(promoter.strong_signal*2)-0.5, environment.content,
                         "Incorrect application of decay")

    def test_read_signal_negative_decay(self):
        local = LocalArea()
        test_in_queue = Queue()
        environment = Environment("leu500", local, decay_rate=0.5, input_queue=test_in_queue)
        environment.read_signal()
        self.assertGreaterEqual(environment.content, 0, "Negative environment content")

    def test_send_signal(self):
        local = LocalArea()
        environment = Environment("leu500", local, content=20)
        environment.send_signal()
        self.assertEqual(environment.content, local.get_environment(environment.label),
                         "Incorrect output signal sent")
        environment.content = 42
        environment.send_signal()
        self.assertEqual(42, local.get_environment(environment.label), "Incorrect update of signal")

    def test_inhibit(self):
        local = LocalArea()
        inhibitor = Inhibitor()
        environmentA = Environment("A", local, content=20, inhibitors=[inhibitor])
        environmentB = Environment("B", local, content=3, inhibitors=[inhibitor])
        try:
            threads = [Thread(target=x.inhibit) for x in [environmentB, environmentA]]
            [x.start() for x in threads]
            [x.join() for x in threads]
        except SignalError:
            self.fail("Inhibit failed")
        self.assertEqual(17, environmentA.content, "Failed inhibit A")
        self.assertEqual(0, environmentB.content, "Failed inhibit B")

    def test_update_sequential(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_in_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, local, output_channel=test_in_queue)
        environment = Environment("leu500", local, input_queue=test_in_queue)
        self.assertEqual(0, environment.content, "Content in initial environment")
        promoter.output_signal("strong")
        environment.update()
        self.assertEqual(1, environment.content, "Incorrect sequential update of content")

    def test_update_concurrent(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_in_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, local, output_channel=test_in_queue)
        environment = Environment("leu500", local, content=12, input_queue=test_in_queue)
        self.assertEqual(12, environment.content, "Incorrect initial content")
        local.set_supercoil(supercoil.supercoiling_region, "negative")
        circuit = [promoter, environment]
        for i in range(1):
            try:
                threads = [Thread(target=x.update) for x in circuit]
                [x.start() for x in threads]
                [x.join() for x in threads]
            except SignalError:
                self.fail("Update failed for supercoiling, gene and promoter")
        self.assertEqual(12, environment.content, "Incorrect concurrent update of content")

    def test_update_concurrent_inhibitor(self):
        local = LocalArea()
        test_queue = Queue()
        inh_queue = Queue()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        test_in_queue = Queue()
        inhibitor = Inhibitor()
        inhibit_env = Environment("Inh", local, content=2, input_queue=inh_queue, inhibitors=[inhibitor])
        promoter = Promoter("leu500", supercoil.supercoiling_region, local, output_channel=test_in_queue)
        environment = Environment("leu500", local, content=12, input_queue=test_in_queue, inhibitors=[inhibitor])
        self.assertEqual(12, environment.content, "Incorrect initial content")
        local.set_supercoil(supercoil.supercoiling_region, "negative")
        circuit = [promoter, environment, inhibit_env]
        for i in range(1):
            try:
                threads = [Thread(target=x.update) for x in circuit]
                [x.start() for x in threads]
                [x.join() for x in threads]
            except SignalError:
                self.fail("Update failed for supercoiling, gene and promoter")
        self.assertEqual(10, environment.content, "Incorrect concurrent update of content")
        self.assertEqual(0, inhibit_env.content, "Did not empty inhibitor")
