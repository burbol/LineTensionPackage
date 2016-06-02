
# coding: utf-8

# In[1]:

import numpy as np
import os


# In[2]:

# The function namecarbons() was copied from pdbfile_v2.py (could also be imported)
def namecarbons(indexC):
	if indexC == 1:
		atomtype = 'CAL'
	if indexC == 2:
		atomtype = 'CAK'
	if indexC == 3:
		atomtype = 'CAJ'
	if indexC == 4:
		atomtype = 'CAI'
	if indexC == 5:
		atomtype = 'CAH'
	if indexC == 6:
		atomtype = 'CAG'
	if indexC == 7:
		atomtype = 'CAF'
	if indexC == 8:
		atomtype = 'CAE'
	if indexC == 9:
		atomtype = 'CAD'
	if indexC == 10:
		atomtype = 'CAC'
	if indexC == 11:
		atomtype = 'CAB'
	else:
		atomtype = 'CAL' # added this line because of python doesnt accept the function without it
	return atomtype


# In[4]:

filesfolder='/Users/eixeres/Dropbox/GitHub/LineTensionPackage/SYSTEM_CREATION/gromacs_files'
OHfile = 'singlechain_XOH_v2.gro'
CH3file = 'singlechain_SAM_v2.gro'
benchCH3itp = 'c10-ch3.itp'
benchOHitp = 'c10oh.itp'
newCH3itp='newCH3.itp'
newOHitp='newOH.itp'

os.chdir(filesfolder)

#################### CH3.itp  ######################
linecnt=0
indexC=1
indexH=1
position=1
# Open .itp files for CH3-ended chains
with open(newCH3itp, 'w') as CH3new:
    with open(benchCH3itp, 'r') as CH3old:
        #copy the first 5 lines
        for line in CH3old:
            if linecnt <= 5:
                CH3new.write(line)
                linecnt = linecnt+1
    # Open .gro file with single CH3-ended chain
    with open(CH3file, 'r') as CH3gro:
        for line in CH3gro:
            # the first and last atom groups are the head groups with bigger mass
            if ("CAL" in line) or ("CAB" in line):    
                CH3new.write("%7d%8s%9s%7s%9s%8d         0.000    15.0000\n" %(position,"CH3","1","SAM", namecarbons(indexC) ,position))               
                position = position +1
                indexC = indexC +1
                print "one"

            elif ("CAL" not in line) and ("CAB" not in line) and ("1SAM" in line):
                CH3new.write("%7d%8s%9s%7s%9s%8d         0.000    14.0000\n" %(position,"CH2","1","SAM", namecarbons(indexC),position))
                position = position +1
                indexC = indexC +1
                print "two"
            

#################### OH.itp  ######################  
linecnt=0
indexC=1
indexH=1
indexO=1
position=1
with open(newOHitp, 'w') as OHnew:
    with open(benchOHitp, 'r') as OHold:
        for line in OHold:
            if linecnt <= 5:
                OHnew.write(line)
                linecnt = linecnt+1
    with open(OHfile, 'r') as OHgro:
        for line in OHgro:
            print line
            if "HAA" in line: # bonded hydrogen
                print "if-statementnt HAA: indexC =", indexC
                OHnew.write("%7d%8s%9s%7s%9s%8d         0.000    1.0000\n" %(position,"H","1","XOH", "HAA",position))
                position = position +1
                indexH = indexH +1

            elif "OAA" in line: # bonded oxygen
                print "if-statementnt OAA: indexC =", indexC
                OHnew.write("%7d%8s%9s%7s%9s%8d         0.000    16.0000\n" %(position,"OA","1","XOH", "OAA",position))
                position = position +1
                indexO = indexO +1
                
            elif "CAC" in line: # bottom head group (CH3)
                print "if-statementnt CAC - CH3: indexC =", indexC
                OHnew.write("%7d%8s%9s%7s%9s%8d         0.000    15.0000\n" %(position,"CH3","1","XOH", namecarbons(indexC),position))
                position = position +1
                indexC = indexC +1
                
            elif ("CAC" not in line) and ("OAA" not in line) and ("OAA" not in line) and ("1XOH" in line): # all other molecules in the chain (CH2)
                print "if-statementnt CH2: indexC =", indexC
                OHnew.write("%7d%8s%9s%7s%9s%8d         0.000    14.0000\n" %(position,"CH2","1","XOH", namecarbons(indexC),position))
                position = position +1
                indexC = indexC +1
    


# In[ ]:



