# start with random search with fixed gradient and sigmoid
# select best candidate as start point for gradient descent
# check against salmonella WT DTA ratio and values to select best candidate
# set up generating parameter set to test for salmonella WT
# select best resultant ind
# repeat till happy with Salmonella WT
# include smaller steps if no progress being made
# TODO: fix supercoiling outputs values and rerun random search for second promoter
# TODO: select candidate based on min promoter
# TODO: gradiant descent for min

# TODO: add ecoli parameter setting
import pandas as pd
import concurrent.futures
from TORC import RandomSearch as rs


def process_circuit_step_parameters(params, fixed=None, increment=1):
    """
    Generates parameter set with small changes in each parameter.

    Parameters
    ----------
    params   :   dict
        Parameters for the circuit.
    fixed    :   list
        Keywords for fixed parameters.
    increment :   float
        amount by which to vary parameters (weighted based on parameter range before applied)

    Returns
    -------
    List<float>
        List of parameter values for the circuit:
            +   tetA_sc         - The supercoiling output from tetA
            +   mhYFP_sc        - The supercoiling output from mhYFP
            +   pleuWT_sigmoid  - The midpoint of the sigmoid function for the promoter to respond to supercoiling
            +   mhYFP_max       - The maximum output of the Yellow reporter gene
            +   mhYFP_min       - The minimum output of the Yellow reporter gene
            +   relax_WT        - The relaxation rate for supercoils in the WT strain bacteria (proxy for topoisomerase
                                  activity)
            +   relax_DTA       - The relaxation rate for supercoils in the delta topA strain bacteria (proxy for
                                  topoisomerase activity)
            +   gradient        - The gradient of the sigmoid function for the promoter to respond to supercoiling
    """
    increments = {"gradient": 0.1 * increment, "mhYFP_max": 8 * increment, "mhYFP_min": 2 * increment,
                  "relax_WT": 0.02 * increment, "relax_DTA": 0.02 * increment,
                  "tetA_sc": 0.005 * increment, "mhYFP_sc": 0.001 * increment, "anti_tetA_sc": 0.0001 * increment}
    fixed = [] if not fixed else fixed
    if "pleuWT_sigmoid" not in fixed:
        temp_param = [[params["pleuWT_sigmoid"] + increments["pleuWT_sigmoid"]], [params["pleuWT_sigmoid"]],
                      [params["pleuWT_sigmoid"] - increments["pleuWT_sigmoid"]]]
    else:
        temp_param = [[params["pleuWT_sigmoid"]]]
    params_set = temp_param
    for keyword in increments.keys():
        if keyword not in fixed:
            temp_param = [[params[keyword] + increments[keyword]],
                          [params[keyword]], [params[keyword] - increments[keyword]]]
        else:
            temp_param = [[params[keyword]]]
        new_params = []
        for p in params_set:
            for temp in temp_param:
                new_params.append(p + temp)
        params_set = new_params
    return params_set


def parallel_circuit_runs(repeats, duration, process_circuit, params, output_file):
    """
    Performs the runs of the circuit so that the output can be assessed for fitness.

    Parameters
    ----------
    repeats         :   int
        Number of circuit iterations that will be run
    duration        :   duration
        Number of time steps to run the circuit for
    process_circuit :   Function
        The function that runs a single circuit
    params          :   List<List>
        The list of parameter sets to be passed to the circuit function for each separate run.
    output_file     :   str
        The file name for output from the process that will be read in from file. The file is overwritten in each
        generation to save space.

    Returns
    -------
        None the output is saved to file.
    """
    cols = ["time", "tetA_sc_rate", "Yellow_sc_rate", "Yellow_response", "Yellow_gradient", "Yellow_strong",
            "Yellow_weak", "SC_relax", "Yellow_value", "Yellow_sc_region", "Strain"]
    cols_comp = ["tetA_sc_rate", "Yellow_sc_rate", "Yellow_response", "Yellow_gradient", "Yellow_strong",
                 "Yellow_weak", "SC_relax_WT", "SC_relax_DTA", "Yellow_value_WT", "Yellow_value_DTA", "Ratio"]
    df = pd.DataFrame(columns=cols)
    comp_df = pd.DataFrame(columns=cols_comp)
    df.to_csv(output_file, index=False, header=True)
    comp_df.to_csv("Combined_Data_" + output_file, index=False, header=True)
    # process_circuit(duration, params[0], output_file, "sigmoid")
    with concurrent.futures.ThreadPoolExecutor(max_workers=repeats) as executor:
        executor.map(process_circuit, [duration for _ in range(repeats)], params,
                     [output_file for _ in range(repeats)],
                     ["Combined_Data_" + output_file for _ in range(repeats)],
                     ["normal" for _ in range(repeats)])


