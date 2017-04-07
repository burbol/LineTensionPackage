#!/bin/bash

# Script to create horizontal density maps
# using "gmx density" recursively for different time intervals 
# Run script from sheldon or yoshi server

module load gromacs/single/2016.1


mkdir /net/data/eixeres/Version_v2/global_SAMs_densmaps/90-100ns
mkdir /net/data/eixeres/Version_v2/global_NVT_densmaps/90-100ns

# Make global density maps for:
# SAM number density   -> name:  ng_density_SAM_sam${i}_water${j}.xvg
# SAM mass density     -> name:  g_density_SAM_sam${i}_water${j}.xvg
# Water number density -> name:  ng_density_NVT_sam${i}_water${j}.xvg 
# Water mass density   -> name:  g_density_NVT_sam${i}_water${j}.xvg

# Choose starting and ending times for the density map
beg_time=90
end_time=100
# Convert time units
beg_time=$((beg_time*1000))
end_time=$((end_time*1000))

for i in 44 37 33 22 11 0 50 # OH density of the SAM
do
  for j in 10000 9000 8000 7000 6500 5000 4000 3000 2000 1000  # number of water molecules
  do

        cd /net/data03/eixeres/scratch_yoshi/Version_v2/s${i}_w${j}
        
        n=4
        if [ $i -eq 0 ]
        then 
          n=3
          m=2
        else 
          n=4
          m=6
        fi
    
        #echo "0" "q"|gmx make_ndx -f NVT_sam${i}_water${j}.gro -o index${i}_${j}.ndx 
     
        #gmx grompp -f NVT_80ns_v2.mdp -c NVT_sam${i}_water${j}.gro -p ${i}pc_${j}.top -n index${i}_${j}.ndx -o g_rad_NVT_sam${i}_water${j}.tpr -maxwarn 11
        
        #Calculate mass densities
        echo ${n} | gmx density -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o g_density_NVT_sam${i}_water${j}.xvg -sl 1000 -b ${beg_time} -e ${end_time}
        echo ${m} | gmx density -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o g_density_SAM_sam${i}_water${j}.xvg -sl 1000 -b ${beg_time} -e ${end_time} # for SAMs density maps
    
        #Calculate number densities   
        echo ${n} | gmx density -dens number -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o ng_density_NVT_sam${i}_water${j}.xvg -sl 1000 -b ${beg_time} -e ${end_time}
        echo ${m} |gmx density -dens number -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o ng_density_SAM_sam${i}_water${j}.xvg -sl 1000 -b ${beg_time} -e ${end_time}
    
        #Copy all files to same folder and delete originals
        mv ng_density_SAM_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_SAMs_densmaps/90-100ns/ng_density_NVT_sam${i}_water${j}.xvg
        mv ng_density_NVT_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_NVT_densmaps/90-100ns/ng_density_SAM_sam${i}_water${j}.xvg
        
        mv g_density_SAM_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_SAMs_densmaps/90-100ns/g_density_SAM_sam${i}_water${j}.xvg
        mv g_density_NVT_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_NVT_densmaps/90-100ns/g_density_NVT_sam${i}_water${j}.xvg
      done
    done
    