from unittest import TestCase
from TORC import Circuit, BridgeError, Supercoil
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
        self.assertEqual([1.0, 0.0, 0.875], circuit0.visible.rgb, "Incorrect output colour, no lac")
        circuit20 = Circuit([("tetA"), ("CF", "red"), ("bridge", "lac"), ("CF", "blue"), ("bridge", "lac")],
                            environments=[("lac", 20)])
        circuit20.setup()
        circuit20.run(10)
        # check correct environments and visible correct
        self.assertEqual(0, circuit20.visible.rgb[2], "Incorrect output colour, with lac")

    def test_create_supercoil(self):
        circuit = Circuit([])
        regions_before = len(circuit.local.supercoil_regions)
        sc, cw, acw, ind = circuit.create_supercoil()
        self.assertEqual(regions_before + 1, len(circuit.local.supercoil_regions), "Supercoil list not expanded")
        self.assertEqual(sc.supercoiling_region, ind, "Incorrect index returned")

    def test_create_gene(self):
        circuit = Circuit([])
        test_cw = Queue()
        test_acw = Queue()
        supercoil0 = Supercoil(test_cw, test_acw, circuit.local)
        components, cw, acw, ind = circuit.create_gene("tetA", supercoil0)
        self.assertEqual(ind, components[1].supercoiling_region, "Incorrect current region")
        self.assertEqual("tetA", components[0].label, "Incorrect components returned")
        self.assertFalse(circuit.create_gene("abc", supercoil0), "Generating gene from garbage label")

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

    def test_create_barrier_bridge(self):
        # create bridge
        circuit = Circuit([])
        test_cw = Queue()
        test_acw = Queue()
        supercoil0 = Supercoil(test_cw, test_acw, circuit.local)
        components, cw, acw, sc_ind = circuit.create_barrier("bridge", "lac", supercoil0)
        # check creation of env
        self.assertIn("lac", circuit.local.get_keys(), "lac environ not created")
        # check bridge has correct label
        self.assertEqual("lac", components[2].label, "Incorrect bridge created")
        # check bridge has different regions
        self.assertNotEqual(components[2].cw_region, components[2].acw_region, "Bridge has only one region")

    def test_create_barrier_origin(self):
        # create origin
        circuit = Circuit([])
        sc, cw, acw, ind = circuit.create_supercoil()
        circuit.circuit_components.append(sc)
        component, cw, acw, sc_ind = circuit.create_barrier("origin", None, sc)
        self.assertEqual("Origin", component[0].label, "Incorrect label")
        self.assertEqual(1, len(circuit.local.supercoil_regions), "Incorrect sc region add")

    def test_create_visible(self):
        circuit = Circuit([])
        viz = circuit.create_visible()
        self.assertEqual("visible", viz.label, "Incorrect component returned")
        viz.check_colour()
        self.assertEqual(viz.colour, "black", "Incorrect colour return")

    def test_pair_bridges(self):
        circuit1 = Circuit([("bridge", "lac"), ("bridge", "topo")])
        sc, cw, acw, ind = circuit1.create_supercoil()
        # circuit1.local.add_supercoil(cw, acw)
        circuit1.circuit_components = circuit1.circuit_components + [sc]
        circuit1.circuit_components = circuit1.circuit_components + circuit1.create_barrier("bridge",
                                                                                            "lac", sc)[0]
        with self.assertRaises(BridgeError, msg="Paired with only one point"):
            circuit1.pair_bridges()
        current_sc = [x for x in circuit1.circuit_components if isinstance(x, Supercoil)
                      and x.supercoiling_region == 1][0]
        circuit1.circuit_components = circuit1.circuit_components + circuit1.create_barrier("bridge",
                                                                                            "topo", current_sc)[0]
        with self.assertRaises(BridgeError, msg="Paired with incorrect labelling"):
            circuit1.pair_bridges()
        circuit2 = Circuit([("bridge", "lac"), ("bridge", "lac")])
        current_sc = [x for x in circuit1.circuit_components if isinstance(x, Supercoil)
                      and x.supercoiling_region == 0][0]
        circuit2.circuit_components = circuit2.circuit_components + circuit2.create_barrier("bridge",
                                                                                            "lac", current_sc)[0]
        current_sc = [x for x in circuit1.circuit_components if isinstance(x, Supercoil)
                      and x.supercoiling_region == 1][0]
        circuit2.circuit_components = circuit2.circuit_components + circuit2.create_barrier("bridge",
                                                                                            "lac", current_sc)[0]
        circuit2.pair_bridges()
        self.assertEqual(circuit2.circuit_components[2], circuit2.circuit_components[4].bridge_check,
                         "First bridge end not set")
        self.assertEqual(circuit2.circuit_components[4], circuit2.circuit_components[2].bridge_check,
                         "Second bridge end not set")
