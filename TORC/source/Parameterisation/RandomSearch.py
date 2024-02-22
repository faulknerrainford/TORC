import random
import pandas as pd
import numpy as np
import concurrent.futures
from TORC import Plasmid


# generate circuit and run for steps = len(phys experiment)
def partial_circuit(duration, parameters, output_file):
    cols = ["time", "tetA_sc_rate", "Blue_sc_rate", "Blue_response", "Blue_strong", "Blue_weak", "SC_relax",
            "Blue_value", "Blue_sc_region"]
    df = pd.DataFrame(columns=cols)
    # sort parameters and declare circuit
    tetA_sc_rate, CF_sc_rate, CF_response, CF_strong, CF_weak, relax = parameters
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}),
                       ("CF", "blue", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                       "response": CF_response})], relax=relax)
    circuit.setup()
    for i in range(duration):
        circuit.run(1)
        # save to dataframe at each timestep
        new_row = np.array([i, tetA_sc_rate, CF_sc_rate, CF_response, CF_strong, CF_weak, relax,
                            circuit.local.environments["blue"], circuit.local.supercoil_regions[1]])
        df.loc[len(df.index)] = new_row
    df.to_csv(output_file, mode='a', index=False, header=False)


# generate random set of parameters for circuit
def partial_circuit_random_parameters(count):
    # tetA_sc_rate 0...1
    # CF_sc_rate 0...1
    # CF_response -1...1
    # CF_strong 0...1
    # CF_weak 0...1
    # relax 0...1
    return [[random.random(), random.random(), random.uniform(-1, 1), random.random(), random.random(),
             random.random()] for _ in range(count)]


def random_search(repeats, duration, output_file):
    cols = ["time", "tetA_sc_rate", "Blue_sc_rate", "Blue_response", "Blue_strong", "Blue_weak", "Blue_value",
            "Blue_sc_region"]
    df = pd.DataFrame(columns=cols)
    df.to_csv(output_file, index=False, header=True)
    params = partial_circuit_random_parameters(repeats)
    # run multiple circuits with threading
    with concurrent.futures.ThreadPoolExecutor(max_workers=repeats) as executor:
        executor.map(partial_circuit, [duration for _ in range(repeats)], params, [output_file
                                                                                   for _ in range(repeats)])

# TODO: write fitness check against data with and without supercoiling

# TODO: write hill climb/possible swarm optimiser for same circuits


if __name__ == "__main__":
    random_search(200, 1000, "test_res.csv")
    pass
