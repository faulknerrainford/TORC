from unittest import TestCase
from TORC import Channel, SendingError, ReceivingError
from threading import Thread


class TestChannelEnd(TestCase):
    def test_Channel(self):
        channel_a, channel_b = Channel()
        self.assertEqual(channel_a.event, channel_b.event, msg="Events don't match")

    def test_send(self):
        channel_a, channel_b = Channel()
        with self.assertRaises(SendingError, msg="Sending without receipt"):
            channel_a.send("test")
        processes = [Thread(target=channel_a.send, args=tuple(["test"])), Thread(target=channel_b.recv)]
        try:
            [x.start() for x in processes]
            [x.join() for x in processes]
        except SendingError:
            self.fail("Did not send message")
        except ReceivingError:
            pass

    def test_recv(self):
        channel_a, channel_b = Channel()
        with self.assertRaises(ReceivingError, msg="Receiving without send"):
            channel_b.recv()
        processes = [Thread(target=channel_a.send, args=tuple(["test"])), Thread(target=channel_b.recv)]
        try:
            [x.start() for x in processes]
            [x.join() for x in processes]
        except ReceivingError:
            self.fail("Did not receive message")
        except SendingError:
            pass
