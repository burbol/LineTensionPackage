#!/bin/bash

cd /Users/eixeres/Dropbox/GitHub/LineTensionPackage/SYSTEM_CREATION/gromacs_files/SAM_startfiles_v2_36x36/NewVersion_v2/

#for i in 0 11 22 33 37 44 50 # OH density of the SAM 
for i in 0 # OH density of the SAM 
do
	for j in 1000 2000 3000 4000 5000 6500 7000 8000 9000 10000  # number of water molecules

  do 
    # old command for reference
  	#scp /Users/burbol/MEGAsync/scripts/Python/SCRIPT_CREATION/sheldon/s${i}_w${j}/s${i}_w${j}_2 eixeres@sheldon.physik.fu-berlin.de:/home/eixeres/Dec14_Last_Sims/s${i}_w${j}/
  	
  	# copy to sheldon-ng
  	scp s${i}_w${j}/*.top eixeres@sheldon-ng.physik.fu-berlin.de:/scratch/eixeres/Version_v2/s${i}_w${j}/
  	# copy to yoshi
  	scp s${i}_w${j}/*.top eixeres@yoshi.physik.fu-berlin.de:/scratch/eixeres/Version_v2/s${i}_w${j}/  	

  done
done