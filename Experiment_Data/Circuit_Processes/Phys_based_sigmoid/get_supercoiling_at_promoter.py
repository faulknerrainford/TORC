# Authors: Victor Velasco-Berrelleza (Primary), Penn Faulkner Rainford (Edited and broke the graphs)

import numpy as np
import matplotlib.pyplot as plt
import pickle

# Description
# ----------------------------------------------------------------------------------------------------------------------
# Loads pickle file which is a dictionary.
# Each key is the name of a system, for example, 'EColi_full_WT' are results for EColi with the full promoter and in the
# WT background.
# Each dictionary entry has a list, where each entry of the list is a dictionary with the results of a simulation
# from TORCPhysics. These results are output dataframes: enzymes_df, sites_df, environmental_df.
# We need to analyse the enzymes_df to extract the superhelicities at which the promoters are active, that is,
# if an RNAP enzyme binds and forms either the closed or open complex.

# This script outputs a dictionary with the superhelical values at each promoter when they are active.
# It also plots the distributions of these for visualization

# Model & simulation conditions
# ----------------------------------------------------------------------------------------------------------------------
input_file = 'block-full-trackingON-dist_op_TORC_plasmid_st3.3_02_df.pkl'
output_file = 'superhelicity_at_promoter'

# Plotting params
#-----------------------------------------------------------------------------------------------------------------------
width = 8#+1
height = 5
lw = 3
font_size = 12
xlabel_size = 14
title_size = 16

gene_names = ['PleuWT', 'tetA', 'antitet', 'bla']

# Load
#-----------------------------------------------------------------------------------------------------------------------
with open(input_file, 'rb') as file:
    df_dict = pickle.load(file)

# Plot - Extract superhelical at the promoter for closed complex and open complex
#-----------------------------------------------------------------------------------------------------------------------
n = 3
# Let's plot as we load
fig, axs = plt.subplots(n, figsize=(width, n*height), tight_layout=True)

output_dict = {} # Th
gen_output_dict = {}
system_names = df_dict.keys()
for i, g_name in enumerate(gene_names):  # Let's go through each gene
    superhelical = []
    gen_superhelical = []
    for name in system_names:  # And go through each system, e.g., EColi WT, Salmonella WT, etc...
        system = df_dict[name]
        for output  in system:  # Calculate cross correlation matrices
            enzymes_df = output['enzymes_df']
            mask = (
                    enzymes_df['name'].isin(['RNAP_Closed_complex', 'RNAP_Open_complex']) &
                    (enzymes_df['site'] == g_name)
            )
            promoter_df = enzymes_df[mask]

            gen_mask = (
                    (enzymes_df['site'] == g_name)
            )

            promoter_gen_df = enzymes_df[gen_mask]

            supe = promoter_df['superhelical'].to_numpy()
            superhelical.append(supe)
            gen = promoter_gen_df['superhelical'].to_numpy()
            gen_superhelical.append(gen)

    # Flatten them into one single array
    flat_superhelical = np.concatenate(superhelical)
    flat_gen_superhelical = np.concatenate(gen_superhelical)

    # Collect the data
    output_dict[g_name] = flat_superhelical
    gen_output_dict[g_name] = flat_gen_superhelical

# Pull back out the relevant promoter data
flat_superhelical = output_dict['PleuWT']
flat_gen_superhelical = gen_output_dict['PleuWT']

# But let's filter cases to those relevant to the active promoter
filtered = flat_superhelical[(flat_superhelical >= -1.2) & (flat_superhelical <= 1.2)]
filtered_gen = flat_gen_superhelical[(flat_gen_superhelical >= -1.2) & (flat_gen_superhelical <= 1.2)]

# bin size thoughts min value in output: -3.323465, max: 3.546623. In gen min: -3.323465, max: 126.141816 suggests
# bining based on active regions with inactive regions grouped with 0 probability.
# Run with start at -3.4 to 3.6 with additional 2 bins outside of range in either direction
# Only PleuWT relevant.
# Bin count: consider 10, 100, 1000
# Best count based on hists is 100 (Will use this)

# build binned frequency arrays for each flat data set (with bins in focus area and additional bins) to get
#  probabilities, remove empty general bins from consideration (lack of data does not produce a 0 prob and active
#  should be empty as well)
# set range for start and end points for each interval, then get count for before and after and for inbetween
interval_points = np.arange(-3.4, 3.6+(7.0/100.0), (7.0/100.0))
counts_active = np.empty(102)
counts_general = np.empty(102)
counts_active[0] = sum([1 if x < -3.4 else 0 for x in flat_superhelical])
counts_general[0] = sum([1 if x < -3.4 else 0 for x in flat_gen_superhelical])

for i in range(0, 100):
    counts_active[i+1] = sum([1 if interval_points[i] <= x < interval_points[i+1] else 0 for x in flat_superhelical])
    counts_general[i+1] = sum([1 if interval_points[i] <= x < interval_points[i+1] else 0 for x in flat_gen_superhelical])

counts_active[101] = sum([1 if x > 3.6 else 0 for x in flat_superhelical])
counts_general[101] = sum([1 if x > 3.6 else 0 for x in flat_gen_superhelical])

# Filtering based on lack of count in counts_general
counts_active = np.array([act if gen > 9 else 0 for act, gen in zip(counts_active, counts_general)])
counts_general = np.array([x if x > 9 else 0 for x in counts_general])

probabilities = counts_active/counts_general
# Remove outlier (outside interval of interest) probabilities
probabilities = probabilities[1:-1]
sh_points = np.empty(100)
for i in range(0, 100):
    sh_points[i] = interval_points[i] + (7.0/200.0)

sh_points = np.array([point for point, prob in zip(sh_points, probabilities) if prob])
probabilities = np.array([prob for prob in probabilities if prob])


# build figure showing frequency hist of all supercoiling, promoter active supercoiling  and probs
ax = axs[0]
# Plot as a histogram
ax.hist(filtered, bins=100, edgecolor='black', color='red')
ax.set_ylabel(r'Frequency', fontsize=xlabel_size)
ax.set_xlabel('Superhelicity', fontsize=xlabel_size)
ax.set_title('Promoter Active', fontsize=title_size)
ax.grid(True)

ax = axs[1]
# Plot as a histogram
ax.hist(filtered_gen, bins=100, edgecolor='black', color='red')
ax.set_ylabel(r'Frequency', fontsize=xlabel_size)
ax.set_xlabel('Superhelicity', fontsize=xlabel_size)
ax.set_title('General', fontsize=title_size)
ax.grid(True)

ax = axs[2]
# Plot as line graph of probability at each bin (final number to be determined)
ax.plot(sh_points, probabilities, linewidth=lw, color='black')
ax.set_ylabel(r'Probability', fontsize=xlabel_size)
ax.set_xlabel('Superhelicity', fontsize=xlabel_size)
ax.set_title('Probability of activity', fontsize=title_size)
ax.grid(True)

plt.show()


# get mean and standard deviation of the active promoter superhelicities
print("Probability Mean: " + str(np.mean(filtered)))
print("Probability Standard Deviation: " + str(np.std(filtered)))



# Save the dictionary to a pickle file
with open(output_file + '.pkl', 'wb') as file:
    pickle.dump(output_dict, file)
