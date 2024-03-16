import random
import pandas as pd
import numpy as np
import concurrent.futures
from TORC import Plasmid
from datetime import datetime


# generate circuit and run for steps = len(phys experiment)
def partial_circuit(duration, parameters, output_file=None, promoter_curve="threshold"):
    """
    Generates a partial circuits including tetA, mKalama and Pleu500 promoter. It runs the circuits for the given
    duration and writes the results after each timestep to a dataframe. At the end of the run this is appeneded to
    the output_file. The output includes the parameter settings and the supercoiling in the promoters region and
    environment value of blue fluorescence.
    Parameters
    ----------
    duration        :   int
        Number of timesteps to run circuit for.
    parameters      :   List<float>
        List of parameter values for the circuit:
            +   tetA supercoiling production rate
            +   mKalama supercoiling production rate
            +   Pleu500 supercoiling response threshold
            +   mKalama max output
            +   mKalama min output
            +   rate of supercoiling relaxation due to topoisomerases
    output_file     :   String
        Filename to append dataframe to.
    promoter_curve  :   String
        Type of curve used to determine rate in promoter


    Returns
    -------

    """
    cols = ["time", "tetA_sc_rate", "Blue_sc_rate", "Blue_response", "Blue_gradient", "Blue_strong", "Blue_weak",
            "SC_relax", "Blue_value", "Blue_sc_region"]
    df = pd.DataFrame(columns=cols)
    # sort parameters and declare circuit
    tetA_sc_rate, CF_sc_rate, CF_response, CF_strong, CF_weak, relax, gradient = parameters
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}),
                       ("CF", "blue", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                       "response": CF_response, "gradient": gradient, "rate_dist": promoter_curve})],
                      relax=relax)
    circuit.setup()
    for i in range(duration):
        circuit.run(1)
        # save to dataframe at each timestep
        new_row = np.array([i, tetA_sc_rate, CF_sc_rate, CF_response, gradient, CF_strong, CF_weak, relax,
                            circuit.local.environments["blue"], circuit.local.supercoil_regions[1]])
        df.loc[len(df.index)] = new_row
    if output_file:
        df.to_csv(output_file, mode='a', index=False, header=False)
    return df


def full_circuit(duration, parameters, output_file=None, promoter_curve="threshold"):
    """
    Generates a partial circuits including tetA, mKalama and Pleu500 promoter. It runs the circuits for the given
    duration and writes the results after each timestep to a dataframe. At the end of the run this is appeneded to
    the output_file. The output includes the parameter settings and the supercoiling in the promoters region and
    environment value of blue fluorescence.
    Parameters
    ----------
    duration        :   int
        Number of timesteps to run circuit for.
    parameters      :   List<float>
        List of parameter values for the circuit:
            +   tetA supercoiling production rate
            +   mKalama supercoiling production rate
            +   Pleu500 supercoiling response threshold
            +   mKalama max output
            +   mKalama min output
            +   rate of supercoiling relaxation due to topoisomerases
    output_file     :   String
        Filename to append dataframe to.
    promoter_curve  :   String
        Type of curve used to determine rate in promoter

    Returns
    -------

    """
    cols = ["time", "tetA_sc_rate", "Blue_sc_rate", "Blue_response", "Blue_gradient", "Blue_strong", "Blue_weak",
            "SC_relax", "Blue_value", "Blue_sc_region"]
    df = pd.DataFrame(columns=cols)
    # sort parameters and declare circuit
    tetA_sc_rate, CF_sc_rate, CF_response, CF_strong, CF_weak, relax, gradient = parameters
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}),
                       ("CF", "blue", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                       "response": CF_response, "gradient": gradient, "rate_dist": promoter_curve}),
                       ("CF", "red", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                      "response": CF_response, "gradient": gradient, "rate_dist": promoter_curve})],
                      relax=relax)
    circuit.setup()
    for i in range(duration):
        circuit.run(1)
        # save to dataframe at each timestep
        new_row = np.array([i, tetA_sc_rate, CF_sc_rate, CF_response, gradient, CF_strong, CF_weak, relax,
                            circuit.local.environments["blue"], circuit.local.supercoil_regions[1]])
        df.loc[len(df.index)] = new_row
    if output_file:
        df.to_csv(output_file, mode='a', index=False, header=False)
    return df


# generate random set of parameters for circuit
def partial_circuit_random_parameters(count):
    """
    Generates random parameter sets for the partial circuit.

    Parameters
    ----------
    count   :   int
        The number of parameters sets to generate

    Returns
    -------
    List<float>
        List of parameter values for the circuit:
            +   tetA supercoiling production rate - -1...0
            +   mKalama supercoiling production rate - 0...1
            +   Pleu500 supercoiling response threshold - -1...0
            +   mKalama max output - 0...1
            +   mKalama min output - 0
            +   rate of supercoiling relaxation due to topoisomerase activity - 0...1
            +   gradient of the promoter sigmoid activation function - -50...-10
    """
    params = []
    for i in range(count):
        #  Threshold version
        pleu500 = -0.047662
        gradient = 0.033367
        # tetA = random.uniform(-1, 0)
        # pleu500 = random.uniform(tetA, 0)
        # mKalama_sc = random.random()
        # mKalama_max = 0.0253897215070109
        # mKalama_max = 0.018390
        mKalama_max = 0.018752
        # relax = random.uniform(-tetA, 1)
        # Sigmoid version
        tetA = random.uniform(-0.2, 0)
        # pleu500 = random.uniform(-0.2, 0)
        mKalama_sc = random.uniform(0, 0.2)
        # mKalama_max = random.random()
        relax = random.uniform(0, 1)
        # gradient = random.uniform(-50, -10)
        params.append([tetA, mKalama_sc, pleu500, mKalama_max, 0, relax, gradient])
    return params


