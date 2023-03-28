from unittest import TestCase
from TORC import Inhibitor


class TestInhibitor(TestCase):
    def test_send(self):
        inh = Inhibitor()
        inh.send(10)
        self.assertEqual([10], inh.list, "Not adding to list correctly")
        inh.send(2)
        self.assertEqual([], inh.list, "List not emptied")
        ret = inh.queue.get()
        inh.queue.get()
        self.assertEqual(2, ret, "Incorrect value picked")
        inh.send(10)
        inh.send(6)
        ret = inh.queue.get()
        self.assertEqual(4, ret, "Incorrect value picked")

    def test_get(self):
        inh = Inhibitor()
        inh.queue.put(10)
        inh.queue.put(3)
        self.assertEqual(10, inh.get(), "Incorrect first value retrieved")
        self.assertEqual(3, inh.get(), "Incorrect second value retrieved")
