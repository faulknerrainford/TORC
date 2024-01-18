from unittest import TestCase
from TORC import Environment, Bridge, Supercoil, SendingError, SignalError, ReceivingError, Channel, LocalArea
from threading import Thread
from queue import Queue


class TestBridge(TestCase):

    def test_set_bridge_check(self):
        local = LocalArea()
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        bridge_cw = Bridge("lac", local, acw_sc_region=supercoil, cw_sc_region=supercoil)
        self.assertEqual(None, bridge_cw.bridge_check, "Bridge end initialised with end")
        bridge_acw = Bridge("lac", local, acw_sc_region=supercoil, cw_sc_region=supercoil)
        bridge_cw.set_bridge_check(bridge_acw)
        self.assertEqual(bridge_acw, bridge_cw.bridge_check, "Bridge end incorrectly updated")

    def test_barrier_check(self):
        local = LocalArea()
        # Create an environment and two bridges
        local.add_environment("lac", 0)
        cw_channel = Queue()
        acw_channel = Queue()
        supercoil = Supercoil(cw_channel, acw_channel, local)
        bridge_cw = Bridge("lac", local, acw_sc_region=supercoil, cw_sc_region=supercoil)
        bridge_acw = Bridge("lac", local, acw_sc_region=supercoil, cw_sc_region=supercoil)
        # Run check state and get false
        self.assertTrue(bridge_cw.barrier_check(), "Bridge without end closed")
        self.assertTrue(bridge_acw.barrier_check(), "Bridge without start closed")
        # Set bridge checks
        bridge_acw.set_bridge_check(bridge_cw)
        bridge_cw.set_bridge_check(bridge_acw)
        # Run check state with environment empty and get false
        self.assertTrue(bridge_cw.barrier_check(), "Connected bridge with empty environment closed")
        # Run check state with environment full and get true
        local.set_environment("lac", 20)
        self.assertFalse(bridge_cw.barrier_check(), "Connected bridge with full environment open")
        # Reset bridges and without check but with full environment get false
        bridge_cw.bridge_check = None
        self.assertTrue(bridge_cw.barrier_check(), "Unconnected bridge with full environment closed")

    def test_update(self):
        local = LocalArea()
        cw_1 = Queue()
        acw_1 = Queue()
        sc_1 = Supercoil(cw_1, acw_1, local)
        cw_2 = Queue()
        acw_2 = Queue()
        sc_2 = Supercoil(cw_2, acw_2, local)
        cw_3 = Queue()
        acw_3 = Queue()
        sc_3 = Supercoil(cw_3, acw_3, local)
        bridge_cw = Bridge("lac", local, acw_sc_region=sc_1, cw_sc_region=sc_2)
        bridge_acw = Bridge("lac", local, acw_sc_region=sc_2, cw_sc_region=sc_3)
        # Test result of run with relevant other components with full and empty environment.
        local.add_environment("lac", 20)
        bridge_acw.set_bridge_check(bridge_cw)
        bridge_cw.set_bridge_check(bridge_acw)
        sc_1.cw_sc = -1
        circuit = [sc_1, bridge_acw, sc_2, sc_3, bridge_cw]
        self.assertEqual(0, sc_2.get_coil_state(), "Incorrect coiling state at start")
        threads = [Thread(target=x.update) for x in circuit]
        [x.start() for x in threads]
        [x.join() for x in threads]
        self.assertEqual(0, sc_2.get_coil_state(), "Updated supercoiling with full environment")
        local.set_environment("lac", 0)
        threads = [Thread(target=x.update) for x in circuit]
        [x.start() for x in threads]
        [x.join() for x in threads]
        threads = [Thread(target=x.update) for x in circuit]
        [x.start() for x in threads]
        [x.join() for x in threads]
        self.assertEqual(-1, sc_2.get_coil_state(), "Updated supercoiling with empty environment failed")
