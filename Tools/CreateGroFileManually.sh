#!/bin/bash

# Script to create .gro file manually from crashed simulation
# READ FILE "CreateGroFileManually.rtf"
# script must be updated for GROMACS 5 (written for version 4, but next line loads module of version 5)
# Run from server

module load gromacs/single/2016.1

for i in 44 37 33 22 11 0 50 # OH density of the SAM
do
  for j in 10000 9000 8000 7000 6500 5000 4000 3000 2000 1000  # number of water molecules
  do

  cd /net/data03/eixeres/scratch_yoshi/Version_v2/s${i}_w${j}

# set approximate ending time (temp) for each system needed
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
    
    echo "0"|/home/shavkat/GMX/bin/trjconv -f NVT_sam${i}_water${j}.xtc # watch output for last frame determination
    /home/shavkat/GMX/bin/grompp -f NVT_60ns_v2.mdp -p ${i}pc_${j}.top -t NVT_sam${i}_water${j}.trr -c Mini_sam${i}_water${j}.gro -o NVT_sam${i}_water${j}_temp.tpr -maxwarn 2
    echo "0"|/home/shavkat/GMX/bin/trjconv -f NVT_sam${i}_water${j}.xtc  -s NVT_sam${i}_water${j}_temp.tpr -o NVT_sam${i}_water${j}_temp.gro -b $temp -sep
    #Afterwards look for the last .gro file, rename and delete the rest
    