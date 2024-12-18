import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from TORC import CircuitSetups as cs

# Set up parameter sets for each of 12 strains as a list
# Salmonella Topo effects
relax_WT_Salmonella = 0.9567036642
relax_DTA_Salmonella = 0.1809996105

# Supercoiling values
tetA_sc = -0.05
mhYFP_sc = 0.003724793623

# Full promoter
pleuWT_sigmoid_full = -0.1749656277
gradient_full = 0.7509601833
# Output Salmonella
mhYFP_min_pfull_s = 6.467848859
mhYFP_max_pfull_s = 48.99416055

# Min promoter
pleuWT_sigmoid_min = -0.1179830536
gradient_min = 0.7438187636
# Output Salmonella
mhYFP_min_pmin_s = 5.245117679
mhYFP_max_pmin_s = 55.8519288

# Topo effects E.coli
relax_WT_ecoli = 0.93494294
relax_DTA_ecoli = 0.174762688

# Output
mhYFP_min_pfull_e = 6.37520546
mhYFP_max_pfull_e = 41.61628657

# Output
mhYFP_min_pmin_e = 5.47835592
mhYFP_max_pmin_e = 32.59074292

# Additional params
Lac_env = 4000
Atet_sc = 0.001

# CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet
# Parameters for strains
#   1. Ecoli - Full - WT
#   2. Ecoli - Full - DTA/DL
#   3. Ecoli - Full - DTA
#   4. Ecoli - Min - WT
#   5. Ecoli - Min - DTA/DL
#   6. Ecoli - Min - DTA
#   7. Salmonella - Full - WT
#   8. Salmonella - Full - DTA
#   9. Salmonella - Full - DTA/IL
#   10. Salmonella - Min - WT
#   11. Salmonella - Min - DTA
#   12. Salmonella - Min - DTA/IL

strains = [[pleuWT_sigmoid_full, gradient_full, mhYFP_max_pfull_e, mhYFP_min_pfull_e, relax_WT_ecoli, tetA_sc, mhYFP_sc,
            Lac_env, Atet_sc],
           [pleuWT_sigmoid_full, gradient_full, mhYFP_max_pfull_e, mhYFP_min_pfull_e, relax_DTA_ecoli, tetA_sc,
            mhYFP_sc, 0, Atet_sc],
           [pleuWT_sigmoid_full, gradient_full, mhYFP_max_pfull_e, mhYFP_min_pfull_e, relax_DTA_ecoli, tetA_sc,
            mhYFP_sc, Lac_env, Atet_sc],
           [pleuWT_sigmoid_min, gradient_min, mhYFP_max_pmin_e, mhYFP_min_pmin_e, relax_WT_ecoli, tetA_sc, mhYFP_sc,
            Lac_env, Atet_sc],
           [pleuWT_sigmoid_min, gradient_min, mhYFP_max_pmin_e, mhYFP_min_pmin_e, relax_DTA_ecoli, tetA_sc,
            mhYFP_sc, 0, Atet_sc],
           [pleuWT_sigmoid_min, gradient_min, mhYFP_max_pmin_e, mhYFP_min_pmin_e, relax_DTA_ecoli, tetA_sc,
            mhYFP_sc, Lac_env, Atet_sc],
           [pleuWT_sigmoid_full, gradient_full, mhYFP_max_pfull_s, mhYFP_min_pfull_s, relax_WT_Salmonella, tetA_sc,
            mhYFP_sc, 0, Atet_sc],
           [pleuWT_sigmoid_full, gradient_full, mhYFP_max_pfull_s, mhYFP_min_pfull_s, relax_DTA_Salmonella, tetA_sc,
            mhYFP_sc, 0, Atet_sc],
           [pleuWT_sigmoid_full, gradient_full, mhYFP_max_pfull_s, mhYFP_min_pfull_s, relax_DTA_Salmonella, tetA_sc,
            mhYFP_sc, Lac_env, Atet_sc],
           [pleuWT_sigmoid_min, gradient_min, mhYFP_max_pmin_s, mhYFP_min_pmin_s, relax_WT_Salmonella, tetA_sc,
            mhYFP_sc, 0, Atet_sc],
           [pleuWT_sigmoid_min, gradient_min, mhYFP_max_pmin_s, mhYFP_min_pmin_s, relax_DTA_Salmonella, tetA_sc,
            mhYFP_sc, 0, Atet_sc],
           [pleuWT_sigmoid_min, gradient_min, mhYFP_max_pmin_s, mhYFP_min_pmin_s, relax_DTA_Salmonella, tetA_sc,
            mhYFP_sc, Lac_env, Atet_sc]
           ]