# select parameters from results
def selection(checks, output, random_search=False):
    """
    Compares the output values for the yellow fluorescent protein and ranks their accuracy as raw values and the ratio
    between them. I then selects the best individual parameter set base on the sum of the three ranks.

    Parameters
    ----------
    checks          :   List<float>
        The values taken from the bio experiments to check against. Should be Ratio (WT/DTA), Yellow_WT, Yellow_DTA
    output          :   str
        File name for the output from the runs.
    random_search   :   bool
        Dictates the variation in file names for random searches verses the gradient descent outputs.

    Returns
    -------
    dict
        The dictionary of parameters that are the current best individual
    Series
        The dataframe row containing the results from running the best individual
    """
    # load results
    ratio, WT, DTA = checks
    if random_search:
        df = pd.read_csv("Combined_Data_" + output + "_Initial_Random_Search.csv")
    else:
        df = pd.read_csv("Combined_Data_" + output + ".csv")
    # get difference of end values and ratio with checks
    df["WT_check"] = abs(df["Yellow_value_WT"] - WT)
    df["DTA_check"] = abs(df["Yellow_value_DTA"] - DTA)
    df["Ratio_check"] = abs(df["Ratio"] - ratio)
    df["WT_rank"] = df["WT_check"].rank(ascending=True)
    df["DTA_rank"] = df["DTA_check"].rank(ascending=True)
    df["Ratio_rank"] = df["Ratio_check"].rank(ascending=True)
    # select for lowest combined rank (not actual values)
    df["Total_rank"] = df["WT_rank"] + df["DTA_rank"] + df["Ratio_rank"]
    best_row = min(df.index, key=lambda i: df["Total_rank"][i])
    # form parameter dictionary
    best = {"tetA_sc": df["tetA_sc_rate"][best_row], "mhYFP_sc": df["Yellow_sc_rate"][best_row],
            "pleuWT_sigmoid": df["Yellow_response"][best_row], "mhYFP_max": df["Yellow_strong"][best_row],
            "mhYFP_min": df["Yellow_weak"][best_row], "relax_WT": df["SC_relax_WT"][best_row],
            "relax_DTA": df["SC_relax_DTA"][best_row], "gradient": df["Yellow_gradient"][best_row],
            "anti_tetA_sc": 0.001}
    return best, df.iloc[best_row]


# check for need to fix
def fixing_values(fixed, checks, df_row, accuracy):
    """
    Checks output values against desired accuracy and fixes parameters based on this. We focus on correct ratios which
    are used to fix in rounds the promoter response, the supercoiling output of genes and the relaxation of supercoiling.
    This means the parameters must produce a correct ratio upto three rounds assuming no fixed values given at start to
    fix all these values. We also check the output values for accuracy the WT value is used to fix min output from the
    fluorescent protein and DTA for the max. Since the min and max both effect the other value this only remains fixed
    while the values remain sufficiently accurate.

    Parameters
    ----------
    fixed       :   List<str>
        List of values that have already been fixed
    checks      :   List<float>
        The ratio and yellow values for the wild type and delta topA systems for comparisons
    df_row      :   Series
        The output from running the current best parameter set on the circuit
    accuracy    :   float
        The level of accuracy needed in the outputs before we fix values

    Returns
    -------
    List<str>
        The updated list of fixed values
    """
    # only check selected individual (quicker)
    ratio, WT, DTA = checks
    # Check ratio first, if close enough to values then fix promoter values
    if "relax_DTA" not in fixed:
        if df_row["Ratio_check"] / ratio <= accuracy:
            if "pleuWT_sigmoid" not in fixed:
                fixed.append("pleuWT_sigmoid")
                fixed.append("gradient") if "gradient" not in fixed else None
                return fixed
            elif "mhYFP_sc" not in fixed:
                # if promoter values already fixed then fix supercoiling values
                fixed.append("tetA_sc") if "tetA_sc" not in fixed else None
                fixed.append("mhYFP_sc") if "mhYFP_sc" not in fixed else None
                return fixed
            else:
                fixed.append("relax_WT") if "relax_WT" not in fixed else None
                fixed.append("relax_DTA") if "relax_DTA" not in fixed else None
                return fixed
    # if all ratio values fixed check output values
    # if both WT and DTA close enough fix both outputs
    if (df_row["WT_check"] / WT <= accuracy) and (df_row["DTA_check"] / DTA <= accuracy):
        fixed.append("mhYFP_min") if "mhYFP_min" not in fixed else None
        fixed.append("mhYFP_max") if "mhYFP_max" not in fixed else None
        return fixed
    # else if WT good fix min but unfix max
    elif df_row["WT_check"] / WT <= accuracy:
        fixed.append("mhYFP_min") if "mhYFP_min" not in fixed else None
        fixed.remove("mhYFP_max") if "mhYFP_max" in fixed else None
        return fixed
    # else if DTA good fix max but unfix min
    elif df_row["DTA_check"] / DTA <= accuracy:
        fixed.remove("mhYFP_min") if "mhYFP_min" in fixed else None
        fixed.append("mhYFP_max") if "mhYFP_max" not in fixed else None
        return fixed
    # else return fixed as is.
    else:
        fixed.remove("mhYFP_min") if "mhYFP_min" in fixed else None
        fixed.remove("mhYFP_max") if "mhYFP_max" in fixed else None
        return fixed


