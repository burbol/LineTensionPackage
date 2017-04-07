#!/bin/bash

# Script to create density profiles ("maps")
# using gmx g_density recursively
# Run from sheldon or yoshi server


module load gromacs/single/2016.1

mkdir /net/data/eixeres/Version_v2/planar_densmaps

for i in 44 37 33 22 11 0 50 # OH density of the SAM 
do

  cd /net/data/eixeres/Version_v2/FINISHED/Planar_Systems/s${i}
  
  n=4
  if [ $i -eq 0 ]
  then 
    n=3
    m=5
  else 
    n=4
    m=6
  fi

# Make global density maps for:
# SAM number density   -> name:  ndens_SAM_sam${i}_water_ptensor.xvg
# SAM mass density     -> name:  dens_SAM_sam${i}_water_ptensor.xvg
# Water number density -> name:  ndens_NVT_sam${i}_water_ptensor.xvg 
# Water mass density   -> name:  dens_NVT_sam${i}_water_ptensor.xvg 
    
    # Calculate mass densities (for the last 4ns of the 8ns-simulations)
    # For water
    echo 0 ${n} | gmx density -f NVT_sam${i}_water_ptensor_v2.xtc -s NVT_sam${i}_water_ptensor_v2.tpr -o dens_NVT_sam${i}_water_ptensor.xvg -sl 1000 -b 4000 -e 8000 -center
    # For SAMs 
    echo 0 ${m} | gmx density -f NVT_sam${i}_water_ptensor_v2.xtc -s NVT_sam${i}_water_ptensor_v2.tpr -o dens_SAM_sam${i}_water_ptensor.xvg -sl 1000 -b 4000 -e 8000 -center
    
    # Calculate number densities (for the last 4ns of the 8ns-simulations)
    # For water
    echo 0 ${n} | gmx density -dens number -f NVT_sam${i}_water_ptensor_v2.xtc -s NVT_sam${i}_water_ptensor_v2.tpr -o ndens_NVT_sam${i}_water_ptensor.xvg -sl 1000 -b 4000 -e 8000 -center
    # For SAMs 
    echo 0 ${m} |gmx density -dens number -f NVT_sam${i}_water_ptensor_v2.xtc -s NVT_sam${i}_water_ptensor_v2.tpr -o ndens_SAM_sam${i}_water_ptensor.xvg -sl 1000 -b 4000 -e 8000 -center

# Move all files to same folder
mv dens_SAM_sam${i}_water_ptensor.xvg  /net/data/eixeres/Version_v2/planar_densmaps/dens_SAM_sam${i}_water_ptensor.xvg
mv dens_NVT_sam${i}_water_ptensor.xvg  /net/data/eixeres/Version_v2/planar_densmaps/dens_NVT_sam${i}_water_ptensor.xvg

mv ndens_SAM_sam${i}_water_ptensor.xvg  /net/data/eixeres/Version_v2/planar_densmaps/ndens_SAM_sam${i}_water_ptensor.xvg
mv ndens_NVT_sam${i}_water_ptensor.xvg  /net/data/eixeres/Version_v2/planar_densmaps/ndens_NVT_sam${i}_water_ptensor.xvg


done
