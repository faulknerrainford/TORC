import numpy as np
import pandas as pd


def compare(a, b, df):
    """
    Takes lists of bacterium, promoter and strain for two different sets and compares the mhYFP_by_A600 values.
    Parameters
    ----------
    a   : List of bacterium, promoter and strain
    b   : List of bacterium, promoter and strain
    df : DataFrame
        Must have bacterium, strain, promoter and mhYFP_by_A600 columns.

    Returns
    -------
    int
        Indicator of the relative values of the compared sets

    """
    a_value = df.loc[(df["strain"] == a[2]) & (df["bacterium"] == a[0]) &
                     (df["promoter"] == a[1]), "mhYFP_by_A600"].values[0]
    b_value = df.loc[(df["strain"] == b[2]) & (df["bacterium"] == b[0]) &
                     (df["promoter"] == b[1]), "mhYFP_by_A600"].values[0]
    if a_value*0.95 > b_value*1.05:
        return 1
    elif b_value*0.95 > a_value*1.05:
        return -1
    else:
        return 0


# read in both files and combine
ecoli_df = pd.read_csv('plotted_bio_data_ecoli.csv')
salmonella_df = pd.read_csv('plotted_bio_data_salmonella.csv')
combined_df = pd.concat([ecoli_df, salmonella_df])

# group by data and get average
res = combined_df.groupby(['bacterium', 'strain', 'promoter'], as_index=False)['mhYFP_by_A600'].mean()
res = res[res['promoter'].str.contains("YFP")]
res = res[~res['promoter'].str.contains("RBS")]
res = res[~res['strain'].str.contains("\\\n")]


# rename for quicker reference
# Strains = WT, topA Lac, No_topA, No_Lac_No_topA
res.replace(["WT", "ΔlacIZYA::FRT ΔtopA::cat", "ΔtopA::cat", "ΔSL1483::lacIMG1655-FRT ΔtopA::cat"],
            ["WT", "No_Lac_No_topA", "No_topA", "Added_Lac_No_topA"], inplace=True)
# bacterium = Ecoil, Salmonella
res.replace(["Escherichia coli K12 MG1655", "Salmonella enterica Typhimurium SL1344"],
            ["E.coli", "Salmonella"], inplace=True)
# promoter = min, full
res.replace(["PleuWT.1 mhYFP", "PleuWT.1min mhYFP"],
            ["Full", "Min"], inplace=True)



# take 5 time steps off values needed for parameters for e.coli and salmonella runs. (5 to allow for leaks and start up
# time)
ecoli_weak_full = res.loc[(res["strain"] == "WT") & (res["bacterium"] == "E.coli") &
                          (res["promoter"] == "Full"), "mhYFP_by_A600"].values[0]/95
ecoli_weak_min = res.loc[(res["strain"] == "WT") & (res["bacterium"] == "E.coli") &
                         (res["promoter"] == "Min"), "mhYFP_by_A600"].values[0]/95
ecoli_strong_full = res.loc[(res["strain"] == "No_Lac_No_topA") & (res["bacterium"] == "E.coli") &
                            (res["promoter"] == "Full"), "mhYFP_by_A600"].values[0]/95
ecoli_strong_min = res.loc[(res["strain"] == "No_Lac_No_topA") & (res["bacterium"] == "E.coli") &
                           (res["promoter"] == "Min"), "mhYFP_by_A600"].values[0]/95
salmonella_weak_full = res.loc[(res["strain"] == "WT") & (res["bacterium"] == "Salmonella") &
                               (res["promoter"] == "Full"), "mhYFP_by_A600"].values[0]/95
salmonella_weak_min = res.loc[(res["strain"] == "WT") & (res["bacterium"] == "Salmonella") &
                              (res["promoter"] == "Min"), "mhYFP_by_A600"].values[0]/95
salmonella_strong_full = res.loc[(res["strain"] == "No_topA") & (res["bacterium"] == "Salmonella") &
                                 (res["promoter"] == "Full"), "mhYFP_by_A600"].values[0]/95
salmonella_strong_min = res.loc[(res["strain"] == "No_topA") & (res["bacterium"] == "Salmonella") &
                                (res["promoter"] == "Min"), "mhYFP_by_A600"].values[0]/95
