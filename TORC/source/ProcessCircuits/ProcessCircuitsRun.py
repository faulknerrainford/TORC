import pandas as pd
import numpy as np
import seaborn as sns
import collections as coll
import matplotlib.pyplot as plt

from TORC import CircuitSetups as cs

# Set up parameter sets for each of 12 strains as a list
# (alternative parameters available in Salmonella_Parameters file)
# Salmonella Topo effects
relax_WT_Salmonella = 0.7152736182204096  # 0.9532908145
relax_DTA_Salmonella = 0.2196310757689402  # 0.1768535622

# Supercoiling values
tetA_sc = -0.05
mhYFP_sc = 0.0030446120261538  # 0.003512001343

# Full promoter
pleuWT_sigmoid_full = -0.0730438758968655  # -0.114657413
gradient_full = 0.0818199620246661  # 0.7267593004
# Output Salmonella
mhYFP_min_pfull_s = 19.937824715727697  # 0.1999758818
mhYFP_max_pfull_s = 23.6265774724979  # 60.40914739

# Min promoter
pleuWT_sigmoid_min = -0.0871953987185861  # -0.1113355055
gradient_min = 0.1284585318724667  # 0.7438187636
# Output Salmonella
mhYFP_min_pmin_s = 18.496844452749595  # 2.372331873
mhYFP_max_pmin_s = 21.765110326714744  # 58.71513799

# Topo effects E.coli
relax_WT_ecoli = 0.9060040144
relax_DTA_ecoli = 0.00066505304

# Output
mhYFP_min_pfull_e = 0.03495783141
mhYFP_max_pfull_e = 47.30393081

# Output
mhYFP_min_pmin_e = 0.4587873903
mhYFP_max_pmin_e = 37.25162462

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

# Mean based fingerprint
# bio_finger_print = [1, 1, 0, -1, -1, -1, -1, 1, 1, -1, 0, 1, -1, 0, -1, 0, 1, 0, -1, -1, -1, -1, -1, -1]

# Median based fingerprint
bio_finger_print = [1, 1, 0, -1, -1, 0, -1, 1, 1, -1, 0, 1, -1, 0, -1, 0, 1, 0, -1, -1, -1, -1, -1, -1]
salmonella_bio_finger_print = [-1, -1, 0, -1, 0, 1, 0, 0, -1]

# Strain only fingerprints
# (ecoli_full + salmonella_full + ecoli_min + salmonella_min + WT_comps + No_topA_No_Lac_comps +
#                         No_topA_Lac_comps)
salmonella_full_only_fp = bio_finger_print[3:6]
salmonella_min_only_fp = bio_finger_print[9:12]
ecoli_full_only_fp = bio_finger_print[0:3]
ecoli_min_only_fp = bio_finger_print[6:9]

# Strain focused fingerprints
salmonella_full_focus_fp = (bio_finger_print[3:6] + [bio_finger_print[13], bio_finger_print[15], bio_finger_print[17],
                            bio_finger_print[19], bio_finger_print[21], bio_finger_print[23]])
salmonella_min_focus_fp = (bio_finger_print[6:9] + [bio_finger_print[13], bio_finger_print[14], bio_finger_print[17],
                           bio_finger_print[18], bio_finger_print[21], bio_finger_print[22]])
ecoli_full_focus_fp = (bio_finger_print[0:3] + [bio_finger_print[12], bio_finger_print[15], bio_finger_print[16],
                       bio_finger_print[19], bio_finger_print[20], bio_finger_print[23]])
ecoli_min_focus_fp = (bio_finger_print[9:12] + [bio_finger_print[12], bio_finger_print[14], bio_finger_print[16],
                      bio_finger_print[18], bio_finger_print[20], bio_finger_print[22]])
salmonella_full_focus_fp_no_ecoli = (bio_finger_print[3:6] + [bio_finger_print[13], bio_finger_print[17], bio_finger_print[21]])
salmonella_min_focus_fp_no_ecoli = (bio_finger_print[9:12] + [bio_finger_print[13], bio_finger_print[17], bio_finger_print[21]])

bio_finger_prints = [salmonella_full_only_fp, salmonella_min_only_fp, ecoli_full_only_fp, ecoli_min_only_fp,
                     salmonella_full_focus_fp, salmonella_min_focus_fp, ecoli_full_focus_fp, ecoli_min_focus_fp]
