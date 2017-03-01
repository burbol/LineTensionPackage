#!/bin/bash

# This script has to be run from the server. There is one copy on yoshi and another on sheldon-ng.
# This script is only a copy for reference of the scripts on the servers.


# number of molecs in order of importance (regarding fair share)
for j in 1000 3000 5000 2000 4000 # sheldon-ng # 9000 6500 8000 10000 7000 $yoshi
do 
  
    for i in 0 11 22 33 37 44 # OH density of the SAM (50% will be treated separately)
    do

    cd /scratch/eixeres/Version_v2/scripts/s${i}_w${j}

    # 1node on sheldon-ng
    #sbatch 1n_s${i}_w${j}_0  # name of submission scripts used for the first round (from 60ns to 100ns)
    sbatch s${i}_w${j}_0 # names used for the second round (extended until 200ns)
    
    # gpu on yoshi
    #sbatch 1n_s${i}_w${j}_gpu_0 # first round names
    #sbatch s${i}_w${j}_gpu_0 #second round names (extended until 200ns)
    
    cd ..  
  done
done