def random_search(repeats, duration, output_file=None):
    """
    Generates a set of random parameters for the partial circuit and then runs each as a circuit in with threading.


    Parameters
    ----------
    repeats     :   int
        Number of random circuits to run
    duration    :   int
        Number of timesteps to run for each circuit
    output_file :   String
        File name to save the data out to

    """
    seed = datetime.now().timestamp()
    if not output_file:
        output_file = "Partial_Circuit_Data_SCLim_Normal_FixedResponse_FixedBlue" + str(seed) + ".csv"
    cols = ["time", "tetA_sc_rate", "Blue_sc_rate", "Blue_response", "Blue_gradient", "Blue_strong", "Blue_weak",
            "sc_relax", "Blue_value", "Blue_sc_region"]
    df = pd.DataFrame(columns=cols)
    df.to_csv(output_file, index=False, header=True)
    params = partial_circuit_random_parameters(repeats)
    # run multiple circuits with threading
    partial_circuit(duration, params[0], output_file, "normal")
    with concurrent.futures.ThreadPoolExecutor(max_workers=repeats) as executor:
        executor.map(partial_circuit, [duration for _ in range(repeats)], params,
                     [output_file for _ in range(repeats)], ["normal" for _ in range(repeats)])


def hill_climbing_random_parameters(res_file, phys_file, rounds, duration, step=0.1, output_file=None):
    # set up output file
    seed = datetime.now().timestamp()
    if not output_file:
        output_file = "Partial_Circuit_Data_HillClimb_Reporter_" + str(seed) + ".csv"
    cols = ["time", "tetA_sc_rate", "Blue_sc_rate", "Blue_response", "Blue_gradient", "Blue_strong", "Blue_weak",
            "sc_relax", "Blue_value", "Blue_sc_region"]
    # load in results from pair grid and select best individual match parameters
    df = pd.DataFrame(columns=cols)
    df.to_csv(output_file, index=False, header=True)
    res_frame = pd.read_csv(res_file)
    params = res_frame.iloc[res_frame["trans_bind_match"].idxmin()]
    best = params.trans_bind_match
    print("Best parameters match:" + str(best))
    params = [params.tetA_sc_rate, params.Blue_sc_rate, params.Blue_response, params.Blue_strong,
              0, params.sc_relax, params.Blue_gradient]
    # get binding from results data, findable from phys_file name
    bindings = pd.read_csv(phys_file)["av_binding"]
    # compress to cumulative average over each ten timesteps
    bind_rate = bindings.groupby(np.arange(len(bindings)) // 10).sum()/22
    # start step at 0.1 and make smaller each step in duration
    standing = params
    for i in range(rounds):
        print("Round " + str(i+1) + "/" + str(rounds))
        # check step in both directions on circuit for resultant match
        stepA = standing[:3] + [standing[3]+step] + standing[4:]
        stepB = standing[:3] + [standing[3]-step] + standing[4:]
        print("A max: " + str(stepA[3]))
        print("B max: " + str(stepB[3]))
        stepA_df = partial_circuit(duration, stepA, output_file)
        stepB_df = partial_circuit(duration, stepB, output_file)
        # get match value for both steps
        stepA_df["binding_rate"] = stepA_df["time"].map(bind_rate)
        stepB_df["binding_rate"] = stepB_df["time"].map(bind_rate)
        stepA_match = np.mean(pd.Series.abs(stepA_df["Blue_value"] - stepA_df["binding_rate"]))
        stepB_match = np.mean(pd.Series.abs(stepB_df["Blue_value"] - stepB_df["binding_rate"]))
        # select better step, reduce step size
        if stepA_match < best and stepA_match <= stepB_match:
            best = stepA_match
            standing = stepA
        if stepB_match < best and stepB_match <= stepA_match:
            best = stepB_match
            standing = stepB
        step = 0.5 * step
        print("Standing max:" + str(standing[3]))
        # print match and return and print parameter setting for mKalama
    print("Best match found: " + str(best) + "\n mKalama max: " + str(standing[3]) + "\n Best parameter set: "
          + str(standing))
    return standing


if __name__ == "__main__":
    # params = partial_circuit_random_parameters(1)
    # df = partial_circuit(1000, params[0])
    random_search(1000, 1000)
    # hill_climbing_random_parameters(
    #     "/Experiment_Data/Parameter_Setting/Partial_Circuit_Data_SCLim_Sigmoid_1710162510.300931.csv",
    #                                 "/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting"
    #                                 "/comp_feed_partial_circuit/no_bridge/N_enzymes_mKalama1_df_CBindings.csv",
    #     100, 1000)
    pass