salmonella_bio_finger_prints = [[salmonella_full_only_fp, salmonella_min_only_fp,
                                 salmonella_full_focus_fp_no_ecoli, salmonella_min_focus_fp_no_ecoli]]


# function that runs all strains for each process
def run_process(process, process_tag, skip_ecoli=False, promoter_type="sigmoid"):
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
    if skip_ecoli:
        row = [process_tag, process_tag]
    else:
        row = [process_tag, process_tag, process_tag, process_tag]
    set_size = 6 if skip_ecoli else 12
    for i in range(set_size):
        if skip_ecoli:
            strain = strains[i+6] + [promoter_type]
            circuit = process(strain)
        else:
            strain = strains[i] + [promoter_type]
            circuit = process(strain)
        circuit.run(1000)
        # add the end value to the row
        row.append(circuit.local.environments["Yellow"])
    # add row to the data frame
    full_row = np.array(row)
    # return the data frame
    return full_row


# loop to run through all process sets and form a single data frame and save to file
def process_set_run(outputfile="", skip_ecoli=False, promoter_type="sigmoid"):
    processes = [cs.RT_LL_circuit, cs.RT_CR_circuit, cs.RT_LL_CR_circuit, cs.RT_circuit,
                 cs.SC_LL_circuit, cs.SC_CR_circuit, cs.SC_LL_CR_circuit, cs.SC_circuit,
                 cs.RT_SC_LL_circuit, cs.RT_SC_CR_circuit, cs.RT_SC_LL_CR_circuit, cs.RT_SC_circuit,
                 cs.LL_circuit, cs.CR_circuit, cs.LL_CR_circuit, cs.None_circuit]
    if skip_ecoli:
        cols = ["Salmonella_Full_Process", "Salmonella_Min_Process",
                "Salmonella_Full_WT", "Salmonella_Full_DTA", "Salmonella_Full_DTA/IL",
                "Salmonella_Min_WT", "Salmonella_Min_DTA", "Salmonella_Min_DTA/IL"]
    else:
        cols = ["Ecoli_Full_Process", "Ecoli_Min_Process", "Salmonella_Full_Process", "Salmonella_Min_Process",
                "Ecoli_Full_WT", "Ecoli_Full_DTA/DL", "Ecoli_Full_DTA",
                "Ecoli_Min_WT", "Ecoli_Min_DTA/DL", "Ecoli_Min_DTA",
                "Salmonella_Full_WT", "Salmonella_Full_DTA", "Salmonella_Full_DTA/IL",
                "Salmonella_Min_WT", "Salmonella_Min_DTA", "Salmonella_Min_DTA/IL"]
    # Make the data frame
    df = pd.DataFrame(columns=cols)
    for i in range(len(processes)):
        new_row = run_process(processes[i], i, skip_ecoli, promoter_type)
        df.loc[len(df.index)] = new_row
    df.to_csv(outputfile + "Median_Process_Circuits_Run.csv", index=False)


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
    if "Ecoli_Min_WT" in row.index:
        ecoli_min = [compare(row["Ecoli_Min_WT"], row["Ecoli_Min_DTA/DL"]),
                     compare(row["Ecoli_Min_WT"], row["Ecoli_Min_DTA"]),
                     compare(row["Ecoli_Min_DTA/DL"], row["Ecoli_Min_DTA"])]
    else:
        ecoli_min = None

    # Ecoli full
    if "Ecoli_Full_WT" in row.index:
        ecoli_full = [compare(row["Ecoli_Full_WT"], row["Ecoli_Full_DTA/DL"]),
                      compare(row["Ecoli_Full_WT"], row["Ecoli_Full_DTA"]),
                      compare(row["Ecoli_Full_DTA/DL"], row["Ecoli_Full_DTA"])]
    else:
        ecoli_full = None

    # Salmonella min
    salmonella_min = [compare(row["Salmonella_Min_WT"], row["Salmonella_Min_DTA"]),
                      compare(row["Salmonella_Min_WT"], row["Salmonella_Min_DTA/IL"]),
                      compare(row["Salmonella_Min_DTA"], row["Salmonella_Min_DTA/IL"])]

    # Salmonella full
    salmonella_full = [compare(row["Salmonella_Full_WT"], row["Salmonella_Full_DTA"]),
                       compare(row["Salmonella_Full_WT"], row["Salmonella_Full_DTA/IL"]),
                       compare(row["Salmonella_Full_DTA"], row["Salmonella_Full_DTA/IL"])]

    # WT Comparison (same bacteria or same promoter)
    if "Ecoli_Full_WT" in row.index:
        WT_comps = [compare(row["Ecoli_Min_WT"], row["Ecoli_Full_WT"]),
                    compare(row["Salmonella_Min_WT"], row["Salmonella_Full_WT"]),
                    compare(row["Ecoli_Min_WT"], row["Salmonella_Min_WT"]),
                    compare(row["Ecoli_Full_WT"], row["Salmonella_Full_WT"])]
    else:
        WT_comps = [compare(row["Salmonella_Min_WT"], row["Salmonella_Full_WT"])]

    # No topA and No Lac Comparison (same bacteria or same promoter)
    if "Ecoli_Min_DTA/DL" in row.index:
        No_topA_No_Lac_comps = [compare(row["Ecoli_Min_DTA/DL"], row["Ecoli_Full_DTA/DL"]),
                                compare(row["Salmonella_Min_DTA"], row["Salmonella_Full_DTA"]),
                                compare(row["Ecoli_Min_DTA/DL"], row["Salmonella_Min_DTA"]),
                                compare(row["Ecoli_Full_DTA/DL"], row["Salmonella_Full_DTA"])]
    else:
        No_topA_No_Lac_comps = [compare(row["Salmonella_Min_DTA"], row["Salmonella_Full_DTA"])]

    # No topA and Lac Comparison (same bacteria or same promoter)
    if "Ecoli_Min_DTA" in row.index:
        No_topA_Lac_comps = [compare(row["Ecoli_Min_DTA"], row["Ecoli_Full_DTA"]),
                             compare(row["Salmonella_Min_DTA/IL"], row["Salmonella_Full_DTA/IL"]),
                             compare(row["Ecoli_Min_DTA"], row["Salmonella_Min_DTA/IL"]),
                             compare(row["Ecoli_Full_DTA"], row["Salmonella_Full_DTA/IL"])]
    else:
        No_topA_Lac_comps = [compare(row["Salmonella_Min_DTA/IL"], row["Salmonella_Full_DTA/IL"])]

    # Form "fingerprints"
    if "Ecoli_Full_WT" in row.index:
        row_finger_print = (ecoli_full + salmonella_full + ecoli_min + salmonella_min + WT_comps + No_topA_No_Lac_comps +
                            No_topA_Lac_comps)
    else:
        row_finger_print = (salmonella_full + salmonella_min + WT_comps + No_topA_No_Lac_comps + No_topA_Lac_comps)
    return row_finger_print


