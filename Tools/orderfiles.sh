#!/bin/bash

# This script moves files to different folders corresponding to each system

#folder where the .xvg files are saved together
cd /Volumes/Version_v2/Version_v2.2/Simulations_xtc_distilled

for i in 0 11 22 33 37 44 50
do
  for j in 1000 2000 3000 4000 5000 6500 7000 8000 9000 10000
  do
	mkdir s${i}_w${j}
	# using "cp" and "rm" instead of "mv" because of wildcard character "*"
	cp NVT_sam${i}_water${j}.gro ./s${i}_w${j}/
	cp NVT_sam${i}_water${j}_dil.xtc ./s${i}_w${j}/
		
	#rm NVT_sam${i}_water${j}.gro
	#rm NVT_sam${i}_water${j}_dil.xtc
  
  done
done