from unittest import TestCase
from TORC import Environment, Bridge, Supercoil, SendingError, SignalError, ReceivingError, Channel
from threading import Thread


class TestBridge(TestCase):

    def test_set_bridge_check(self):
        bridge_cw = Bridge("lac")
        self.assertEqual(None, bridge_cw.bridge_check, "Bridge end initialised with end")
        bridge_acw = Bridge("lac")
        bridge_cw.set_bridge_check(bridge_acw)
        self.assertEqual(bridge_acw, bridge_cw.bridge_check, "Bridge end incorrectly updated")

    def test_check_state(self):
        # Create an environment and two bridges
        Environment.environment_dictionary["lac"] = 0
        bridge_cw = Bridge("lac")
        bridge_acw = Bridge("lac")
        # Run check state and get false
        self.assertFalse(bridge_cw.check_state(), "Bridge without end closed")
        self.assertFalse(bridge_acw.check_state(), "Bridge without start closed")
        # Set bridge checks
        bridge_acw.set_bridge_check(bridge_cw)
        bridge_cw.set_bridge_check(bridge_acw)
        # Run check state with environment empty and get false
        self.assertFalse(bridge_cw.check_state(), "Connected bridge with empty environment closed")
        # Run check state with environment full and get true
        Environment.environment_dictionary["lac"] = 20
        self.assertTrue(bridge_cw.check_state(), "Connected bridge with full environment open")
        # Reset bridges and without check but with full environment get false
        bridge_cw.bridge_check = None
        self.assertFalse(bridge_cw.check_state(), "Unconnected bridge with full environment closed")

    def test_coil_in(self):
        # Create the bridge
        bridge = Bridge("lac")
        Supercoil.region_list.append("neutral")
        # Check coil in get neutral
        self.assertEqual(Supercoil.region_list[0], bridge.coil_in(), "Read from region list incorrect")
        # Modify coiling region state
        Supercoil.region_list[0] = "test"
        # Check coil in get new value
        self.assertEqual("test", bridge.coil_in(), "Incorrect read from updated region list")
        Supercoil.region_list = []

    def test_coil_out(self):
        Supercoil.region_list = []
        Supercoil.super_coil_index = 0
        # Create queue
        sc_channel, bridge_channel = Channel()
        # Create bridge
        bridge_cw = Bridge("lac", channel= bridge_channel)
        # Run coil out and get false
        with self.assertRaises(SignalError, msg="Sending with no signal"):
            bridge_cw.coil_out("test")
        # Create supercoil region
        supercoil = Supercoil(sc_channel)
        # Run coil_out and supercoil coil concurrently and not get error
        try:
            threads = [Thread(target=bridge_cw.coil_out, args=("test",)), Thread(target=supercoil.coil)]
            [x.start() for x in threads]
            [x.join() for x in threads]
        except [SendingError, ReceivingError]:
            self.fail("Signalling failed")
        # check correct update of supercoil region
        self.assertEqual("test", Supercoil.region_list[supercoil.supercoiling_region],
                         "Incorrect supercoiling state transmitted")

    def test_update(self):
        Supercoil.region_list = []
        Supercoil.super_coil_index = 0
        # Test result of run with relevant other components with full and empty environment.
        Environment.environment_dictionary["lac"] = 20
        test_sc, test_bridge = Channel()
        bridge_cw = Bridge("lac")
        bridge_acw = Bridge("lac", 0, 1, channel=test_bridge)
        bridge_acw.set_bridge_check(bridge_cw)
        bridge_cw.set_bridge_check(bridge_acw)
        sc_channel, _ = Channel()
        supercoil1 = Supercoil(sc_channel)
        Supercoil.region_list[supercoil1.supercoiling_region] = "negative"
        supercoil2 = Supercoil(test_sc)
        circuit = [supercoil1, bridge_acw, supercoil2]
        self.assertEqual("neutral", supercoil2.get_coil_state(), "Incorrect coiling state at start")
        threads = [Thread(target=x.update) for x in circuit]
        [x.start() for x in threads]
        [x.join() for x in threads]
        self.assertEqual("neutral", supercoil2.get_coil_state(), "Updated supercoiling with full environment")
        Environment.environment_dictionary["lac"] = 0
        threads = [Thread(target=x.update) for x in circuit]
        [x.start() for x in threads]
        [x.join() for x in threads]
        self.assertEqual("negative", supercoil2.get_coil_state(), "Updated supercoiling with empty environment failed")