# distance measure with bio fingerprint
def finger_print_distance_vector(row):
    dist = []
    fp = finger_print(row)
    if len(fp) < len(bio_finger_print):
        bio_fp = salmonella_bio_finger_print
    else:
        bio_fp = bio_finger_print

    for (bio, comp) in zip(bio_fp, fp):
        dist.append(abs(bio - comp))
    return dist


def finger_print_distance(row):
    dists = finger_print_distance_vector(row)
    return sum(dists)


def fp_dist_df(df):
    # get columns needed from full df
    dist_df = df.iloc[:, :16]
    # get finger print per row
    dist_df['fp_dist_vector'] = dist_df.apply(lambda row: finger_print_distance_vector(row), axis=1)
    # get frequency of different error levels
    comps = [coll.Counter((v[x] for v in dist_df['fp_dist_vector'])) for x in range(24)]
    # gen graph and then add tick labels
    matches = [comp[0] for comp in comps]
    matches = np.array(matches)
    small_mismatch = [comp[1] for comp in comps]
    small_mismatch = np.array(small_mismatch)
    big_mismatch = [comp[2] for comp in comps]
    big_mismatch = np.array(big_mismatch)
    print(matches)
    print(small_mismatch)
    print(big_mismatch)
    x_labels = ['EF_WT_DTADL', 'EF_WT_DTA', 'EF_DTADL_DTA',
                'SF_WT_DTA', 'SF_WT_DTAIL', 'SF_DTA_DTAIL',
                'EM_WT_DTADL', 'EM_WT_DTA', 'EM_DTADL_DTA',
                'SM_WT_DTA', 'SM_WT_DTAIL', 'SM_DTA_DTAIL',
                'WT_EM_EF', 'WT_SM_SF', 'WT_EM_SM', 'WT_EF_SF',
                'NTANL_EM_EF', 'NTANL_SM_SF', 'NTANL_EM_SM', 'NTANL_EF_SF',
                'NTA_EM_EF', 'NTA_SM_SF', 'NTA_EM_SM', 'NTA_EF_SF',
                ]
    # plt.bar(x_labels, matches, color='g')
    # plt.bar(x_labels, small_mismatch, bottom=matches, color='y')
    # plt.bar(x_labels, big_mismatch, bottom=matches+small_mismatch, color='r')
    # plt.xticks(rotation=90)
    # plt.savefig("FingerPrintMedianPlot.png", bbox_inches='tight')
    # # plt.show()
    return dist_df


