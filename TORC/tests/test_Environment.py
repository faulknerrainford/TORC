from unittest import TestCase
from TORC import Promoter, Supercoil, Environment, SignalError, Channel
from queue import Queue
from threading import Thread


class TestEnvironment(TestCase):
    def test_read_signal_no_decay(self):
        sc_channel, _ = Channel()
        supercoil = Supercoil(sc_channel)
        test_in_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, output_channel=test_in_queue)
        environment = Environment("leu500", input_queue=test_in_queue)
        promoter.output_signal("strong")
        promoter.output_signal("strong")
        content = environment.content
        environment.read_signal()
        self.assertEqual(content+(promoter.strong_signal*2), environment.content,
                         "Incorrect read from queue of input signal")
        self.assertTrue(test_in_queue.empty(), "Queue not cleared after read")

    def test_read_signal_decay(self):
        sc_channel, _ = Channel()
        supercoil = Supercoil(sc_channel)
        test_in_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, output_channel=test_in_queue)
        environment = Environment("leu500", decay_rate=0.5, input_queue=test_in_queue)
        promoter.output_signal("strong")
        promoter.output_signal("strong")
        content = environment.content
        environment.read_signal()
        self.assertEqual(content+(promoter.strong_signal*2)-0.5, environment.content,
                         "Incorrect application of decay")

    def test_read_signal_negative_decay(self):
        test_in_queue = Queue()
        environment = Environment("leu500", decay_rate=0.5, input_queue=test_in_queue)
        environment.read_signal()
        self.assertGreaterEqual(environment.content, 0, "Negative environment content")

    def test_send_signal(self):
        environment = Environment("leu500", content=20)
        environment.send_signal()
        self.assertEqual(environment.content, Environment.environment_dictionary[environment.label],
                         "Incorrect output signal sent")
        environment.content = 42
        environment.send_signal()
        self.assertEqual(42, Environment.environment_dictionary[environment.label], "Incorrect update of signal")

    def test_update_sequential(self):
        sc_channel, _ = Channel()
        supercoil = Supercoil(sc_channel)
        test_in_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, output_channel=test_in_queue)
        environment = Environment("leu500", input_queue=test_in_queue)
        self.assertEqual(0, environment.content, "Content in initial environment")
        promoter.output_signal("strong")
        environment.update()
        self.assertEqual(1, environment.content, "Incorrect sequential update of content")

    def test_update_concurrent(self):
        test_queue = Queue()
        supercoil = Supercoil(test_queue)
        test_in_queue = Queue()
        promoter = Promoter("leu500", supercoil.supercoiling_region, output_channel=test_in_queue)
        environment = Environment("leu500", content=12, input_queue=test_in_queue)
        self.assertEqual(12, environment.content, "Incorrect initial content")
        Supercoil.region_list[supercoil.supercoiling_region] = "negative"
        circuit = [promoter, environment]
        for i in range(1):
            try:
                threads = [Thread(target=x.update) for x in circuit]
                [x.start() for x in threads]
                [x.join() for x in threads]
            except SignalError:
                self.fail("Update failed for supercoiling, gene and promoter")
        self.assertEqual(13, environment.content, "Incorrect concurrent update of content")
