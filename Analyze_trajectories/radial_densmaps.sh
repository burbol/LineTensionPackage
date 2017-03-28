#!/bin/bash

# Script to create horizontal and radial density maps
# using g_density recursively and g_rad_density in time intervals of 500 ps
# Run script from sheldon or yoshi server using gromacs_tpi_compiled
# Change "include" commands at the beginning of top files using "change_top_files.sh"


module load gromacs/single/2016.1


# the round function:
round()
{
echo $(printf %.$2f $(echo "scale=$2;(((10^$2)*$1)+0.5)/(10^$2)" | bc))
};


#mkdir /net/data/eixeres/Version_v2/radial_densmaps

for i in 44  # OH density of the SAM
do
  for j in 5000  # number of water molecules
  do

  #cd /net/data/eixeres/Version_v2/FINISHED/s${i}_w${j} # First Round all systems
  #cd /net/data03/eixeres/scratch_yoshi/Version_v2/s${i}_w${j} # Second round big systems (small still running on sheldon-ng)
  cd /scratch/eixeres/Version_v2/s${i}_w${j}
  
  if [ $i -eq 0 ]
  then 
    n=3
    m=2
  else 
    n=4
    m=6
  fi


# # Make radial density maps every 500ps

#echo "0" "q"|gmx make_ndx -f NVT_sam${i}_water${j}.gro -o index${i}_${j}.ndx 
 
#gmx grompp -f NVT_80ns_v2.mdp -c NVT_sam${i}_water${j}.gro -p ${i}pc_${j}.top -n index${i}_${j}.ndx -o g_rad_NVT_sam${i}_water${j}.tpr -maxwarn 11
    
# # Load old GROMACS for compatibility with g_rad_density 
 GMXLIB="/net/data/eixeres/sheldon-old/gromacs_tpi_compiled/share/gromacs/top/"

# # Use old version of grompp with old version of .top file
 /net/data/eixeres/sheldon-old/gromacs_tpi_compiled/bin/grompp -f NVT_60ns_v2.mdp -c Mini_sam${i}_water${j}.gro -p ${i}pc_${j}_old.top -n index${i}_${j}.ndx -o g_rad_NVT_sam${i}_water${j}.tpr -maxwarn 11
 
    
    
    k=0
    while [[ $k -le 1995 ]]  # segments of time to be multiplied by 100 so that we get [ps]
    do    
        k2=$((k+5))
        nanosecs1=$(echo $(round $k/10 1))
        nanosecs2=$(echo $(round $k2/10 1))
        start=$((k*100))
        ending=$((start+500))

        echo "Creating densmap from $start ps to $ending ps"

        echo ${n} ${n} | /net/data/eixeres/sheldon-old/g_rad_density -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -n index${i}_${j}.ndx -sz 200 -o g_rad_dmap_${i}pc_w${j}_${nanosecs1}ns_${nanosecs2}ns.xvg -b ${start} -e ${ending}
        
        mv g_rad_dmap_${i}pc_w${j}_${nanosecs1}ns_${nanosecs2}ns.xvg /net/data/eixeres/Version_v2/radial_densmaps/s${i}_w${j}/g_rad_dmap_${i}pc_w${j}_${nanosecs1}ns_${nanosecs2}ns.xvg
	
	    k=$(($k+5))
	done    
  done
done