def comp_process_frequency(df):
    # take dist df and separate into df columns based on relevance to comps
    # Start with top A knockout salmonella comparison and work up graph then attempt to generate for all
    #  comparison
    Bacteria = ["Salmonella", "Ecoli"]
    Bacteria_indexes = [(21, 17, 13), (20, 16, 12)]
    comps = ['NTA_comp', 'NTANL_comp', 'WT_comp']
    for (B, inds) in zip(Bacteria, Bacteria_indexes):
        topAB_df = df[[B+'_Full_Process', B+'_Min_Process', 'fp_dist_vector']].copy()
        for (i, comp) in zip(inds, comps):
            topAB_df[comp] = [row[i] for row in df['fp_dist_vector']]
            matched = topAB_df[topAB_df[comp] == 0]
            small_error = topAB_df[topAB_df[comp] == 1]
            big_error = topAB_df[topAB_df[comp] == 2]
            # get uniques of each process
            print(comp+" "+B+" Full")
            print(matched[B+'_Full_Process'].unique())
            print(small_error[B+'_Full_Process'].unique())
            print(big_error[B+'_Full_Process'].unique())
            print(comp+" "+B+" Min")
            print(matched[B+'_Min_Process'].unique())
            print(small_error[B+'_Min_Process'].unique())
            print(big_error[B+'_Min_Process'].unique())
    # Repeat print outs with Promoter instead of the bacteria
    Promoter = ['Full', 'Min']
    Promoter_indexes = [(23, 19, 15), (22, 18, 14)]
    for (P, inds) in zip(Promoter, Promoter_indexes):
        topAP_df = df[["Salmonella_"+P+"_Process", 'Ecoli_'+P+'_Process', 'fp_dist_vector']].copy()
        for (i, comp) in zip(inds, comps):
            topAP_df[comp] = [row[i] for row in df['fp_dist_vector']]
            matched = topAP_df[topAP_df[comp] == 0]
            small_error = topAP_df[topAP_df[comp] == 1]
            big_error = topAP_df[topAP_df[comp] == 2]
            # get uniques for each process
            print(comp + " Salmonella " + P)
            print(matched["Salmonella_" + P + '_Process'].unique())
            print(small_error["Salmonella_" + P + '_Process'].unique())
            print(big_error["Salmonella_" + P + '_Process'].unique())
            print(comp + " Ecoli " + P)
            print(matched["Ecoli_" + P + '_Process'].unique())
            print(small_error["Ecoli_" + P + '_Process'].unique())
            print(big_error["Ecoli_" + P + '_Process'].unique())
    # TODO: Same again for individual strains
    Strain = ['Salmonella_Min', 'Salmonella_Full', 'Ecoli_Min', 'Ecoli_Full']
    Strain_indexes = [(9, 10, 11), (3, 4, 5), (6, 7, 8), (0, 1, 2)]
    Strain_comps = ['WT_NTANL', 'WT_NTA', 'NTA_NTANL']
    for (S, inds) in zip(Strain, Strain_indexes):
        comp_df = df[[S+'_Process', 'fp_dist_vector']].copy()
        for (i, comp) in zip(inds, Strain_comps):
            comp_df[comp] = [row[i] for row in df['fp_dist_vector']]
            matched = comp_df[comp_df[comp] == 0]
            small_error = comp_df[comp_df[comp] == 1]
            big_error = comp_df[comp_df[comp] == 2]
            print(comp + '_' + S)
            print(matched[S + '_Process'].unique())
            print(small_error[S + '_Process'].unique())
            print(big_error[S + '_Process'].unique())


