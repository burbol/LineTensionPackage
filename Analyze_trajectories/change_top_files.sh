#!/bin/bash

# Make a copy of each .top file and change text of "include" commands to adapt to GROMACS version 4. 

#for i in 0 # OH density of the SAM
for i in 11 22 33 37 44
do

  #for j in 1000   # number of water molecules
  for j in 1000 2000 3000 4000 5000 6500
  do

    #cd /net/data/eixeres/Version_v2/FINISHED/s${i}_w${j}/
    cd /scratch/eixeres/Version_v2.2/s${i}_w${j}/

    file=${i}pc_${j}_old.top
    cp ${i}pc_${j}.top $file
    sed -e 's/gromos53a6\.ff\/forcefield\.itp/ffG53a6\.itp/' -e 's/gromos53a6\.ff\/spce\.itp/spce\.itp/' <${i}pc_${j}.top >$file
    
    
   done
done