process_split = {"Lac Loop": [[0, 2, 4, 6, 8, 10, 12, 14], [1, 3, 5, 7, 9, 11, 13, 15]],
                 "Lac Canonical Repression": [[1, 2, 5, 6, 9, 10, 13, 14], [0, 3, 4, 7, 8, 11, 12, 15]],
                 "Anti-tet Supercoiling": [[4, 5, 6, 7, 8, 9, 10, 11], [0, 1, 2, 3, 12, 13, 14, 15]],
                 "Anti-tet Read through": [[0, 1, 2, 3, 8, 9, 10, 11], [4, 5, 6, 7, 12, 13, 14, 15]]}

bio_finger_print = [1, 1, 0, -1, -1, -1, -1, 1, 1, -1, 0, 1, -1, 0, -1, 0, 1, 0, -1, -1, -1, -1, -1, -1]


# function that runs all strains for each process
def run_process(process, process_tag):
    #   3. Ecoli - Full - DTA
    #   4. Ecoli - Min - WT
    #   5. Ecoli - Min - DTA/DL
    #   6. Ecoli - Min - DTA
    #   7. Salmonella - Full - WT
    #   8. Salmonella - Full - DTA
    #   9. Salmonella - Full - DTA/IL
    #   10. Salmonella - Min - WT
    #   11. Salmonella - Min - DTA
    #   12. Salmonella - Min - DTA/IL
    # cols = ["Ecoli_Full_Process", "Ecoli_Min_Process", "Salmonella_Full_Process", "Salmonella_Min_Process",
    #         "Ecoli_Full_WT", "Ecoli_Full_DTA/DL", "Ecoli_Full_DTA",
    #         "Ecoli_Min_WT", "Ecoli_Min_DTA/DL", "Ecoli_Min_DTA",
    #         "Salmonella_Full_WT", "Salmonella_Full_DTA", "Salmonella_Full_DTA/IL",
    #         "Salmonella_Min_WT", "Salmonella_Min_DTA", "Salmonella_Min_DTA/IL"]
    # Make the data frame and start the row with the process markers
    row = [process_tag, process_tag, process_tag, process_tag]
    for i in range(12):
        circuit = process(strains[i])
        circuit.run(1000)
        # add the end value to the row
        row.append(circuit.local.environments["Yellow"])
    # add row to the data frame
    full_row = np.array(row)
    # return the data frame
    return full_row


# loop to run through all process sets and form a single data frame and save to file
def process_set_run(outputfile=""):
    processes = [cs.RT_LL_circuit, cs.RT_CR_circuit, cs.RT_LL_CR_circuit, cs.RT_circuit,
                 cs.SC_LL_circuit, cs.SC_CR_circuit, cs.SC_LL_CR_circuit, cs.SC_circuit,
                 cs.RT_SC_LL_circuit, cs.RT_SC_CR_circuit, cs.RT_SC_LL_CR_circuit, cs.RT_SC_circuit,
                 cs.LL_circuit, cs.CR_circuit, cs.LL_CR_circuit, cs.None_circuit]
    cols = ["Ecoli_Full_Process", "Ecoli_Min_Process", "Salmonella_Full_Process", "Salmonella_Min_Process",
            "Ecoli_Full_WT", "Ecoli_Full_DTA/DL", "Ecoli_Full_DTA",
            "Ecoli_Min_WT", "Ecoli_Min_DTA/DL", "Ecoli_Min_DTA",
            "Salmonella_Full_WT", "Salmonella_Full_DTA", "Salmonella_Full_DTA/IL",
            "Salmonella_Min_WT", "Salmonella_Min_DTA", "Salmonella_Min_DTA/IL"]
    # Make the data frame
    df = pd.DataFrame(columns=cols)
    for i in range(len(processes)):
        new_row = run_process(processes[i], i)
        df.loc[len(df.index)] = new_row
    df.to_csv(outputfile + "Process_Circuits_Run.csv", index=False)