# finger print generator
def strain_finger_prints(row):
    # Set up the individual fingerprints for each strain
    # Ecoli min
    if "Ecoli_Min_WT" in row.index:
        ecoli_min = [compare(row["Ecoli_Min_WT"], row["Ecoli_Min_DTA/DL"]),
                     compare(row["Ecoli_Min_WT"], row["Ecoli_Min_DTA"]),
                     compare(row["Ecoli_Min_DTA/DL"], row["Ecoli_Min_DTA"])]
    else:
        ecoli_min = None

    # Ecoli full
    if "Ecoli_Full_WT" in row.index:
        ecoli_full = [compare(row["Ecoli_Full_WT"], row["Ecoli_Full_DTA/DL"]),
                      compare(row["Ecoli_Full_WT"], row["Ecoli_Full_DTA"]),
                      compare(row["Ecoli_Full_DTA/DL"], row["Ecoli_Full_DTA"])]
    else:
        ecoli_full = None

    # Salmonella min
    salmonella_min = [compare(row["Salmonella_Min_WT"], row["Salmonella_Min_DTA"]),
                      compare(row["Salmonella_Min_WT"], row["Salmonella_Min_DTA/IL"]),
                      compare(row["Salmonella_Min_DTA"], row["Salmonella_Min_DTA/IL"])]

    # Salmonella full
    salmonella_full = [compare(row["Salmonella_Full_WT"], row["Salmonella_Full_DTA"]),
                       compare(row["Salmonella_Full_WT"], row["Salmonella_Full_DTA/IL"]),
                       compare(row["Salmonella_Full_DTA"], row["Salmonella_Full_DTA/IL"])]

    # WT Comparison (same bacteria or same promoter)

    if "Ecoli_Min_WT" in row.index:
        WT_comps = [compare(row["Ecoli_Min_WT"], row["Ecoli_Full_WT"]),
                    compare(row["Salmonella_Min_WT"], row["Salmonella_Full_WT"]),
                    compare(row["Ecoli_Min_WT"], row["Salmonella_Min_WT"]),
                    compare(row["Ecoli_Full_WT"], row["Salmonella_Full_WT"])]
    else:
        WT_comps = [compare(row["Salmonella_Min_WT"], row["Salmonella_Full_WT"])]

    # No topA and No Lac Comparison (same bacteria or same promoter)
    if "Ecoli_Min_WT" in row.index:
        No_topA_No_Lac_comps = [compare(row["Ecoli_Min_DTA/DL"], row["Ecoli_Full_DTA/DL"]),
                                compare(row["Salmonella_Min_DTA"], row["Salmonella_Full_DTA"]),
                                compare(row["Ecoli_Min_DTA/DL"], row["Salmonella_Min_DTA"]),
                                compare(row["Ecoli_Full_DTA/DL"], row["Salmonella_Full_DTA"])]
    else:
        No_topA_No_Lac_comps = [compare(row["Salmonella_Min_DTA"], row["Salmonella_Full_DTA"])]

    # No topA and Lac Comparison (same bacteria or same promoter)
    if "Ecoli_Min_WT" in row.index:
        No_topA_Lac_comps = [compare(row["Ecoli_Min_DTA"], row["Ecoli_Full_DTA"]),
                             compare(row["Salmonella_Min_DTA/IL"], row["Salmonella_Full_DTA/IL"]),
                             compare(row["Ecoli_Min_DTA"], row["Salmonella_Min_DTA/IL"]),
                             compare(row["Ecoli_Full_DTA"], row["Salmonella_Full_DTA/IL"])]
    else:
        No_topA_Lac_comps = [compare(row["Salmonella_Min_DTA/IL"], row["Salmonella_Full_DTA/IL"])]

    # Form "fingerprints"
    # form multiple strain fingerprints (all eight)
    sf_fp_only = salmonella_full
    sm_fp_only = salmonella_min
    ef_fp_only = ecoli_full
    em_fp_only = ecoli_min
    if "Ecoli_Min_WT" in row.index:
        sf_fp_focus = salmonella_full + [WT_comps[1], WT_comps[3], No_topA_No_Lac_comps[1], No_topA_No_Lac_comps[3],
                                         No_topA_Lac_comps[1], No_topA_Lac_comps[3]]
        sm_fp_focus = salmonella_min + [WT_comps[1], WT_comps[2], No_topA_No_Lac_comps[1], No_topA_No_Lac_comps[2],
                                        No_topA_Lac_comps[1], No_topA_Lac_comps[2]]
    else:
        sf_fp_focus = salmonella_full + [WT_comps[0], No_topA_No_Lac_comps[0], No_topA_Lac_comps[0]]
        sm_fp_focus = salmonella_min + [WT_comps[0], No_topA_No_Lac_comps[0], No_topA_Lac_comps[0]]
    if "Ecoli_Min_WT" in row.index:
        ef_fp_focus = ecoli_full + [WT_comps[0], WT_comps[3], No_topA_No_Lac_comps[0], No_topA_No_Lac_comps[3],
                                    No_topA_Lac_comps[0], No_topA_Lac_comps[3]]
        em_fp_focus = ecoli_min + [WT_comps[0], WT_comps[2], No_topA_No_Lac_comps[0], No_topA_No_Lac_comps[2],
                                   No_topA_Lac_comps[0], No_topA_Lac_comps[2]]
        return sf_fp_only, sm_fp_only, ef_fp_only, em_fp_only, sf_fp_focus, sm_fp_focus, ef_fp_focus, em_fp_focus
    else:
        return sf_fp_only, sm_fp_only, sf_fp_focus, sm_fp_focus