# print("Ecoli: weak - "+str(ecoli_weak)+", strong - "+str(ecoli_strong))
# print("Salmonella: weak - "+str(salmonella_weak)+", strong - "+str(salmonella_strong))

# set up comparisons and collect separate vectors before combining into single main vector
# In promoter and bacteria comparisons
# Ecoli min
ecoli_min = [compare(["E.coli", "Min", "WT"], ["E.coli", "Min", "No_Lac_No_topA"], res),
             compare(["E.coli", "Min", "WT"], ["E.coli", "Min", "No_topA"], res),
             compare(["E.coli", "Min", "No_Lac_No_topA"], ["E.coli", "Min", "No_topA"], res)]

# Ecoli full
ecoli_full = [compare(["E.coli", "Full", "WT"], ["E.coli", "Full", "No_Lac_No_topA"], res),
              compare(["E.coli", "Full", "WT"], ["E.coli", "Full", "No_topA"], res),
              compare(["E.coli", "Full", "No_Lac_No_topA"], ["E.coli", "Full", "No_topA"], res)]

# Salmonella min
salmonella_min = [compare(["Salmonella", "Min", "WT"], ["Salmonella", "Min", "No_topA"], res),
                  compare(["Salmonella", "Min", "WT"], ["Salmonella", "Min", "Added_Lac_No_topA"], res),
                  compare(["Salmonella", "Min", "No_topA"], ["Salmonella", "Min", "Added_Lac_No_topA"], res)]

# Salmonella full
salmonella_full = [compare(["Salmonella", "Full", "WT"], ["Salmonella", "Full", "No_topA"], res),
                   compare(["Salmonella", "Full", "WT"], ["Salmonella", "Full", "Added_Lac_No_topA"], res),
                   compare(["Salmonella", "Full", "No_topA"], ["Salmonella", "Full", "Added_Lac_No_topA"], res)]

# WT Comparison (same bacteria or same promoter)
WT_comps = [compare(["E.coli", "Min", "WT"], ["E.coli", "Full", "WT"], res),
            compare(["Salmonella", "Min", "WT"], ["Salmonella", "Full", "WT"], res),
            compare(["E.coli", "Min", "WT"], ["Salmonella", "Min", "WT"], res),
            compare(["E.coli", "Full", "WT"], ["Salmonella", "Full", "WT"], res)]

# No topA and No Lac Comparison (same bacteria or same promoter)
No_topA_No_Lac_comps = [compare(["E.coli", "Min", "No_Lac_No_topA"], ["E.coli", "Full", "No_Lac_No_topA"], res),
                        compare(["Salmonella", "Min", "No_topA"], ["Salmonella", "Full", "No_topA"], res),
                        compare(["E.coli", "Min", "No_Lac_No_topA"], ["Salmonella", "Min", "No_topA"], res),
                        compare(["E.coli", "Full", "No_Lac_No_topA"], ["Salmonella", "Full", "No_topA"], res)]

# No topA and Lac Comparison (same bacteria or same promoter)
No_topA_Lac_comps = [compare(["E.coli", "Min", "No_topA"], ["E.coli", "Full", "No_topA"], res),
                     compare(["Salmonella", "Min", "Added_Lac_No_topA"],
                             ["Salmonella", "Full", "Added_Lac_No_topA"], res),
                     compare(["E.coli", "Min", "No_topA"], ["Salmonella", "Min", "Added_Lac_No_topA"], res),
                     compare(["E.coli", "Full", "No_topA"], ["Salmonella", "Full", "Added_Lac_No_topA"], res)]

# Form "fingerprints"
bio_finger_print = ecoli_full+salmonella_full+ecoli_min+salmonella_min+WT_comps+No_topA_No_Lac_comps+No_topA_Lac_comps

# group by data and get average
res_med = combined_df.groupby(['bacterium', 'strain', 'promoter'], as_index=False)['mhYFP_by_A600'].median()
res_med = res_med[res_med['promoter'].str.contains("YFP")]
res_med = res_med[~res_med['promoter'].str.contains("RBS")]
res_med = res_med[~res_med['strain'].str.contains("\\\n")]


# rename for quicker reference
# Strains = WT, topA Lac, No_topA, No_Lac_No_topA
res_med.replace(["WT", "ΔlacIZYA::FRT ΔtopA::cat", "ΔtopA::cat", "ΔSL1483::lacIMG1655-FRT ΔtopA::cat"],
            ["WT", "No_Lac_No_topA", "No_topA", "Added_Lac_No_topA"], inplace=True)
