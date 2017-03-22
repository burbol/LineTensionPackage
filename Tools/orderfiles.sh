#!/bin/bash

# This script moves the .xvg files (density profiles) to different folders corresponding to each system

#folder where the .xvg files are saved together
cd /Volumes/UNI/radial_densmaps_Version_v2

for i in 0 11 22 33 37 44 50
do
  for j in 1000 2000 3000 4000 5000 6500 7000 8000 9000 10000
  do
	mkdir s${i}_w${j}
	# using "cp" and "rm" instead of "mv" because of wildcard character "*"
	cp g_rad_dmap_${i}pc_w${j}_*ns.xvg ./s${i}_w${j}/
	rm g_rad_dmap_${i}pc_w${j}_*ns.xvg
  
  done
done