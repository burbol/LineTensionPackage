#!/bin/bash

# Run from server
# Delete files recursively

##################################################################
# For testing:

#for i in 0 
#do
#	for j in 1000
#    do
##################################################################

##################################################################
# For droplet simulations

#cd /scratch/eixeres/Version_v2

#for i in 0 11 22 33 37 44 50 # OH density of the SAM
#do
#	for j in 1000 2000 3000 4000 5000 6500 7000 8000 9000 10000  # number of water molecules
#   do 
#  
#  	cd s${i}_w${j}
#  	rm \#*
#  	cd ..
# 	
#  done
#done
##################################################################

##################################################################
# For planar systems (bilayers)

cd /net/data/eixeres/Version_v2/FINISHED/Planar_Systems

for i in 0 11 22 33 37 44 50 # OH density of the SAM
do
  
  	cd s${i}
  	rm \#*
  	cd ..
  	
done
##################################################################