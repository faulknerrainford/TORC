from unittest import TestCase
from TORC import Barrier, Supercoil, LocalArea
from queue import Queue
from threading import Thread


class TestBarrier(TestCase):
    def test_update(self):
        cw_1 = Queue()
        acw_1 = Queue()
        cw_2 = Queue()
        acw_2 = Queue()
        local = LocalArea()
        sc_1 = Supercoil(cw_1, acw_1, local)
        sc_2 = Supercoil(cw_2, acw_2, local)
        barrier = Barrier(local, sc_1, sc_2)
        circuit = [sc_1, sc_2, barrier]
        # set up sc on both regions
        cw_2.put(-2)
        acw_2.put(-3)
        cw_1.put(-1)
        acw_1.put(2)
        sc_1.coil()
        sc_2.coil()
        # check regional sc
        self.assertEqual(-5, local.get_supercoil(sc_2.supercoiling_region), "Incorrect starting regional supercoiling")
        self.assertEqual(1, local.get_supercoil(sc_1.supercoiling_region), "Incorrect starting regional supercoiling")
        # run update
        threads = [Thread(target=x.update) for x in circuit]
        [x.start() for x in threads]
        [x.join() for x in threads]
        # check regions directional sc levels
        self.assertEqual(-3, sc_2.acw_sc, "Incorrect acw region acw supercoiling")
        self.assertEqual(-2, sc_2.cw_sc, "Incorrect acw region cw supercoiling")
        self.assertEqual(2, sc_1.acw_sc, "Incorrect cw region acw supercoiling")
        self.assertEqual(-1, sc_1.cw_sc, "Incorrect cw region cw supercoiling")
        # check regions general sc levels
        self.assertEqual(1, local.get_supercoil(sc_1.supercoiling_region), "Incorrect regional supercoiling")
        self.assertEqual(-5, local.get_supercoil(sc_2.supercoiling_region), "Incorrect regional supercoiling")

    def test_barrier_check(self):
        cw_1 = Queue()
        acw_1 = Queue()
        cw_2 = Queue()
        acw_2 = Queue
        local = LocalArea()
        sc_1 = Supercoil(cw_1, acw_1, local)
        sc_2 = Supercoil(cw_2, acw_2, local)
        barrier = Barrier(local, sc_1, sc_2)
        self.assertEqual(False, barrier.barrier_check(), "Does not return default false response")

    def test_sc_exchange(self):
        cw_1 = Queue()
        acw_1 = Queue()
        cw_2 = Queue()
        acw_2 = Queue()
        local = LocalArea()
        sc_1 = Supercoil(cw_1, acw_1, local)
        sc_2 = Supercoil(cw_2, acw_2, local)
        barrier = Barrier(local, sc_1, sc_2)
        # set up sc on both regions
        cw_2.put(-2)
        acw_2.put(-3)
        cw_1.put(-1)
        acw_1.put(2)
        sc_1.coil()
        sc_2.coil()
        # check regional sc
        self.assertEqual(-5, local.get_supercoil(sc_2.supercoiling_region), "Incorrect starting regional supercoiling")
        self.assertEqual(1, local.get_supercoil(sc_1.supercoiling_region), "Incorrect starting regional supercoiling")
        # run exchange
        barrier.sc_exchange()
        sc_1.coil()
        sc_2.coil()
        # check regions directional sc levels
        self.assertEqual(-1, sc_2.acw_sc, "Incorrect acw region acw supercoiling")
        self.assertEqual(-2, sc_2.cw_sc, "Incorrect acw region cw supercoiling")
        self.assertEqual(2, sc_1.acw_sc, "Incorrect cw region acw supercoiling")
        self.assertEqual(-3, sc_1.cw_sc, "Incorrect cw region cw supercoiling")
        # check regions general sc levels
        self.assertEqual(-1, local.get_supercoil(sc_1.supercoiling_region), "Incorrect regional supercoiling")
        self.assertEqual(-3, local.get_supercoil(sc_2.supercoiling_region), "Incorrect regional supercoiling")
