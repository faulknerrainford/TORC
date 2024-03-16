import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ranksums


def load_phys_data(phys_file_name):
    """
    Loads the data from TORC Phys runs and processes it to give an idea of the transcription rate which can then be
    compared with the transcription in TORC Comp

    Parameters
    ----------
    phys_file_name   :   String
        string of path to correct TORCPhys data file.

    Returns
    -------
    dataframe :
        The cumulative sum of average enzyme bindings at each frame in the physics model

    """
    # read in data from phys model/
    phys_frame = pd.read_csv(phys_file_name, sep=",")
    # cal sum of rows/col_count
    # add as column
    col = phys_frame.loc[:, "simulation_0":"simulation_95"]
    phys_frame["av_binding"] = col.mean(axis=1)
    # create cumulative version of column
    phys_frame["cumulative_binding"] = phys_frame["av_binding"].cumsum(axis=0)
    # save updated data (with new name)
    new_phys_file = phys_file_name[:-4] + "_CBindings" + ".csv"
    phys_frame.to_csv(new_phys_file)
    return phys_frame["cumulative_binding"]


def load_comp_data(comp_file_name, bindings=None, phys_file_name=None):
    """

    Parameters
    ----------
    comp_file_name  :   String
        String of path to comp data
    bindings        :   List of floats
        List of the cumulative average binding at each frame in the physics model
    phys_file_name  :   String
        String of path to phys data (with CBindings)

    Returns
    -------

    """
    # Check if bindings handed in
    if not bindings and not phys_file_name:
        raise ValueError("Need bindings or file name to proceed")
    # If column not handed in directly get from file
    elif not bindings:
        bindings = pd.read_csv(phys_file_name)["av_binding"]
    # compress to cumulative average over each ten timesteps
    bind_rate = bindings.groupby(np.arange(len(bindings)) // 10).sum() / 22
    # load circuit data from comp
    comp_frame = pd.read_csv(comp_file_name)
    # add column to output data of circuits
    comp_frame["binding_rate"] = comp_frame["time"].map(bind_rate)
    # add abs diff with env to output data (and save result)
    comp_frame["Blue_rate"] = comp_frame["Blue_value"].diff()
    comp_frame["trans_bind_match"] = pd.Series.abs(comp_frame["Blue_rate"] - comp_frame["binding_rate"])
    # get sum of match for each parameter setting
    parameters = ["tetA_sc_rate", "Blue_sc_rate", "Blue_response", "Blue_strong", "sc_relax", "Blue_gradient"]
    comp_results_frame = comp_frame.groupby(parameters)["trans_bind_match"].mean()
    # save results and comp_frame back to file
    comp_frame.to_csv(comp_file_name)
    comp_results_frame.to_csv(comp_file_name[:-4] + "_RateCompResults.csv")


def random_search_parameters(file_name):
    # load data
    comp_res = pd.read_csv(file_name)
    # comp_res.drop("Blue_response", axis=1, inplace=True)
    # comp_res["log_match"] = np.log10(comp_res["trans_bind_match"])
    # comp_res.drop("trans_bind_match", axis=1, inplace=True)
    # seaborn scatter plot of mKalama strong against match value
    comp_res = comp_res.rename(columns={"tetA_sc_rate": "tetA sc", "Blue_sc_rate": "mKalama sc",
                                        "Blue_response": "response", "Blue_gradient": "gradient",
                                        "sc_relax": "relax", "Blue_strong": "mKalama max",
                                        "trans_bind_match": "m"})
    # comp_res.drop("mKalama max", axis=1, inplace=True)
    comp_res.drop("response", axis=1, inplace=True)
    comp_res.drop("gradient", axis=1, inplace=True)
    print(comp_res.loc[comp_res["m"].idxmin()])
    sns.set_theme(style="white", font_scale=1.3)
    # g = sns.scatterplot(data=comp_res, x="trans_bind_match", y="Blue_strong")
    # g.set(xlabel="m", ylabel="mKalama max output")
    # plt.xlabel("m", fontsize=14)
    # plt.ylabel("mKalama max output", fontsize=14)
    # seaborn pair grid hue=match
    g = sns.PairGrid(comp_res, hue="m")
    # g = sns.PairGrid(comp_res, hue="log_match")
    # use hist diag to show parameter coverage with hue=None (else will try hue from above, very confusing)
    g.map_diag(sns.histplot, hue=None, color=".3")
    g.map_offdiag(sns.scatterplot)
    g.add_legend()
    # hist probably needs color setting eg. ".3" and bin count increasing for interpretation
    plt.savefig(file_name[:-4] + "PairGridBehaviour.png", bbox_inches="tight")
    # plt.savefig(file_name[:-4] + "PairGridLog.png", bbox_inches="tight")
    # plt.savefig(file_name[:-4] + "MaxScatter.png", bbox_inches="tight")
    plt.show()
    pass


def boxplot(file_names):
    cols = [pd.read_csv(file) for file in file_names]
    cols = [df["trans_bind_match"] for df in cols]
    statistic, p_value = ranksums(cols[1], cols[3])
    r = abs(statistic)/np.sqrt(len(cols[1]))
    params = (["All" for _ in range(len(cols[0]))] + ["Fixed Max" for _ in range(len(cols[1]))] +
              ["Normal" for _ in range(len(cols[2]))] + ["Normal Fixed Max" for _ in range(len(cols[3]))])
    m = pd.concat(cols)
    df = pd.DataFrame({"Parameter set": params,
                       "m": m})
    sns.set_theme(style="white", font_scale=1.3)
    g = sns.boxplot(data=df, x="Parameter set", y="m", log_scale=True)
    g.set_xticklabels(g.get_xticklabels(), rotation=45)
    plt.savefig(file_names[0][:-20]+"Boxplot.png", bbox_inches="tight")
    plt.show()
    pass


if __name__ == "__main__":
    # load_comp_data(
    #     "/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting/Partial_Circuit_Data_SCLim_Normal_FixedResponse_FixedBlue1710438298.412516.csv",
    #     phys_file_name="/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting"
    #                               "/comp_feed_partial_circuit/no_bridge/N_enzymes_mKalama1_df_CBindings.csv")
    # random_search_parameters(
    #     "/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting/Partial_Circuit_Data_SCLim_Normal_FixedResponse_FixedBlue1710438298.412516_RateCompResults.csv")
    # pca_analysis("/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting/Partial_Circuit_Data_SCLim_Sigmoid_FixedBlue_FixedResponse1710178684.777095_RateCompResults.csv")
    boxplot(["/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting"
             "/Partial_Circuit_Data_SCLim_Sigmoid_1710162510.300931_RateCompResults.csv",
             "/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting"
             "/Partial_Circuit_Data_SCLim_Sigmoid_FixedBlue1710176585.520892_RateCompResults.csv",
             "/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting"
             "/Partial_Circuit_Data_SCLim_Normal_FixedResponse1710434146.623161_RateCompResults.csv",
             "/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting"
             "/Partial_Circuit_Data_SCLim_Normal_FixedResponse_FixedBlue1710438298.412516_RateCompResults.csv"])
    # boxplot(["/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting"
    #          "/Partial_Circuit_Data_SCLim_Sigmoid_1710162510.300931_RateCompResults.csv",
    #          "/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting"
    #          "/Partial_Circuit_Data_SCLim_Sigmoid_FixedBlue1710176585.520892_RateCompResults.csv"])