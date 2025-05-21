from TORC import GradientDescent as gd
from TORC import RandomSearch as rs
from unittest import TestCase
import pandas as pd
import pathlib as pl
import os


class Test(TestCase):
    def test_process_circuit_step_parameters(self):
        # tetA_sc_rate, CF_sc_rate, CF_response, CF_strong, CF_weak, relax, gradient = parameters
        dict_params = {"tetA_sc": -15, "mhYFP_sc": -1, "pleuWT_sigmoid": 0, "mhYFP_max": 1, "mhYFP_min": 0,
                       "relax_WT": 0, "relax_DTA": 0.5, "gradient": -1}
        params = gd.process_circuit_step_parameters(dict_params, )
        self.assertEqual(len(params), 6561, "Wrong number of parameters returned")
        params = gd.process_circuit_step_parameters(dict_params, ["gradient", "pleuWT_sigmoid", "tetA_sc"])
        self.assertEqual(len(params), 243, "Wrong number of parameters returned with fixed parameters")
        params_small_inc = gd.process_circuit_step_parameters(dict_params,
                                                              ["gradient", "pleuWT_sigmoid", "tetA_sc"],
                                                              0.001)
        self.assertNotEqual(params_small_inc, params, "Increment value not working")

    def test_selection(self):
        # set up test data for selection
        checks = [0.6633588091, 20471.26332, 30860.01578]
        output = "Test_Data"
        best, _ = gd.selection(checks, output)
        self.assertIsInstance(best, dict, "selection not returning dictionary")
        self.assertEqual(best, {'gradient': 0.7267593004, 'mhYFP_max': 65.78387956792757,
                                'mhYFP_min': 1.4649103071628666, 'mhYFP_sc': 0.003512001343,
                                'pleuWT_sigmoid': -0.114657413, 'relax_DTA': 0.1761112448061897,
                                'relax_WT': 0.9565458088572388, 'tetA_sc': -0.05}, "Wrong selection returned")

    def test_fixing_values(self):
        checks = [0.6633588091, 20471.26332, 30860.01578]
        output = "Test_Data"
        _, best_row = gd.selection(checks, output)
        fixed = []
        fixed = gd.fixing_values(fixed, checks, best_row, 0.001)
        self.assertListEqual(fixed, [], "Fixing values when too inaccurate")
        checks = [0.6519, 5, 65]
        fixed = gd.fixing_values(fixed, checks, best_row, 0.1)
        self.assertListEqual(fixed, ["pleuWT_sigmoid", "gradient"], "Fixing wrong values first")
        fixed = gd.fixing_values(fixed, checks, best_row, 0.1)
        self.assertListEqual(fixed, ["pleuWT_sigmoid", "gradient", "tetA_sc", "mhYFP_sc"],
                             "Failed to add supercoiling values to fixed list")
        fixed = gd.fixing_values(fixed, checks, best_row, 0.1)
        self.assertListEqual(fixed, ["pleuWT_sigmoid", "gradient", "tetA_sc", "mhYFP_sc", "relax_WT", "relax_DTA"],
                             "Failed to add relax values to fixed list")
        fixed = gd.fixing_values(fixed, checks, best_row, 0.1)
        self.assertListEqual(fixed, ["pleuWT_sigmoid", "gradient", "tetA_sc", "mhYFP_sc", "relax_WT", "relax_DTA"],
                             "Fixed inaccurate values")
        checks = [0.6633588091, 20471.26332, 30860.01578]
        fixed = gd.fixing_values(fixed, checks, best_row, 0.001)
        self.assertListEqual(fixed, ["pleuWT_sigmoid", "gradient", "tetA_sc", "mhYFP_sc", "relax_WT", "relax_DTA"],
                             "Fixed inaccurate values")
        fixed = gd.fixing_values(fixed, checks, best_row, 0.001)
        self.assertListEqual(fixed, ["pleuWT_sigmoid", "gradient", "tetA_sc", "mhYFP_sc", "relax_WT", "relax_DTA"],
                             "Fixed inaccurate values")
        checks = [0.651948, 22287.905349, 34187.649965]
        best_row = best_row.to_dict()
        best_row["DTA_check"] = 33326.634185
        best_row = pd.Series(best_row)
        fixed = gd.fixing_values(fixed, checks, best_row, 0.1)
        self.assertListEqual(fixed, ["pleuWT_sigmoid", "gradient", "tetA_sc", "mhYFP_sc", "relax_WT", "relax_DTA",
                                     "mhYFP_min"],
                             "Failed to fix min without fixing max")
        best_row = best_row.to_dict()
        best_row["WT_check"] = 11816.642029
        best_row["DTA_check"] = 3326.634185
        best_row = pd.Series(best_row)
        fixed = gd.fixing_values(fixed, checks, best_row, 0.1)
        self.assertListEqual(fixed, ["pleuWT_sigmoid", "gradient", "tetA_sc", "mhYFP_sc", "relax_WT", "relax_DTA",
                                     "mhYFP_max"],
                             "Failed to fix max and unfix min")
        best_row = best_row.to_dict()
        best_row["WT_check"] = 1816.642029
        best_row = pd.Series(best_row)
        fixed = gd.fixing_values(fixed, checks, best_row, 0.1)
        self.assertListEqual(fixed, ["pleuWT_sigmoid", "gradient", "tetA_sc", "mhYFP_sc", "relax_WT", "relax_DTA",
                                     "mhYFP_max", "mhYFP_min"],
                             "Failed to fix min and max")

    def test_parallel_circuit_runs(self):
        dict_params = {"tetA_sc": -15, "mhYFP_sc": -1, "pleuWT_sigmoid": 0, "mhYFP_max": 1, "mhYFP_min": 0,
                       "relax_WT": 0, "relax_DTA": 0.5, "gradient": -1, "anti_tetA_sc": 0.001}
        params = gd.process_circuit_step_parameters(dict_params, ["gradient", "pleuWT_sigmoid", "tetA_sc"])
        gd.parallel_circuit_runs(len(params), 10, rs.process_circuit, params, "Parallel_Circuit_Test.csv")
        path = pl.Path("Combined_Data_Parallel_Circuit_Test.csv")
        self.assertTrue(path.is_file())
        checks = [0.6633588091, 20471.26332, 30860.01578]
        best, _ = gd.selection(checks, "Parallel_Circuit_Test")
        os.remove("Combined_Data_Parallel_Circuit_Test.csv")
        os.remove("Parallel_Circuit_Test.csv")

    def test_parameter_setting(self):
        check_values = [0.6633588091, 20471.26332, 30860.01578]
        full_promoter = gd.parameter_setting("Gradient_Descent_Phys_Test_Full", 0.5,
                                            ["pleuWT_sigmoid", "gradient", "tetA_sc", "anti_tetA_sc"],
                                             1000, 0.02, check_values, generation_limit=3)
        os.remove("Gradient_Descent_Phys_Test_Full_Initial_Random_Search.csv")
        os.remove("Combined_Data_Gradient_Descent_Phys_Test_Full_Initial_Random_Search.csv")
        os.remove("Gradient_Descent_Phys_Test_Full.csv")
        os.remove("Combined_Data_Gradient_Descent_Phys_Test_Full.csv")
