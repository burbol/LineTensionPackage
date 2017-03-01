#!/bin/bash

# This script has to be run from the server. (This is only a copy of the scripts saved on yoshi and sheldon-ng).
# It reduces the size of the simulation trajectories to adapt to vmd (extracting only one frame every 50)

module load gromacs/single/2016.1

for i in 0 5 11 22 33 37 44 50 # OH density of the SAM 
do

  for j in 1000 2000 3000 4000 5000 6500 7000 8000 9000 10000 

  do 
    cd /scratch/eixeres/Version_v2/s${i}_w${j}
    
    gmx trjconv -f NVT_sam${i}_water${j}.xtc -o NVT_sam${i}_water${j}_dil.xtc -skip 50 
    
    cd ..  
  done
done