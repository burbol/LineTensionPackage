#!/bin/bash

# Run from server
# Delete files recursively

cd /scratch/eixeres/Version_v2

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
  
  	cd s${i}_w${j}
  	rm \#*
  	cd ..
  	
  done
done