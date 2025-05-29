Instructions on the full process from the output of the physics model to graphs using the code in TORC.

################
Step 1
################
- Process output from Physics Model for sigmoid values (actually gaussian)
    + Use Experiment_Data/Circuit_Processes/Phys_based_sigmoid/get_sigmoid_values.py
        + Modify file path to use the superhelicity_at_promoter file from TORCPhysics
        + If this file does not exist it can be generated using the get_supercoiling_at_promoter.py

21/05/2025 Sigmoid Values (actually gaussian):
Full Promoter Probability Mean: -0.07304387589686555
Full Promoter Probability Standard Deviation: 0.08181996202466614
Min Promoter Probability Mean: -0.08719539871858617
Min Promoter Probability Standard Deviation: 0.12845853187246675

##############
Step 2
##############
- Modify the fixed values in the main of the gradient descent
    + pleuWT_sigmoid -> Probability Mean
    + gradient -> Probability Standard Deviation

21/05/2025 Parameterisation run:
    check_values = [0.6633588091, 20471.26332, 30860.01578]
    fixed_values_full = {"pleuWT_sigmoid": -0.07304387589686555, "gradient": 0.08181996202466614, "tetA_sc": 0.05,
                         "anti_tet_sc": 0.001}
    full_promoter = parameter_setting("Gradient_Descent_Phys_Test_Full", 0.01,
                                      ["pleuWT_sigmoid", "gradient", "tetA_sc", "anti_tet_sc"], 1000,
                                      1, check_values, 60, fixed_values_full)

    Parameters for Salmonella with full promoter:
    {'tetA_sc': 0.05, 'mhYFP_sc': 0.0030446120261538, 'pleuWT_sigmoid': -0.0730438758968655, 'mhYFP_max': 23.6265774724979, 'mhYFP_min': 19.937824715727697, 'relax_WT': 0.7152736182204096, 'relax_DTA': 0.2196310757689402, 'gradient': 0.0818199620246661, 'anti_tetA_sc': 0.001}

22/05/2025 Min promoter parameterisation run (uses supercoiling and relax values from previous and sigmoid and gradient from TORCPhysics)

    check_values = [0.6917340988, 21443.75987, 31000.00405]
    fixed_values_full = {"pleuWT_sigmoid": -0.08719539871858617, "gradient": 0.12845853187246675, "tetA_sc": 0.05,
                         "anti_tet_sc": 0.001, "mhYFP_sc": 0.0030446120261538,
                         'relax_WT': 0.7152736182204096, 'relax_DTA': 0.2196310757689402}
    min_parameters = parameter_setting("Gradient_Descent_Phys_Test_Full", 0.01,
                                       ["pleuWT_sigmoid", "gradient", "tetA_sc", "anti_tet_sc",
                                        "mhYFP_sc", "relax_WT", "relax_DTA"], 1000, 1,
                                       check_values, 60, fixed_values_full)

This did not complete in 60 generations so is restarted using the following settings:

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

7 generations with no further increment changes yielded accurate values for the Min Promoter in Salmonella:
{'tetA_sc': 0.05, 'mhYFP_sc': 0.0030446120261538, 'pleuWT_sigmoid': -0.0871953987185861, 'mhYFP_max': 21.765110326714744, 'mhYFP_min': 18.496844452749595, 'relax_WT': 0.7152736182204096, 'relax_DTA': 0.2196310757689402, 'gradient': 0.1284585318724667, 'anti_tetA_sc': 0.001}

###############
Step 3
###############
- Run the set of process circuits
    + Use the Main of the ProcessCircuits/ProcessCircuitRun.py

    + Edit globals to match parameters found above:
        # Salmonella Topo effects
        relax_WT_Salmonella = 0.7152736182204096
        relax_DTA_Salmonella = 0.2196310757689402

        # Supercoiling values
        tetA_sc = -0.05
        mhYFP_sc = 0.0030446120261538

        # Full promoter
        pleuWT_sigmoid_full = -0.0730438758968655
        gradient_full = 0.0818199620246661
        # Output Salmonella
        mhYFP_min_pfull_s = 19.937824715727697
        mhYFP_max_pfull_s = 23.6265774724979

        # Min promoter
        pleuWT_sigmoid_min = -0.0871953987185861
        gradient_min = 0.1284585318724667
        # Output Salmonella
        mhYFP_min_pmin_s = 18.496844452749595
        mhYFP_max_pmin_s = 21.765110326714744