# distance measure with bio fingerprint
def strain_finger_print_distances(row, skip_ecoli=False):
    # get the distances for the individual strain fingerprints add focused and only version
    dists = []
    strain_fps = strain_finger_prints(row)
    if skip_ecoli:
        bfp = salmonella_bio_finger_prints
    else:
        bfp = bio_finger_prints
    # compare each print with bio and get 4 dists to return
    for (strain_fp, bio_fp) in zip(strain_fps, bfp):
        dist = 0
        for (bio, comp) in zip(bio_fp, strain_fp):
            dist = dist + abs(bio - comp)
        dists.append(dist)
    return dists


def add_combos(df, skip_ecoli=False):
    if skip_ecoli:
        combos = pd.DataFrame(columns=["Salmonella_Full_Process", "Salmonella_Min_Process",
                                       "Salmonella_Full_WT", "Salmonella_Full_DTA", "Salmonella_Full_DTA/IL",
                                       "Salmonella_Min_WT", "Salmonella_Min_DTA", "Salmonella_Min_DTA/IL"])
    else:
        combos = pd.DataFrame(columns=["Ecoli_Full_Process", "Ecoli_Min_Process", "Salmonella_Full_Process",
                                       "Salmonella_Min_Process",
                                       "Ecoli_Full_WT", "Ecoli_Full_DTA/DL", "Ecoli_Full_DTA",
                                       "Ecoli_Min_WT", "Ecoli_Min_DTA/DL", "Ecoli_Min_DTA",
                                       "Salmonella_Full_WT", "Salmonella_Full_DTA", "Salmonella_Full_DTA/IL",
                                       "Salmonella_Min_WT", "Salmonella_Min_DTA", "Salmonella_Min_DTA/IL"])

    if not skip_ecoli:
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
                            tags_4 = tags_3 + [row_SM["Salmonella_Min_Process"]]
                            values_4 = values_3 + [row_SM["Salmonella_Min_WT"], row_SM["Salmonella_Min_DTA"],
                                                   row_SM["Salmonella_Min_DTA/IL"]]
                            new_row = tags_4 + values_4
                            combos.loc[len(combos.index)] = new_row
    else:
        for r_SF in df.iterrows():
            # Salmonella full process
            row_SF = r_SF[1]
            tags_3 = [row_SF["Salmonella_Full_Process"]]
            values_3 = [row_SF["Salmonella_Full_WT"], row_SF["Salmonella_Full_DTA"], row_SF["Salmonella_Full_DTA/IL"]]
            for r_SM in df.iterrows():
                # Salmonella min process
                row_SM = r_SM[1]
                if not (row_SF.all() == row_SM.all()):
                    tags_4 = tags_3 + [row_SM["Salmonella_Min_Process"]]
                    values_4 = values_3 + [row_SM["Salmonella_Min_WT"], row_SM["Salmonella_Min_DTA"],
                                           row_SM["Salmonella_Min_DTA/IL"]]
                    new_row = tags_4 + values_4
                    combos.loc[len(combos.index)] = new_row
    # add_dist_col(combos)
    df = pd.concat([df, combos], ignore_index=True, sort=False)
    add_dist_col(df)
    add_strain_dist_cols(df)
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
    LL = sns.catplot(graph_data, x="Lac Loop", y='fp_dist', kind='violin')
    LCR = sns.catplot(graph_data, x="Lac Canonical Repression", y='fp_dist', kind='violin')
    AS = sns.catplot(graph_data, x="Anti-tet Supercoiling", y='fp_dist', kind='violin')
    ART = sns.catplot(graph_data, x="Anti-tet Read through", y='fp_dist', kind='violin')
    # save the plots with the strain name and the process for each plot
    LL.figure.savefig(strain + "_Lac_Loop_Violin.png")
    LCR.figure.savefig(strain + "_Lac_Canonical_Repression_Violin.png")
    AS.figure.savefig(strain + "_Antitet_Supercoiling_Violin.png")
    ART.figure.savefig(strain + "_Antitet_Readthrough_Violin.png")