# bacterium = Ecoil, Salmonella
res_med.replace(["Escherichia coli K12 MG1655", "Salmonella enterica Typhimurium SL1344"],
            ["E.coli", "Salmonella"], inplace=True)
# promoter = min, full
res_med.replace(["PleuWT.1 mhYFP", "PleuWT.1min mhYFP"],
            ["Full", "Min"], inplace=True)

# set up comparisons and collect separate vectors before combining into single main vector
# In promoter and bacteria comparisons
# Ecoli min
ecoli_min = [compare(["E.coli", "Min", "WT"], ["E.coli", "Min", "No_Lac_No_topA"], res_med),
             compare(["E.coli", "Min", "WT"], ["E.coli", "Min", "No_topA"], res_med),
             compare(["E.coli", "Min", "No_Lac_No_topA"], ["E.coli", "Min", "No_topA"], res_med)]

# Ecoli full
ecoli_full = [compare(["E.coli", "Full", "WT"], ["E.coli", "Full", "No_Lac_No_topA"], res_med),
              compare(["E.coli", "Full", "WT"], ["E.coli", "Full", "No_topA"], res_med),
              compare(["E.coli", "Full", "No_Lac_No_topA"], ["E.coli", "Full", "No_topA"], res_med)]

# Salmonella min
salmonella_min = [compare(["Salmonella", "Min", "WT"], ["Salmonella", "Min", "No_topA"], res_med),
                  compare(["Salmonella", "Min", "WT"], ["Salmonella", "Min", "Added_Lac_No_topA"], res_med),
                  compare(["Salmonella", "Min", "No_topA"], ["Salmonella", "Min", "Added_Lac_No_topA"], res_med)]

# Salmonella full
salmonella_full = [compare(["Salmonella", "Full", "WT"], ["Salmonella", "Full", "No_topA"], res_med),
                   compare(["Salmonella", "Full", "WT"], ["Salmonella", "Full", "Added_Lac_No_topA"], res_med),
                   compare(["Salmonella", "Full", "No_topA"], ["Salmonella", "Full", "Added_Lac_No_topA"], res_med)]

# WT Comparison (same bacteria or same promoter)
WT_comps = [compare(["E.coli", "Min", "WT"], ["E.coli", "Full", "WT"], res_med),
            compare(["Salmonella", "Min", "WT"], ["Salmonella", "Full", "WT"], res_med),
            compare(["E.coli", "Min", "WT"], ["Salmonella", "Min", "WT"], res_med),
            compare(["E.coli", "Full", "WT"], ["Salmonella", "Full", "WT"], res_med)]

# No topA and No Lac Comparison (same bacteria or same promoter)
No_topA_No_Lac_comps = [compare(["E.coli", "Min", "No_Lac_No_topA"], ["E.coli", "Full", "No_Lac_No_topA"], res_med),
                        compare(["Salmonella", "Min", "No_topA"], ["Salmonella", "Full", "No_topA"], res_med),
                        compare(["E.coli", "Min", "No_Lac_No_topA"], ["Salmonella", "Min", "No_topA"], res_med),
                        compare(["E.coli", "Full", "No_Lac_No_topA"], ["Salmonella", "Full", "No_topA"], res_med)]

# No topA and Lac Comparison (same bacteria or same promoter)
No_topA_Lac_comps = [compare(["E.coli", "Min", "No_topA"], ["E.coli", "Full", "No_topA"], res_med),
                     compare(["Salmonella", "Min", "Added_Lac_No_topA"],
                             ["Salmonella", "Full", "Added_Lac_No_topA"], res_med),
                     compare(["E.coli", "Min", "No_topA"], ["Salmonella", "Min", "Added_Lac_No_topA"], res_med),
                     compare(["E.coli", "Full", "No_topA"], ["Salmonella", "Full", "Added_Lac_No_topA"], res_med)]

# Form "fingerprints"
med_bio_finger_print = ecoli_full+salmonella_full+ecoli_min+salmonella_min+WT_comps+No_topA_No_Lac_comps+No_topA_Lac_comps

print(bio_finger_print)
print(med_bio_finger_print)