27/05/2025 Process Circuit Run with:

if __name__ == "__main__":
    process_set_run("Phys_Data_Salmonella_Only_", True, "normal")

############
Step 4
############

Recombine data to get full set of possible combinations of processes. This is much smaller with just salmonella.
This can be done using the previously generated file with out the need to regenerate it. Suggest that this is done by
commenting out the above line (used to run step 3) in the main and instead reading in the dataframe.

27/05/2025 Combinations Run with:

Note: This part (in particular the formation of strain based finger prints) should be checked before being relied by
someone with a clear head.

if __name__ == "__main__":
    # process_set_run("Phys_Data_Salmonella_Only_", True, "normal")
    data = pd.read_csv("Phys_Data_Salmonella_Only_Median_Process_Circuits_Run.csv")
    # add individual strain dist
    data = add_combos(data, skip_ecoli=True)
    data.to_csv("Full_Combined_Phys_Data_Salmonella_Only__Median_Process_Circuit_Results.csv", index=False)


####################
Data Description
####################

At this stage you will have the file: "Full_Combined_Phys_Data_Salmonella_Only__Median_Process_Circuit_Results.csv"
(or equivalent if you have ecoli in as well)

To aid further analysis the values in each column are explained:

-------------
Process
-------------

The process fields dictate which process set (variant action of anti-tet and lac) the relevant strain (bacteria and
promoter combination) used to produce output data in that row.

Anti-tet read-through - transcription at the anti-tet promoter is not terminated so continues along the DNA and through
    the YFP promoter producing junk and preventing transcription starting at the YFP promoter.
Anti-tet interfering supercoiling - the anti-tet promoter while small transcribes and in doing so produces positive
    supercoiling that cancels out the effect of the tetA gene and this effects the transcription rate of the YFP
    production.
Anti-tet does nothing - the anti-tet promoter is assumed to be too small to have any effect on the YFP promoter and gene

Lac forms loop - Lac binds at both binding points and with each other to create an isolated loop in the plasmid which
    supercoiling can not move into or out of. This is the twin domain model often seen in the literature.
Lac canonically represses a promoter - Lac binds so close to the promoter that at the lac binding point that it prevents
    the promoter opening and transcribing.
Lac does nothing - we assume that lac does not bind and has no effect on the plasmid.

0 = Anti-tet induces read-through of the YFP promoter and lac forms an isolated loop
1 = Anti-tet induces read-through of the YFP promoter and lac represses the YFP promoter (canonical repression)
2 = Anti-tet induces read-through of the YFP promoter and lac forms an isolated loop and represses the YFP promoter
3 = Anti-tet induces read-through of the YFP promoter and lac does nothing
4 = Anti-tet produces interfering supercoiling and lac forms an isolated loop
5 = Anti-tet produces interfering supercoiling and lac represses the YFP promoter (canonical repression)
6 = Anti-tet produces interfering supercoiling and lac forms an isolated loop and represses the YFP promoter
7 = Anti-tet produces interfering supercoiling and lac does nothing
8 = Anti-tet induces read-through of the YFP promoter and interfering supercoiling and lac forms an isolated loop
9 = Anti-tet induces read-through of the YFP promoter and interfering supercoiling and lac represses the YFP promoter (canonical repression)
10 = Anti-tet induces read-through of the YFP promoter and interfering supercoiling and lac forms an isolated loop and represses the YFP promoter
11 = Anti-tet induces read-through of the YFP promoter and interfering supercoiling and lac does nothing
12 = Anti-tet does nothing and lac forms an isolated loop
13 = Anti-tet does nothing and lac represses the YFP promoter (canonical repression)
14 = Anti-tet does nothing and lac forms an isolated loop and represses the YFP promoter
15 = Anti-tet does nothing and lac does nothing

-------------------
Strains
-------------------

There are generally up to four strains in the data. Two Ecoli versions and two Salmonella versions. There are then three
substrains for each strain that effect the presence of lac and the supercoiling relaxation rates through the
modification of topoisomerases.

