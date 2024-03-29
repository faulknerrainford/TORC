from unittest import TestCase
from TORC import Circuit, BridgeError
from queue import Queue
# from threading import Thread


class TestCircuit(TestCase):

    def test_setup(self):
        circuit = Circuit([("tetA"), ("CF", "red"), ("bridge", "lac"), ("CF", "blue"), ("bridge", "lac")],
                          environments=[("lac", 0)])
        circuit.setup()
        # check correct number of supercoil regions
        self.assertEqual(4, len(circuit.local.supercoil_regions), "Incorrect number of supercoiling regions created")
        # check correct environments
        self.assertEqual(sorted(["lac", "red", "blue"]), sorted(circuit.local.get_keys()),
                         "Incorrect Environment setup")
        self.assertEqual(13, len(circuit.circuit_components), "Incorrect component list")

    def test_run(self):
        circuit0 = Circuit([("tetA"), ("CF", "red"), ("bridge", "lac"), ("CF", "blue"), ("bridge", "lac")],
                           environments=[("lac", 0)])
        circuit0.setup()
        circuit0.run(10)
        # check visible correct
        self.assertEqual("magenta", circuit0.visible.colour, "Incorrect output colour, no lac")
        circuit20 = Circuit([("tetA"), ("CF", "red"), ("bridge", "lac"), ("CF", "blue"), ("bridge", "lac")],
                            environments=[("lac", 20)])
        circuit20.setup()
        circuit20.run(10)
        # check correct environments and visible correct
        self.assertEqual("red", circuit20.visible.colour, "Incorrect output colour, with lac")

    def test_create_supercoil(self):
        circuit = Circuit([])
        regions_before = len(circuit.local.supercoil_regions)
        sc, coil, ind = circuit.create_supercoil()
        self.assertEqual(regions_before+1, len(circuit.local.supercoil_regions), "Supercoil list not expanded")
        self.assertEqual(sc.supercoiling_region, ind, "Incorrect index returned")

    def test_create_gene(self):
        circuit = Circuit([])
        components, coil, ind = circuit.create_gene("tetA")
        self.assertEqual(ind, components[1].supercoiling_region, "Incorrect current region")
        self.assertEqual("tetA", components[0].label, "Incorrect components returned")
        self.assertFalse(circuit.create_gene("abc"), "Generating gene from garbage label")

    def test_create_environment(self):
        circuit = Circuit([])
        queue = Queue()
        env = circuit.create_environment("test", queue)
        self.assertIn(env.label, circuit.local.get_keys(), "Environment not added")
        self.assertEqual(0.0, circuit.local.get_environment(env.label), "Environment content not correctly initialised")
        env = circuit.create_environment("content", queue, 10)
        self.assertEqual(env.content, circuit.local.get_environment("content"), "Incorrect initial content")

    def test_create_promoter(self):
        # test base promoter setup
        circuit = Circuit([])
        components = circuit.create_promoter("P", "lac", 0)
        self.assertEqual(len(components), 2, "Incorrect number of components returned, promoter")
        # test supercoil sensitive setup
        components = circuit.create_promoter("C", "lac", 0)
        self.assertEqual(len(components), 1, "Incorrect number of components returned, sc sensitive")
        # test CF setup
        components = circuit.create_promoter("CF", "red", 0)
        self.assertEqual(len(components), 2, "Incorrect number of components returned, fluorescent")

    def test_create_barrier(self):
        # create bridge
        circuit = Circuit([])
        components, coil, sc_ind = circuit.create_barrier("bridge", "lac", 0)
        # check creation of env
        self.assertIn("lac", circuit.local.get_keys(), "lac environ not created")
        # check bridge has correct label
        self.assertEqual("lac", components[2].label, "Incorrect bridge created")

    def test_create_visible(self):
        circuit = Circuit([])
        viz = circuit.create_visible()
        self.assertEqual("visible", viz.label, "Incorrect component returned")
        viz.check_colour()
        self.assertEqual(viz.colour, "black", "Incorrect colour return")

    def test_pair_bridges(self):
        circuit1 = Circuit([("bridge", "lac"), ("bridge", "topo")])
        circuit1.circuit_components = circuit1.circuit_components + circuit1.create_barrier("bridge", "lac", 0)[0]
        with self.assertRaises(BridgeError, msg="Paired with only one point"):
            circuit1.pair_bridges()
        circuit1.circuit_components = circuit1.circuit_components + circuit1.create_barrier("bridge", "topo", 1)[0]
        with self.assertRaises(BridgeError, msg="Paired with incorrect labelling"):
            circuit1.pair_bridges()
        circuit2 = Circuit([("bridge", "lac"), ("bridge", "lac")])
        circuit2.circuit_components = circuit2.circuit_components + circuit2.create_barrier("bridge", "lac", 0)[0]
        circuit2.circuit_components = circuit2.circuit_components + circuit2.create_barrier("bridge", "lac", 1)[0]
        circuit2.pair_bridges()
        self.assertEqual(circuit2.circuit_components[2],circuit2.circuit_components[4].bridge_check,
                         "First bridge end not set")
        self.assertEqual(circuit2.circuit_components[4],circuit2.circuit_components[2].bridge_check,
                         "Second bridge end not set")