def compare(a, b):
    """
    Takes lists of bacterium, promoter and strain for two different sets and compares the mhYFP_by_A600 values.
    Parameters
    ----------
    a   : float
        first value
    b   : float
        second value

    Returns
    -------
    int
        1 if a greater than b, -1 if a less than b, 0 if no significant difference

    """
    if a * 0.95 > b * 1.05:
        return 1
    elif b * 0.95 > a * 1.05:
        return -1
    else:
        return 0


# finger print generator
def finger_print(row):
    # Ecoli min
    ecoli_min = [compare(row["Ecoli_Min_WT"], row["Ecoli_Min_DTA/DL"]),
                 compare(row["Ecoli_Min_WT"], row["Ecoli_Min_DTA"]),
                 compare(row["Ecoli_Min_DTA/DL"], row["Ecoli_Min_DTA"])]

    # Ecoli full
    ecoli_full = [compare(row["Ecoli_Full_WT"], row["Ecoli_Full_DTA/DL"]),
                  compare(row["Ecoli_Full_WT"], row["Ecoli_Full_DTA"]),
                  compare(row["Ecoli_Full_DTA/DL"], row["Ecoli_Full_DTA"])]

    # Salmonella min
    salmonella_min = [compare(row["Salmonella_Min_WT"], row["Salmonella_Min_DTA"]),
                      compare(row["Salmonella_Min_WT"], row["Salmonella_Min_DTA/IL"]),
                      compare(row["Salmonella_Min_DTA"], row["Salmonella_Min_DTA/IL"])]

    # Salmonella full
    salmonella_full = [compare(row["Salmonella_Full_WT"], row["Salmonella_Full_DTA"]),
                       compare(row["Salmonella_Full_WT"], row["Salmonella_Full_DTA/IL"]),
                       compare(row["Salmonella_Full_DTA"], row["Salmonella_Full_DTA/IL"])]

    # WT Comparison (same bacteria or same promoter)
    WT_comps = [compare(row["Ecoli_Min_WT"], row["Ecoli_Full_WT"]),
                compare(row["Salmonella_Min_WT"], row["Salmonella_Full_WT"]),
                compare(row["Ecoli_Min_WT"], row["Salmonella_Min_WT"]),
                compare(row["Ecoli_Full_WT"], row["Salmonella_Full_WT"])]

    # No topA and No Lac Comparison (same bacteria or same promoter)
    No_topA_No_Lac_comps = [compare(row["Ecoli_Min_DTA/DL"], row["Ecoli_Full_DTA/DL"]),
                            compare(row["Salmonella_Min_DTA"], row["Salmonella_Full_DTA"]),
                            compare(row["Ecoli_Min_DTA/DL"], row["Salmonella_Min_DTA"]),
                            compare(row["Ecoli_Full_DTA/DL"], row["Salmonella_Full_DTA"])]

    # No topA and Lac Comparison (same bacteria or same promoter)
    No_topA_Lac_comps = [compare(row["Ecoli_Min_DTA"], row["Ecoli_Full_DTA"]),
                         compare(row["Salmonella_Min_DTA/IL"], row["Salmonella_Full_DTA/IL"]),
                         compare(row["Ecoli_Min_DTA"], row["Salmonella_Min_DTA/IL"]),
                         compare(row["Ecoli_Full_DTA"], row["Salmonella_Full_DTA/IL"])]

    # Form "fingerprints"
    row_finger_print = (ecoli_full + salmonella_full + ecoli_min + salmonella_min + WT_comps + No_topA_No_Lac_comps +
                        No_topA_Lac_comps)
    return row_finger_print


# distance measure with bio fingerprint
def finger_print_distance(row):
    dist = 0
    fp = finger_print(row)
    for (bio, comp) in zip(bio_finger_print, fp):
        dist = dist + abs(bio - comp)
    return dist