- Ecoli
    - Full pleuWT promoter
        - WT (Includes Lac and topA)
        - DTA or delta topA (Includes Lac and Removes topA)
        - DL/DTA or delta lac delta topA (Removes Lac and topA)
    - Minimal pleuWT promoter
        - WT (Includes Lac and topA)
        - DTA or delta topA (Includes Lac and Removes topA)
        - DL/DTA or delta lac delta topA (Removes Lac and topA)

- Salmonella
    - Full pleuWT promoter
        - WT (Does not include Lac but does include topA)
        - IL/DTA or include lac delta topA (Includes Lac and Removes topA)
        - DTA or delta topA (Does not include Lac and removes topA)
    - Minimal pleuWT promoter
        - WT (Does not include Lac but does include topA)
        - IL/DTA or include lac delta topA (Includes Lac and Removes topA)
        - DTA or delta topA (Does not include Lac and removes topA)


-----------------
Outputs
-----------------

The outputs from the models are labeled by strain. They all are the same output value. This is the measure of output
from the mhYFP gene in the plasmid. In the bio data this is in terms of fluorescence, we attempt to match the median
value from those experiments. In the TORCcomp model it is a total "output" which can be tuned in parameterisation to
match transcription, fluorescence or any other measure of this genes output as we do not work with discrete output
objects but instead with rates.

----------------
Fingerprints
----------------

There are a set of distances and measures based on comparing the finger prints of the bio data and the comp data
outputs.

The bio fingerprint is put together based on:
Experiment_Data/Circuit_Processes/Parameters/plotted_bio_data_ecoli.csv
Experiment_Data/Circuit_Processes/Parameters/plotted_bio_data_salmonella.csv

These are processed in:
Experiment_Data/Circuit_Processes/Parameters/Bio_data_analysis.py

This gives a fingerprint of ternary values (-1,0,1) which indicate the comparative difference between different values.
The values indicate if the first value is lower, the same or higher than the second value. In order the finger print
compares (the fingerprint is just a list but is given here in blocks for readability):

Ecoli Full
1. WT & No_Lac_No_topA
2. WT & No_topA
3. No_Lac_No_topA & No_topA

Salmonella Full
4. WT & No_topA
5. WT & Added_Lac_No_topA
6. No_topA & Added_Lac_No_topA

Ecoli Min
7. WT & No_Lac_No_topA
8. WT & No_topA
9. No_Lac_No_topA & No_topA

Salmonella Min
10. WT & No_topA
11. WT & Added_Lac_No_topA
12. No_topA & Added_Lac_No_topA

WT
13. Ecoli Min & Ecoli Full
14. Salmonella Min & Salmonella Full
15. Ecoli Min & Salmonella Min
16. Ecoli Full & Salmonella Full

No topA and No Lac
17. Ecoli Min & Ecoli Full
18. Salmonella Min & Salmonella Full
19. Ecoli Min & Salmonella Min
20. Ecoli Full & Salmonella Full

No topA and Lac
21. Ecoli Min & Ecoli Full
22. Salmonella Min & Salmonella Full
23. Ecoli Min & Salmonella Min
24. Ecoli Full & Salmonella Full

These fingerprints can also be formed through comparisons between values produced from our TORCcomp results. We can then
get a distance between two fingerprints based on the sum of the absolute differences. This leads to our next set of
data values.

fp_dist - The total distance between full fingerprints (for salmonella only runs this is just comparisons without ecoli)
ind_dist - vector of distances for the separate strain comparisons also given separately below.
sf_only_dist - Distance between comparisons which are in the Salmonella Full block
sm_only_dist - Distance between comparisons which are in the Salmonella Min block
ef_only_dist - Distance between comparisons which are in the Ecoli Full block
em_only_dist - Distance between comparisons which are in the Ecoli Min block

Finally we expand the individual strain distance measures to include any comparisons with other strains that involved
the in focus strain.
sf_focus_dist - Distance between comparisons which include substrains from the Salmonella Full strain
sm_focus_dist - Distance between comparisons which include substrains from the Salmonella Min strain
ef_focus_dist - Distance between comparisons which include substrains from the Ecoli Full strain
em_focus_dist - Distance between comparisons which include substrains from the Ecoli Min strain
