#!/bin/bash

for i in 0 11 22 33 37 44 50 # OH density of the SAM 
do
  for j in 1000 2000 3000 4000 5000 6500
  do
    cd /scratch/eixeres/Version_v2.2/s${i}_w${j}
    
    cp ${i}pc_${j}.top ${i}pc_${j}_old.top
    #/net/data03/eixeres/Version_v2.2/s11_w2000/ 
    
    cd ..  
  done
done