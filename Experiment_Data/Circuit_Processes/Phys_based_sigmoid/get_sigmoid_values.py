# Authors: Victor Velasco-Berrelleza (Primary), Penn Faulkner Rainford (Edited and broke the graphs)
import pickle
import numpy as np

# Model & simulation conditions
# ----------------------------------------------------------------------------------------------------------------------
input_file = 'superhelicity_at_promoter-both-SalmonellaOnly_separated.pkl'


gene_names = ['PleuWT', 'tetA', 'antitet', 'bla']

# Load
#-----------------------------------------------------------------------------------------------------------------------
with open(input_file, 'rb') as file:
    output_dict = pickle.load(file)

# Pull back out the relevant promoter data
flat_superhelical = output_dict['PleuWT_full']

# But let's filter cases to those relevant to the active promoter
filtered = flat_superhelical[(flat_superhelical >= -1.2) & (flat_superhelical <= 1.2)]

# get mean and standard deviation of the active promoter superhelicities
print("Full Promoter Probability Mean: " + str(np.mean(filtered)))
print("Full Promoter Probability Standard Deviation: " + str(np.std(filtered)))

# Pull back out the relevant promoter data
flat_superhelical = output_dict['PleuWT_min']

# But let's filter cases to those relevant to the active promoter
filtered = flat_superhelical[(flat_superhelical >= -1.2) & (flat_superhelical <= 1.2)]

# get mean and standard deviation of the active promoter superhelicities
print("Min Promoter Probability Mean: " + str(np.mean(filtered)))
print("Min Promoter Probability Standard Deviation: " + str(np.std(filtered)))
