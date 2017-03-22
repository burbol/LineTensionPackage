#!/bin/bash

#script to change text inside numbered script

for i in 11 22 33 37 44 50
do
  for j in 1000 2000 3000 4000 5000
  do
    cd /Users/eixeres/Dropbox/GitHub/LineTensionPackage/Tools/SubmissionScripts/Extend/s${i}_w${j}

    file1=s${i}_w${j}_1
    file2=s${i}_w${j}_2

    sed -ie 's/scripts/scripts_sheldon-ng/g' $file1
    sed -ie 's/scripts/scripts_sheldon-ng/g' $file2    
    
   done
done