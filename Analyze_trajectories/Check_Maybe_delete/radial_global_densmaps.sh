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


n=4


#mkdir /net/data/eixeres/Version_v2/global_SAMS_densmaps
#mkdir /net/data/eixeres/Version_v2/global_NVT_densmaps
#mkdir /net/data/eixeres/Version_v2/radial_densmaps

for i in 44 37 33 22 11 0 50 # OH density of the SAM
do
  for j in 10000 9000 8000 7000 6500  # number of water molecules
  do

  #cd /net/data/eixeres/Version_v2/FINISHED/s${i}_w${j} # First Round all systems
  cd /net/data03/eixeres/scratch_yoshi/Version_v2/s${i}_w${j} # Second round big systems (small still running on sheldon-ng)
  
  if [ $i -eq 0 ]
  then 
    n=3
    m=2
  else 
    n=4
    m=6
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

# Choose starting and ending times for the density map
beg_time=90
end_time=100
# Convert time units
beg_time=$((beg_time*1000))
end_time=$((end_time*1000))

    #echo "0" "q"|gmx make_ndx -f NVT_sam${i}_water${j}.gro -o index${i}_${j}.ndx 
 
    #gmx grompp -f NVT_80ns_v2.mdp -c NVT_sam${i}_water${j}.gro -p ${i}pc_${j}.top -n index${i}_${j}.ndx -o g_rad_NVT_sam${i}_water${j}.tpr -maxwarn 11
    
    #Calculate mass densities
    echo ${n} | gmx density -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o g_density_NVT_sam${i}_water${j}.xvg -sl 1000 -b ${beg_time} -e ${end_time}
    echo ${m} | gmx density -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o g_density_SAM_sam${i}_water${j}.xvg -sl 1000 -b ${beg_time} -e ${end_time} # for SAMs density maps

    #Calculate number densities   
    echo ${n} | gmx density -dens number -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o ng_density_NVT_sam${i}_water${j}.xvg -sl 1000 -b ${beg_time} -e ${end_time}
    echo ${m} |gmx density -dens number -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -o ng_density_SAM_sam${i}_water${j}.xvg -sl 1000 -b ${beg_time} -e ${end_time}

#Copy all files to same folder and delete originals
mv ng_density_SAM_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_SAMS_densmaps/ng_density_NVT_sam${i}_water${j}.xvg
mv ng_density_NVT_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_NVT_densmaps/ng_density_SAM_sam${i}_water${j}.xvg

mv g_density_SAM_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_SAMS_densmaps/g_density_SAM_sam${i}_water${j}.xvg
mv g_density_NVT_sam${i}_water${j}.xvg  /net/data/eixeres/Version_v2/global_NVT_densmaps/g_density_NVT_sam${i}_water${j}.xvg

#######################################################################


#######################################################################
# For the second round each simulation starts at a different time k
    if [ $j -eq 6500 ]
    then k=600
    elif [ $j -eq 7000 ]
    then k=800
    elif [ $j -eq 8000 ]
    then k=800
    elif [ $j -eq 9000 ]
    then k=800
    elif [ $j -eq 10000 ]
    then k=1000
    elif [ $j -eq 1000 ]
    then k=600
    elif [ $j -eq 2000 ]
    then k=600
    elif [ $j -eq 3000 ]
    then k=600
    elif [ $j -eq 4000 ]
    then k=600
    elif [ $j -eq 5000 ]
    then k=600
    fi
#######################################################################

# # Make radial density maps every 500ps
# 
# # Load old GROMACS for compatibility with g_rad_density 
# GMXLIB="/net/data/eixeres/sheldon-old/gromacs_tpi_compiled/share/gromacs/top/"
# 
# # Use old version of grompp with old version of .top file
# /net/data/eixeres/sheldon-old/gromacs_tpi_compiled/bin/grompp -f NVT_60ns_v2.mdp -c NVT_sam${i}_water${j}.gro -p ${i}pc_${j}_old.top -n index${i}_${j}.ndx -o g_rad_NVT_sam${i}_water${j}.tpr -maxwarn 11
# 
#     
#     
#     #k=180
#     #k=0
#     while [[ $k -le 1995 ]]  # segments of time to be multiplied by 100 so that we get [ps]
#     do    
#         k2=$((k+5))
#         nanosecs1=$(echo $(round $k/10 1))
#         nanosecs2=$(echo $(round $k2/10 1))
#         start=$((k*100))
#         ending=$((start+500))
# 
#         echo "Creating densmap from $start ps to $ending ps"
# 
#         echo ${n} ${n} | /net/data/eixeres/sheldon-old/g_rad_density -f NVT_sam${i}_water${j}.xtc -s g_rad_NVT_sam${i}_water${j}.tpr -n index${i}_${j}.ndx -sz 200 -o g_rad_dmap_${i}pc_w${j}_${nanosecs1}ns_${nanosecs2}ns.xvg -b ${start} -e ${ending}
#         
#         mv g_rad_dmap_${i}pc_w${j}_${nanosecs1}ns_${nanosecs2}ns.xvg /net/data/eixeres/Version_v2/radial_densmaps/s${i}_w${j}/g_rad_dmap_${i}pc_w${j}_${nanosecs1}ns_${nanosecs2}ns.xvg
# 	
# 	    k=$(($k+5))
# 	done    
  done
done