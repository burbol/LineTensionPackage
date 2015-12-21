#!/bin/bash

#!!!!!CALL THIS SCRIPT WITH 6 ARGUMENTS:
# 1-> FILE NAME
# 2-> PERCENTAGE (for ex: 50 for 50%)
# 3-> number of copies in x-direction
# 4-> x-length of simulation box
# 5-> number of copies in y-direction
# 6-> y-length of simulation box

#cd /home/eixeres/Downloads/SAMs/NEW
#cd /Users/burbol/Desktop/scripts/SAM_CREATION/SAMs/NEW
#cd /Users/burbol/MEGAsync/scripts/SAM_CREATION/SAMs/NEW/drop_placement
cd /Users/burbol/MEGAsync/scripts/SAM_CREATION/EstendSAMs

startfile=$1
pc=$2

xtimes=$3
xdist=$(echo "$4" | bc)
ytimes=$5
ydist=$(echo "$6" | bc)
####################from here nothing needs to be changed ###################

newfolder=$pc'reshape'
mkdir $newfolder

source /usr/local/gromacs/bin/GMXRC

for (( i=0; i<=$xtimes; i++ ))
do
for (( j=0; j<=$ytimes; j++ ))
do

x=$(echo "$i*$xdist" | bc)
y=$(echo "$j*$ydist" | bc)

endfile=$i$j$startfile

editconf -f $startfile -o $endfile -translate $x $y 0 
mv $endfile ./$newfolder

# NEXT 4 LINES ONLY FOR TESTING
#echo "x= ${x} , y= $y"
#echo "i= ${i} , j= $j"
#echo "editconf -f $startfile -o $endfile -translate $x $y 0 "
#echo "mv $endfile ./$newfolder"

done
done
