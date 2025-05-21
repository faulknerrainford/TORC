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
        amount by which to vary parameters.

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
        temp_param = [[params["pleuWT_sigmoid"]+increments["pleuWT_sigmoid"]], [params["pleuWT_sigmoid"]],
                      [params["pleuWT_sigmoid"]-increments["pleuWT_sigmoid"]]]
    else:
        temp_param = [[params["pleuWT_sigmoid"]]]
    params_set = temp_param
    for keyword in increments.keys():
        if keyword not in fixed:
            temp_param = [[params[keyword]+increments[keyword]],
                          [params[keyword]], [params[keyword]-increments[keyword]]]
        else:
            temp_param = [[params[keyword]]]
        new_params = []
        for p in params_set:
            for temp in temp_param:
                new_params.append(p + temp)
        params_set = new_params
    return params_set


def parallel_circuit_runs(repeats, duration, process_circuit, params, output_file):
    cols = ["time", "tetA_sc_rate", "Yellow_sc_rate", "Yellow_response", "Yellow_gradient", "Yellow_strong",
            "Yellow_weak", "SC_relax", "Yellow_value", "Yellow_sc_region", "Strain"]
    cols_comp = ["tetA_sc_rate", "Yellow_sc_rate", "Yellow_response", "Yellow_gradient", "Yellow_strong",
                 "Yellow_weak", "SC_relax_WT", "SC_relax_DTA", "Yellow_value_WT", "Yellow_value_DTA", "Ratio"]
    df = pd.DataFrame(columns=cols)
    comp_df = pd.DataFrame(columns=cols_comp)
    df.to_csv(output_file, index=False, header=True)
    comp_df.to_csv("Combined_Data_" + output_file, index=False, header=True)
    process_circuit(duration, params[0], output_file, "sigmoid")
    with concurrent.futures.ThreadPoolExecutor(max_workers=repeats) as executor:
        executor.map(process_circuit, [duration for _ in range(repeats)], params,
                     [output_file for _ in range(repeats)],
                     ["Combined_Data_" + output_file for _ in range(repeats)],
                     ["sigmoid" for _ in range(repeats)])


# select parameters from results
def selection(checks, output, random_search=False):
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
    # only check selected individual (quicker)
    ratio, WT, DTA = checks
    # Check ratio first, if close enough to values then fix promoter values
    if "relax_DTA" not in fixed:
        if df_row["Ratio_check"]/ratio <= accuracy:
            if "pleuWT_sigmoid" not in fixed:
                fixed.append("pleuWT_sigmoid")
                fixed.append("gradient") if "gradient" not in fixed else None
                return fixed
            elif "mhYFP_sc" not in fixed:
                # if promoter values already fixed then fix supercoiling values
                fixed.append("tetA_sc")
                fixed.append("mhYFP_sc") if "mhYFP_sc" not in fixed else None
                return fixed
            else:
                fixed.append("relax_WT") if "relax_WT" not in fixed else None
                fixed.append("relax_DTA") if "relax_DTA" not in fixed else None
                return fixed
    # if all ratio values fixed check output values
    # if both WT and DTA close enough fix both outputs
    if (df_row["WT_check"]/WT <= accuracy) and (df_row["DTA_check"]/DTA <= accuracy):
        fixed.append("mhYFP_min") if "mhYFP_min" not in fixed else None
        fixed.append("mhYFP_max") if "mhYFP_max" not in fixed else None
        return fixed
    # else if WT good fix min but unfix max
    elif df_row["WT_check"]/WT <= accuracy:
        fixed.append("mhYFP_min") if "mhYFP_min" not in fixed else None
        fixed.remove("mhYFP_max") if "mhYFP_max" in fixed else None
        return fixed
    # else if DTA good fix max but unfix min
    elif df_row["DTA_check"]/DTA <= accuracy:
        fixed.remove("mhYFP_min") if "mhYFP_min" in fixed else None
        fixed.append("mhYFP_max") if "mhYFP_max" not in fixed else None
        return fixed
    # else return fixed as is.
    else:
        return fixed


def parameter_setting(output, accuracy=0.001, fixed=None, duration=1000, increment=0.002, checks=None,
                      generation_limit=120, fixed_values=None):
    # set up circuit
    process_circuit = rs.process_circuit
    # random search - pull all functions from RandomSearch
    rs.random_search(500, duration, output + "_Initial_Random_Search.csv", fixed_values)
    # select best parameters from results
    best, _ = selection(checks, output, random_search=True)
    # do while loop (check if all values fixed)
    fixed = [] if not fixed else fixed
    increment_count = 0
    generation = 0
    while (len(fixed) < 9) and (increment_count <= 10) and (generation < generation_limit):
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
    # Run for full promoter salmonella
    check_values = [0.6633588091, 20471.26332, 30860.01578]
    full_promoter = parameter_setting("Gradient_Descent_Phys_Test_Full", 0.01,
                                      ["pleuWT_sigmoid", "gradient"], 1000, 0.002, check_values)
    # TODO: run for min promoter, Add fixed values hand in for random search parameter generation function
    # min_promoter = parameter_setting("Gradient_Descent_Phys_Test_Min", )