def add_combos(df):
    combos = pd.DataFrame(columns=["Ecoli_Full_Process", "Ecoli_Min_Process", "Salmonella_Full_Process",
                                   "Salmonella_Min_Process",
                                   "Ecoli_Full_WT", "Ecoli_Full_DTA/DL", "Ecoli_Full_DTA",
                                   "Ecoli_Min_WT", "Ecoli_Min_DTA/DL", "Ecoli_Min_DTA",
                                   "Salmonella_Full_WT", "Salmonella_Full_DTA", "Salmonella_Full_DTA/IL",
                                   "Salmonella_Min_WT", "Salmonella_Min_DTA", "Salmonella_Min_DTA/IL"])
    for r_EF in df.iterrows():
        # Ecoli Full process
        row_EF = r_EF[1]
        tags_1 = [row_EF["Ecoli_Full_Process"]]
        values_1 = [row_EF["Ecoli_Full_WT"], row_EF["Ecoli_Full_DTA/DL"], row_EF["Ecoli_Full_DTA"]]
        for r_EM in df.iterrows():
            # Ecoli min process
            row_EM = r_EM[1]
            tags_2 = tags_1 + [row_EM["Ecoli_Min_Process"]]
            values_2 = values_1 + [row_EM["Ecoli_Min_WT"], row_EM["Ecoli_Min_DTA/DL"], row_EM["Ecoli_Min_DTA"]]
            for r_SF in df.iterrows():
                # Salmonella full process
                row_SF = r_SF[1]
                tags_3 = tags_2 + [row_SF["Salmonella_Full_Process"]]
                values_3 = values_2 + [row_SF["Salmonella_Full_WT"], row_SF["Salmonella_Full_DTA"],
                                       row_SF["Salmonella_Full_DTA/IL"]]
                for r_SM in df.iterrows():
                    # Salmonella min process
                    row_SM = r_SM[1]
                    if not (row_EF.all() == row_EM.all()
                            and row_EF.all() == row_SM.all()
                            and row_EF.all() == row_SF.all()):
                        tags_4 = tags_3 + [row_SM["Ecoli_Min_Process"]]
                        values_4 = values_3 + [row_SM["Salmonella_Min_WT"], row_SM["Salmonella_Min_DTA"],
                                               row_SM["Salmonella_Min_DTA/IL"]]
                        new_row = tags_4 + values_4
                        combos.loc[len(combos.index)] = new_row
    # add_dist_col(combos)
    df = pd.concat([df, combos], ignore_index=True, sort=False)
    add_dist_col(df)
    return df


def combo_graphs(df, strain):
    # add columns for each ind process with booleans for process being used (for this set).
    graph_data = df.copy()
    graph_data["Lac Loop"] = [(x in process_split["Lac Loop"][0]) for x in df[strain].to_list()]
    graph_data["Lac Canonical Repression"] = [(x in process_split["Lac Canonical Repression"][0])
                                              for x in df[strain].to_list()]
    graph_data["Anti-tet Supercoiling"] = [(x in process_split["Anti-tet Supercoiling"][0])
                                           for x in df[strain].to_list()]
    graph_data["Anti-tet Read through"] = [(x in process_split["Anti-tet Read through"][0])
                                           for x in df[strain].to_list()]
    LL = sns.catplot(graph_data, x="Lac Loop", y='fp_dist', kind='box')
    LCR = sns.catplot(graph_data, x="Lac Canonical Repression", y='fp_dist', kind='box')
    AS = sns.catplot(graph_data, x="Anti-tet Supercoiling", y='fp_dist', kind='box')
    ART = sns.catplot(graph_data, x="Anti-tet Read through", y='fp_dist', kind='box')
    # TODO: save the plots with the strain name and the process for each plot
    LL.figure.savefig(strain + "_Lac_Loop_Boxplot.png")
    LCR.figure.savefig(strain + "_Lac_Canonical_Repression_Boxplot.png")
    AS.figure.savefig(strain + "_Antitet_Supercoiling_Boxplot.png")
    ART.figure.savefig(strain + "_Antitet_Readthrough_Boxplot.png")


# function to add distance column to data frame
def add_dist_col(df):
    df['fp_dist'] = df.apply(finger_print_distance, axis=1)


if __name__ == "__main__":
    # process_set_run()
    data = pd.read_csv("Process_Circuits_Run.csv")
    # add_dist_col(data)
    data = add_combos(data)
    data.to_csv("Full_Combined_Process_Circuit_Results.csv", index=False)
    # data = pd.read_csv("Full_Combined_Process_Circuit_Results.csv", index_col=None)
    combo_graphs(data, "Salmonella_Full_Process")
    pass
