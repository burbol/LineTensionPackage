
# coding: utf-8

# In[1]:

import numpy as np
import os


# In[24]:

filesfolder='/Users/burbol/Desktop/scripts/SAM_CREATION/SAMs/NEW/drop_placement'
CH3file= 's21singlechainCH3.gro'
OHfile= 's21singlechainOH.gro'
benchCH3itp = 'CH3.itp'
benchOHitp = 'OH.itp'
newCH3itp='CH3version2.itp'
newOHitp='OHversion2.itp'

os.chdir(filesfolder)


#################### CH3.itp  ######################
linecnt=0
indexC=1
indexH=1
position=1
with open(newCH3itp, 'w') as CH3new:
    with open(benchCH3itp, 'r') as CH3old:
        for line in CH3old:
            if linecnt <= 5:
                CH3new.write(line)
                linecnt = linecnt+1
    with open(CH3file, 'r') as CH3gro:
        for line in CH3gro:
            if "C" in line:
                #CH3new.write("     %2d       %s        1    SAM      %s%d       %2d         0.000    12.0110\n" %(position,"C", "C",indexC,position))
                CH3new.write("%7d%8s%9s%7s%9s%8d         0.000    12.0110\n" %(position,"C","1","SAM", "C"+str(indexC),position))               
                position = position +1
                indexC = indexC +1

            elif "H" in line and "sam" not in line:
                #CH3new.write("     %2d       %s        1    SAM      %s%d       %2d         0.000     1.0080\n" %(position,"H", "H",indexH,position))
                CH3new.write("%7d%8s%9s%7s%9s%8d         0.000    1.0080\n" %(position,"H","1","SAM", "H"+str(indexH),position))
                position = position +1
                indexH = indexH +1
            

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
            if "C" in line:
                #OHnew.write("     %2d       %s        1    SAM      %s%d       %2d         0.000    12.0110\n" %(position,"C", "C",indexC,position))
                OHnew.write("%7d%8s%9s%7s%9s%8d         0.000    12.0110\n" %(position,"C","1","OAM", "C"+str(indexC),position))
                position = position +1
                indexC = indexC +1

            elif "H" in line and "sam" not in line:
                #OHnew.write("     %2d       %s        1    SAM      %s%d       %2d         0.000     1.0080\n" %(position,"H", "H", indexH,position))
                OHnew.write("%7d%8s%9s%7s%9s%8d         0.000    1.0080\n" %(position,"H","1","OAM", "H"+str(indexH),position))
                position = position +1
                indexH = indexH +1
                
            elif "O" in line and "sam" not in line:
                #OHnew.write("     %2d       %s        1    SAM      %s%d       %2d         0.000     1.0080\n" %(position,"OT", "O",indexO,position))
                OHnew.write("%7d%8s%9s%7s%9s%8d         -0.734    15.9990\n" %(position,"OT","1","OAM", "O"+str(indexO),position))
                position = position +1
                indexO = indexO +1
    


# In[ ]:

#Change this cell to subtitute lines with "C" and "H" atoms with charges
#if i!=33:
    #os.system("sed -i -e 's/%s/%s/g' %s" %("CH3_long.itp",newCH3itp,newtop ))
    #os.system("sed -i -e 's/%s/%s/g' %s" %("OH.itp",newOHitp,newtop ))

