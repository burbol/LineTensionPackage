#!/bin/bash

# Script to create horizontal and radial density maps
# using g_density recursively and g_rad_density in time intervals of 500 ps
# Run script from slurm server


#######source /Volumes/UNI/SHELDON/CLOSEDsheldon/eixeres/gromacs_tpi_compiled/bin/GMXRC
module load gromacs/single/2016


# the round function:
round()
{
echo $(printf %.$2f $(echo "scale=$2;(((10^$2)*$1)+0.5)/(10^$2)" | bc))
};


n=4


#mkdir /net/data/eixeres/Version_v2/global_SAMS_densmaps
#mkdir /net/data/eixeres/Version_v2/global_NVT_densmaps
#mkdir /net/data/eixeres/Version_v2/radial_density

#for i in 0 11 22 33 37 44 50 # OH density of the SAM
for i in 0
do
  #for j in 1000 2000 3000 4000 5000 6500 7000 8000 9000 10000  # number of water molecules
  for j in 1000
  do

  cd /net/data/eixeres/Version_v2/FINISHED/s${i}_w${j}
  
  if [ $i -eq 0 ]
  then 
    n=3
  else 
    n=4
  fi
  

#######################################################################
########## THESE LINES WERE ADDED TO CREATE THE .gro FILES OF SIMULATIONS NOT ENDED NORMALLY ##########
    temp=0
    if [ $j -eq 1000 ]
    then temp=19000
    elif [ $j -eq 2000 ]
    then temp=43000
    elif [ $j -eq 3000 ]
    then temp=51000
    elif [ $j -eq 4000 ]
    then temp=47000
    elif [ $j -eq 5000 ]
    then temp=48000
    elif [ $j -eq 6500 ]
    then temp=44000
    elif [ $j -eq 7000 ]
    then temp=93000
    elif [ $j -eq 8000 ]
    then temp=63000
    elif [ $j -eq 9000 ]
    then temp=19000
    elif [ $j -eq 10000 ]
    then temp=26000
    fi
    
    #echo "0"|/home/shavkat/GMX/bin/trjconv -f NVT_sam${i}_water${j}.xtc # watch output for last frame determination
    #/home/shavkat/GMX/bin/grompp -f NVT_60ns_v2.mdp -p ${i}pc_${j}.top -t NVT_sam${i}_water${j}.trr -c Mini_sam${i}_water${j}.gro -o NVT_sam${i}_water${j}_temp.tpr -maxwarn 2
    #echo "0"|/home/shavkat/GMX/bin/trjconv -f NVT_sam${i}_water${j}.xtc  -s NVT_sam${i}_water${j}_temp.tpr -o NVT_sam${i}_water${j}_temp.gro -b $temp -sep
    #Afterwards look for the last .gro file, rename and delete the rest
    
########## INSERTION ENDED  ##########
#######################################################################

# Make global density maps for:
# SAM number density   -> name:  ng_density_SAM_sam${i}_water${j}.xvg
# SAM mass density     -> name:  g_density_SAM_sam${i}_water${j}.xvg
# Water number density -> name:  ng_density_NVT_sam${i}_water${j}.xvg 
# Water mass density   -> name:  g_density_NVT_sam${i}_water${j}.xvg 
    
    echo "0" "q"|make_ndx -f sam${i}_water${j}.gro -o index${i}_${j}.ndx 
 
    #/net/data/eixeres/sheldon-old/gromacs_tpi_compiled/bin/grompp -f NVT_60ns_v2.mdp -c NVT_sam${i}_water${j}.gro -p ${i}pc_${j}.top -n index${i}_${j}.ndx -o g_rad_NVT_sam${i}_water${j}.tpr -maxwarn 1
    grompp -f NVT_60ns_v2.mdp -c NVT_sam${i}_water${j}.gro -p ${i}pc_${j}.top -n index${i}_${j}.ndx -o g_rad_NVT_sam${i}_water${j}.tpr -maxwarn 11
    
    # Calculate mass densities
    #echo ${n} | g_density -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o g_density_NVT_sam${i}_water${j}.xvg -sl 1000
    #echo "6" | g_density -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o g_density_SAM_sam${i}_water${j}.xvg -sl 1000 # for SAMs density maps

    # Calculate number densities   
    #echo ${n} | g_density -dens number -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o ng_density_NVT_sam${i}_water${j}.xvg -sl 1000 
    #echo "5" |g_density -dens number -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o ng_density_SAM_sam${i}_water${j}.xvg -sl 1000

# Copy all files to same folder and delete originals
cp ng_density_SAM_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_SAMS_densmaps/
cp g_density_SAM_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_NVT_densmaps
cp ng_density_SAM_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_SAMS_densmaps/
cp g_density_SAM_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_NVT_densmaps
rm ng_density_NVT_sam${i}_water${j}.xvg	
rm g_density_SAM_sam${i}_water${j}.xvg
rm ng_density_NVT_sam${i}_water${j}.xvg	
rm g_density_SAM_sam${i}_water${j}.xvg

#######################################################################

# Make radial density maps every 500ps

    #k=200
    k=0
    while [[ $k -le 5 ]]  # segments of time to be multiplied by 100 so that we get [ps]
    #while [[ $k -le 995 ]]  # segments of time to be multiplied by 100 so that we get [ps]
    do    
        k2=$((k+5))
        nanosecs1=$(echo $(round $k/10 1))
        nanosecs2=$(echo $(round $k2/10 1))
        start=$((k*100))
        ending=$((start+500))

        #echo "Creating densmap from $start ps to $ending ps"

        echo ${n} ${n} | /net/data/eixeres/sheldon-old/g_rad_density -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -n index${i}_${j}.ndx -sz 200 -o g_rad_dmap_${i}pc_w${j}_${nanosecs1}ns_${nanosecs2}ns.xvg -b ${start} -e ${ending}
        
        cp g_rad_dmap_${i}pc_w${j}_${nanosecs1}ns_${nanosecs2}ns.xvg /net/data/eixeres/Version_v2/radial_densmaps/
        rm g_rad_dmap_${i}pc_w${j}_${nanosecs1}ns_${nanosecs2}ns.xvg
	
	    k=$(($k+5))
	done    
  done
done
