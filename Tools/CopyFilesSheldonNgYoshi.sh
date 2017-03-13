#!/bin/bash

cd /Users/eixeres/Dropbox/GitHub/LineTensionPackage/Tools/SubmissionScripts/Extend/ 

#################################
# For testing:

#for i in 0 
#do
#	for j in 1000
#    do
#################################

for i in 0 11 22 33 37 44 50 # OH density of the SAM
do
	for j in 1000 2000 3000 4000 5000 6500 7000 8000 9000 10000  # number of water molecules
   do
  
  	# copy to sheldon-ng
  	#scp s${i}_w${j}/* eixeres@sheldon-ng.physik.fu-berlin.de:/scratch/eixeres/Version_v2/scripts/s${i}_w${j}/
  	# copy to yoshi
  	scp s${i}_w${j}/pairtypes.itp eixeres@yoshi.physik.fu-berlin.de:/scratch/eixeres/Version_v2/scripts/s${i}_w${j}/

  done
done