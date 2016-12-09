#!/bin/bash

cd /Users/burbol/MEGAsync/scripts/Python/SCRIPT_CREATION/sheldon/

for i in 25 # OH density of the SAM 
do
	for j in 1000 2000 3000 4000 5000 6500 7000 8000 9000 10000  # number of water molecules

  do 

  	scp /Users/burbol/MEGAsync/scripts/Python/SCRIPT_CREATION/sheldon/s${i}_w${j}/s${i}_w${j}_2 eixeres@sheldon.physik.fu-berlin.de:/home/eixeres/Dec14_Last_Sims/s${i}_w${j}/
  	scp /Users/burbol/MEGAsync/scripts/Python/SCRIPT_CREATION/sheldon/s${i}_w${j}/s${i}_w${j}_3 eixeres@sheldon.physik.fu-berlin.de:/home/eixeres/Dec14_Last_Sims/s${i}_w${j}/
  	scp /Users/burbol/MEGAsync/scripts/Python/SCRIPT_CREATION/sheldon/s${i}_w${j}/s${i}_w${j}_4 eixeres@sheldon.physik.fu-berlin.de:/home/eixeres/Dec14_Last_Sims/s${i}_w${j}/
  	

  done
done