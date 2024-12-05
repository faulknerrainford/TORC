from unittest import TestCase
from TORC import CircuitSetups as CS


class Test(TestCase):
    def test_rt_ll_circuit(self):
        self.fail()

    def test_rt_cr_circuit(self):
        self.fail()

    def test_rt_ll_cr_circuit(self):
        self.fail()

    def test_rt_circuit(self):
        # test that read through represses reporter and that read through is the cause
        # Include check that read through channel in action
        params = [-15, -1, 1, 0, 0, 0, 0, 0, 0]
        circuit = CS.RT_circuit(params)
        self.assertFalse(circuit.circuit_components[6].terminator, "read through not set")
        self.assertIsNotNone(circuit.circuit_components[6].output_read_through, "no output read through queue")
        self.assertIsNotNone(circuit.circuit_components[10].input_read_through, "no input read through")
        circuit.circuit_components[6].update()
        self.assertFalse(circuit.circuit_components[6].output_read_through.empty(),
                         "No read through signal generated")
        self.assertFalse(circuit.circuit_components[10].input_read_through.empty(),
                         "No read through signal received")
        circuit = CS.RT_circuit(params)
        circuit.run(5)
        self.assertLess(circuit.local.environments["Yellow"], 0.0001, "Promoter turned on with read through")

    def test_sc_ll_circuit(self):
        # check supercoiling stays inside or outside the loop
        params = [-1, -1, 1, 0, 0, -1, 0, 0, 0.1]
        circuit = CS.SC_LL_circuit(params)
        self.assertEqual(circuit.circuit_components[6].sc_rate, 0.1, "Incorrect supercoiling rate")
        circuit.run(5)
        before = circuit.local.supercoil_regions[3]
        params = [-1, -1, 1, 0, 0, -1, 0, 10, 0.1]
        circuit = CS.SC_LL_circuit(params)
        circuit.run(5)
        self.assertNotEqual(before, circuit.local.supercoil_regions[3], "No supercoiling effect from lac loop")

    def test_sc_cr_circuit(self):
        # check supercoiling and repression both run
        # check supercoiling stays inside or outside the loop
        params = [-1, -1, 1, 0, 0, -1, 0, 0, 0.1]
        circuit = CS.SC_CR_circuit(params)
        self.assertEqual(circuit.circuit_components[6].sc_rate, 0.1, "Incorrect supercoiling rate")
        circuit.run(5)
        before = circuit.local.supercoil_regions[3]
        params = [-1, -1, 1, 0, 0, -1, 0, 10, 0.1]
        circuit = CS.SC_CR_circuit(params)
        circuit.run(5)
        self.assertEqual(before, circuit.local.supercoil_regions[3], "No supercoiling effect from repression")
        self.assertEqual(circuit.local.environments["Yellow"], 0, "Promoter turned on with repression")

    def test_sc_ll_cr_circuit(self):
        # check supercoiling in regions correct
        params = [-1, -1, 1, 0, 0, -1, 0, 0, 0.1]
        circuit = CS.SC_LL_CR_circuit(params)
        self.assertEqual(circuit.circuit_components[6].sc_rate, 0.1, "Incorrect supercoiling rate")
        circuit.run(5)
        before = circuit.local.supercoil_regions[3]
        params = [-1, -1, 1, 0, 0, -1, 0, 10, 0.1]
        circuit = CS.SC_LL_CR_circuit(params)
        circuit.run(5)
        self.assertNotEqual(before, circuit.local.supercoil_regions[3], "No supercoiling effect from lac loop")
        self.assertEqual(circuit.local.environments["Yellow"], 0, "Promoter turned on with repression")

    def test_sc_circuit(self):
        # Check bridge stays open and correct promoter response
        # Parameters are: CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti-tet
        # First with no supercoiling generation to keep check promoter off
        params = [-15, -1, 1, 0, 0, -1, 0, 0, 0]
        circuit = CS.SC_circuit(params)
        self.assertFalse(circuit.circuit_components[10].clockwise, "Promoter wrong direction")
        circuit.run(5)
        before = circuit.local.supercoil_regions[2]
        # Second with supercoiling
        params = [-1, -1, 1, 0, 0, -1, 0, 0, 0.1]
        circuit = CS.SC_circuit(params)
        self.assertEqual(circuit.circuit_components[6].sc_rate, 0.1, "Incorrect supercoiling rate")
        circuit.run(5)
        self.assertNotEqual(before, circuit.local.supercoil_regions[2], "No supercoiling effect from anti-tet")

    def test_rt_sc_ll_circuit(self):
        self.fail()

    def test_rt_sc_cr_circuit(self):
        self.fail()

    def test_rt_sc_ll_cr_circuit(self):
        self.fail()

    def test_rt_sc_circuit(self):
        self.fail()

    def test_ll_circuit(self):
        # Check bridge closes preventing supercoiling and promoter activation
        # Parameters are: CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate
        # Second with supercoiling
        params = [-1, -1, 1, 0, 0, -1, 0, 10, 0]
        circuit = CS.LL_circuit(params)
        circuit.run(5)
        self.assertEqual(circuit.local.supercoil_regions[3], 0, "Supercoiling propagating with bridge closed")
        self.assertLess(circuit.local.environments["Yellow"], 1, "Promoter turned on with closed bridge")

    def test_cr_circuit(self):
        # Check repression prevents promoter activation but does not repress supercoiling
        # Parameters are: CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate
        # Second with supercoiling
        params = [-1, -1, 1, 0, 0, -1, 0, 10, 0]
        circuit = CS.CR_circuit(params)
        circuit.run(5)
        self.assertEqual(circuit.local.supercoil_regions[3], -1, "Supercoiling not propagating with bridge open")
        self.assertEqual(circuit.local.environments["Yellow"], 0, "Promoter turned on with repression")

    def test_ll_cr_circuit(self):
        # Check repression prevents promoter activation and bridge prevents supercoiling propagation
        # Parameters are: CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate
        # Second with supercoiling
        params = [-1, -1, 1, 0, 0, -1, 0, 10, 0]
        circuit = CS.LL_CR_circuit(params)
        circuit.run(5)
        self.assertEqual(circuit.local.supercoil_regions[3], 0, "Supercoiling propagating with bridge closed")
        self.assertEqual(circuit.local.environments["Yellow"], 0, "Promoter turned on with repression")

    def test_none_circuit(self):
        # Check bridge stays open and correct promoter response
        # Parameters are: CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti-tet
        # First with no supercoiling generation to keep check promoter off
        params = [-15, -1, 1, 0, 0, 0, 0, 0, 0]
        circuit = CS.None_circuit(params)
        circuit.run(5)
        self.assertAlmostEqual(circuit.local.environments["Yellow"], 0, 3,
                               "Promoter turned on in absence of supercoiling")
        # Second with supercoiling
        params = [-1, -1, 1, 0, 0, -1, 0, 0, 0]
        circuit = CS.None_circuit(params)
        circuit.run(5)
        self.assertGreater(circuit.local.environments["Yellow"], 1, "Promoter turned off with negative supercoiling")
        self.assertEqual(circuit.local.supercoil_regions[3], -1, "Supercoiling not propagating correctly")