def strain_graphs(df, strain):
    # add columns for each ind process with booleans for process being used (for this set).
    # TODO: adapt to produce graphs of processes for the individual stains (possibly just the one graph of the different
    #  process sets
    graph_data = df.copy()
    # TODO: graph for each strain of distance based on process/process combo
    graph_data["Lac Loop"] = [(x in process_split["Lac Loop"][0]) for x in df[strain].to_list()]
    graph_data["Lac Canonical Repression"] = [(x in process_split["Lac Canonical Repression"][0])
                                              for x in df[strain].to_list()]
    graph_data["Anti-tet Supercoiling"] = [(x in process_split["Anti-tet Supercoiling"][0])
                                           for x in df[strain].to_list()]
    graph_data["Anti-tet Read through"] = [(x in process_split["Anti-tet Read through"][0])
                                           for x in df[strain].to_list()]
    LL = sns.catplot(graph_data, x="Lac Loop", y='fp_dist', kind='violin')
    LCR = sns.catplot(graph_data, x="Lac Canonical Repression", y='fp_dist', kind='violin')
    AS = sns.catplot(graph_data, x="Anti-tet Supercoiling", y='fp_dist', kind='violin')
    ART = sns.catplot(graph_data, x="Anti-tet Read through", y='fp_dist', kind='violin')
    # save the plots with the strain name and the process for each plot
    LL.figure.savefig(strain + "_Lac_Loop_Violin.png")
    LCR.figure.savefig(strain + "_Lac_Canonical_Repression_Violin.png")
    AS.figure.savefig(strain + "_Antitet_Supercoiling_Violin.png")
    ART.figure.savefig(strain + "_Antitet_Readthrough_Violin.png")


# function to add distance column to data frame
def add_dist_col(df):
    df['fp_dist'] = df.apply(finger_print_distance, axis=1)


def add_strain_dist_cols(df):
    # set up for the set of strains rather than the full version, need to resolve multiple returns from apply
    #  statement to multiple columns
    df['ind_dist'] = df.apply(strain_finger_print_distances, axis=1)
    if 'Ecoli_Min_Process' in df.columns:
        (df['sf_only_dist'], df['sm_only_dist'],
         df['ef_only_dist'], df['em_only_dist'],
         df['sf_focus_dist'], df['sm_focus_dist'],
         df['ef_focus_dist'], df['em_focus_dist']) = zip(*df['ind_dist'].to_list())
    else:
        (df['sf_only_dist'], df['sm_only_dist'],
         df['sf_focus_dist'], df['sm_focus_dist']) = zip(*df['ind_dist'].to_list())


if __name__ == "__main__":
    # process_set_run("Phys_Data_Salmonella_Only_", True, "normal")
    # data = pd.read_csv("Phys_Data_Salmonella_Only_Median_Process_Circuits_Run.csv")
    # add individual strain dist
    # data = add_combos(data, skip_ecoli=True)
    # data.to_csv("Full_Combined_Phys_Data_Salmonella_Only_Median_Process_Circuit_Results.csv", index=False)
    data = pd.read_csv("Full_Combined_Phys_Data_Salmonella_Only_Median_Process_Circuit_Results.csv", index_col=None)
    # TODO: Form new data frame of finger print errors
    # dist_data = fp_dist = fp_dist_df(data)
    # comp_process_frequency(dist_data)
    # TODO: generate graphs for strain only and strain focus on processes
    # TODO: generate graphs for finger_print comparisons (full, focused and only)
    # sets = ["Ecoli_Min_Process", "Ecoli_Full_Process", "Salmonella_Min_Process", "Salmonella_Full_Process"]
    # for bact_strain in sets:
    #     combo_graphs(data, bact_strain)
    pass
