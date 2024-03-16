from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def get_phys_data(binding_file, supercoiling_file, reporter_output, output_file):
    initialisations_df = pd.read_csv(binding_file)
    supercoiling_df = pd.read_csv(supercoiling_file)
    init_values = initialisations_df.loc[:, 'simulation_0':'simulation_95'].values.flat
    sc_values = supercoiling_df.loc[:, 'simulation_0':'simulation_95'].values.flat
    df = pd.DataFrame({'Initialisation': init_values, 'Supercoiling': sc_values})
    df = df.sort_values(by=['Supercoiling'])
    groups = df.loc[df["Initialisation"] == 1]
    print(groups.quantile(.75))
    print(groups.mean())
    print(groups.std())
    sns.set_theme(style="white", font_scale=1.3)
    sns.histplot(data=groups, x='Supercoiling', cumulative=False)
    plt.savefig(output_file + "hist.png", bbox_inches="tight")
    plt.show()
    pass


if __name__ == "__main__":
    get_phys_data("/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting/TORCPhys_comp_data"
                  "/binding_mKalama1_df.csv",
                  "/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting/comp_feed_partial_circuit"
                  "/no_bridge/superhelical_mKalama1_df.csv",
                  0.3989,
                  "/home/psmr500/PycharmProjects/TORC/Experiment_Data/Parameter_Setting/sigmoid_training")