def parameter_setting(output, accuracy=0.001, fixed=None, duration=1000, increment=0.002, checks=None,
                      generation_limit=120, fixed_values=None, starter_params=None):
    """
    Runs a gradient descent to search for an parameter set that gives and output matching the biological experiment
    data provided in checks. It starts by running a random search over biologically plausible values unless a set of
    starting parameters is provided. After that it selects the best individual (the starter if given) to then start a
    gradient descent with. For each generation it tests all the possible steps on all non-fixed values and then selects
    the best individual. It checks the best individual and fixes some parameters based on correct outputs. It also
    halves the increment sizes if no improving step is found in a generation. The system stops if the generation limit
    is reached, the increment size has been reduced 10 times or all values have become fixed.

    Parameters
    ----------
    output              :   str
        Name to use for output files.
    accuracy            :   float
        Level of accuracy needed to fix parameters
    fixed               :   List<str>
        List of parameters that should be fixed from the start
    duration            :   int
        Number of time steps to run circuits for
    increment           :   float
        Relative size of steps to be taken. default is 1 and corresponds to steps which are roughly 1 tenth the size of
        range of biologically plausible values.
    checks              :   List<float>
        List of ratio, yellow output in WT and yellow output in DTA taken from biological experiments. Used to check
        accuracy and select parameter sets
    generation_limit    :   int
        Number of generations to run before stopping as a max limit. (Early stopping possible if all parameters fixed or
        increment has become too small.
    fixed_values        :   dict
        Keyword value pairings to set fixed values before running random search and gradient descent.
    starter_params      :   dict
        Parameter dictionary to use as the start point for the gradient descent

    Returns
    -------
    dict
        Best parameter set found at termination.

    """
    # set up circuit
    process_circuit = rs.process_circuit
    # check if starter_params provided
    if starter_params:
        best = starter_params
    else:
        # random search - pull all functions from RandomSearch
        rs.random_search(500, duration, output + "_Initial_Random_Search.csv", fixed_values, "normal")
        # select best parameters from results
        best, _ = selection(checks, output, random_search=True)
    # do while loop (check if all values fixed)
    fixed = [] if not fixed else fixed
    increment_count = 0
    generation = 0
    while (len(fixed) < 9) and (increment_count <= 10) and (generation < generation_limit):
        print("Fixed: " + str(fixed) + " Increment: " + str(increment) + " Generation: " + str(generation))
        # gen new parameter set
        params = process_circuit_step_parameters(best, fixed, increment)
        # run parameter set - pull process_circuit function from Random Search
        parallel_circuit_runs(len(params), duration, process_circuit, params, output + ".csv")
        # select best parameters from results
        best_new, row = selection(checks, output, random_search=False)
        # check for increment change needed
        if best_new == best:
            increment = increment * 0.5
            increment_count = increment_count + 1
        else:
            best = best_new
        # set fixed values
        fixed = fixing_values(fixed, checks, row, accuracy)
        generation = generation + 1
    # return parameters
    return best


if __name__ == "__main__":
    # Run for min promoter salmonella
    check_values = [0.6917340988, 21443.75987, 31000.00405]
    fixed_values_full = {"pleuWT_sigmoid": -0.08719539871858617, "gradient": 0.12845853187246675, "tetA_sc": 0.05,
                         "anti_tet_sc": 0.001, "mhYFP_sc": 0.0030446120261538,
                         'relax_WT': 0.7152736182204096, 'relax_DTA': 0.2196310757689402}
    starter = {'tetA_sc': 0.05, 'mhYFP_sc': 0.0030446120261538, 'pleuWT_sigmoid': -0.0871953987185861,
               'mhYFP_max': 21.890110326714744, 'mhYFP_min': 18.621844452749595, 'relax_WT': 0.7152736182204096,
               'relax_DTA': 0.2196310757689402, 'gradient': 0.1284585318724667, 'anti_tetA_sc': 0.001}
    min_parameters = parameter_setting("Gradient_Descent_Phys_Test_Full", 0.01,
                                       ["pleuWT_sigmoid", "gradient", "tetA_sc", "anti_tet_sc",
                                        "mhYFP_sc", "relax_WT", "relax_DTA"], 1000, 0.0078125,
                                       check_values, 60, fixed_values_full, starter)
    print(min_parameters)
    # TODO: run for min promoter, Add fixed values hand in for random search parameter generation function
    # min_promoter = parameter_setting("Gradient_Descent_Phys_Test_Min", )
