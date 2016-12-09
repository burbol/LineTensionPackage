#!/bin/bash

for i in 0 5 11 22 33 37 44 50 # OH density of the SAM 
do
  # now number of molecs in order of importance (regarding fair share)
  for j in 1000 2000 3000 4000 5000 # sheldon-ng
  #for j in 9000 6500 8000 10000 7000 # gpu yoshi
  do 
    cd /scratch/eixeres/Version_v2/scripts/s${i}_w${j}

    # 1node on sheldon-ng
    sbatch 1n_s${i}_w${j}_0
    
    # gpu on yoshi
    #sbatch 1n_s${i}_w${j}_gpu_0
    
    cd ..  
  done
done