
# coding: utf-8

# In[5]:

import os


# In[6]:

first_text = '; Include forcefield parameters'+ '\n' '#include "gromos53a6.ff/forcefield.itp"'+ '\n' + '\n' '; Include atomtype parameters (old T1.itp)'+ '\n' '#include "repelOH.itp"'+ '\n' + '\n' '; Include molecule parameters'+ '\n' '#include "c10-oh.itp"'+ '\n' '#include "c10-ch3.itp"'+ '\n' + '\n' '; Include water topology'+ '\n' '#include "gromos53a6.ff/spce.itp"'+ '\n' + '\n' '; Position restraint for each water oxygen'+ '\n' '#ifdef POSRES_WATER'+ '\n' '[ position_restraints ]'+ '\n' ';  i funct       fcx        fcy        fcz'+ '\n' '   1    1       1000       1000       1000'+ '\n' '#endif'+ '\n' + '\n' '[ system ]'+ '\n' 'Decanol SAM in water'+ '\n' + '\n' '[molecules]'+ '\n' 


# In[7]:

print first_text


# In[11]:

# New version using variable first_text (instead of copying from benchfile)
#### copy bench top file to the working folder!!! ####

#path to .gro files 
samsfolder = "/Users/burbol/GitHub/LineTensionPackage/SYSTEM_CREATION/gromacs_files/DropsGroTop/NewVersion_v2/"

# All systems
#pc = [0,11,22,33, 37, 44, 50]
#molec = [1000, 2000, 3000, 4000, 5000, 6500, 7000, 8000, 9000, 10000]

# Single system for testing
pc = [11]
molec = [5000]


# VERSION 1 of the new sams 21% & 25% ==> #chain length of the rest:  CH3len2= 62, OHlen2= 63

newCH3itp='c10-ch3.itp'
newOHitp='c10-oh.itp'

#chain length
CH3len= 11     #length of chain with CH3-head groups
OHlen= 12      #length of chain with OH-head groups


# From here everything runs automatically...

for i in pc:
    for j in molec:
        
        os.chdir(samsfolder)
        
        # create and work in a different folder for each system
        separatedfolder='s'+str(i)+'_w'+str(j)
        #os.mkdir(separatedfolder)
        os.chdir(separatedfolder)

        #name of .gro files (input)
        grofile='sam'+str(i)+'_water'+str(j)+'.gro'

        #name of new .top file (output)
        newtop= str(i)+'pc_'+str(j)+'.top'

        # we create the new file by openning and closing it
        #creating = open(newtop, 'w+')
        #creating.close()

        # count number of atoms in c10-Ch3 and c10-oh chains, and number of solvent atoms
        f = open(samsfolder + grofile)
        totalSAM = 0
        totalXOH = 0
        totalSOL = 0
        for line in f:
            if "SAM" in line:
                totalSAM += 1
            elif "XOH" in line:
                totalXOH += 1
            elif "SOL" in line:
                totalSOL += 1
        f.close()

        # determine number of chains
        totalSAM = int(totalSAM/CH3len)
        totalXOH = int(totalXOH/OHlen)

        # determine number of solvent molecules
        totalSOL = int(totalSOL/3)

        # print out calculated numbers
        print "totalSAM=",totalSAM,"totalXOH=",totalXOH,"totalSOL=",totalSOL

        # create new .top file
        with open(newtop, 'w') as f1:
            
            k = 0
            m = 0
            f1.write(first_text)

            # write into new .top file
            with open(samsfolder + grofile, 'r') as h:
                
                # set counters to zero
                lastcountsam=0
                lastcountXOH=0
                
                # write one line for each carbon chain
                for line2 in h:
                    # write one line for each chain with CH3-head group
                    if "SAM" in line2:
                        k = k + 1
                        if k in range(1,(totalSAM*CH3len)+1,CH3len):
                            f1.write("SAM	1\n")
                            lastcountsam += 1
                    # write one line for each chain with OH-head group
                    elif "XOH" in line2:
                        m = m + 1
                        if m in range(1,(totalXOH*OHlen)+1,OHlen):
                            f1.write("XOH	1\n")
                            lastcountXOH += 1
                
            # write number of water molecules at the end of file
            f1.write("SOL	"+str(totalSOL)+"\n")

            # check number of chains and water molecules
            print "lastcount:",lastcountsam,lastcountXOH,totalSOL
            print "just created ", newtop

        #os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(startsamfile, samfile ))
        #This last line would make the .top file include ALSO T1_new.itp
        #os.system("sed -i -e 's/%s/%s/g' %s")% ("#include \"T1.itp\"","#include \"T1.itp\"\n#include \"T1_new.itp\"".itp,newtop, ))


# In[10]:

# Old version using benchfile
#### copy bench top file to the working folder!!! ####

#path to .gro files 
samsfolder = "/Users/eixeres/Dropbox/GitHub/LineTensionPackage/SYSTEM_CREATION/gromacs_files/DropsGroTop/NewVersion_v2/"

#.top file with the right configuration for copying first lines (Alex & Matej's file)
benchfile="/Users/eixeres/Dropbox/GitHub/LineTensionPackage/SYSTEM_CREATION/gromacs_files/state.top"
firstline=11 #first line not to copy (use the real line number, it will recalculated)

# All systems
#pc = [0,11,22,33, 37, 44, 50]
#molec = [1000, 2000, 3000, 4000, 5000, 6500, 7000, 8000, 9000, 10000]

# Single system for testing
pc = [11]
molec = [5000]

newCH3itp='c10-ch3.itp'
newOHitp='c10-oh.itp'

#chain length
CH3len= 11     #length of chain with CH3-head groups
OHlen= 12      #length of chain with OH-head groups


# From here everything runs automatically...

for i in pc:
    for j in molec:

        # create and work in a different folder for each system
        separatedfolder='s'+str(i)+'_w'+str(j)
        os.chdir(samsfolder)
        os.chdir(separatedfolder)

        #name of .gro files (input)
        grofile='sam'+str(i)+'_water'+str(j)+'.gro'

        #name of new .top file (output)
        newtop= str(i)+'pc_'+str(j)+'.top'

        # we create the new file by openning and closing it
        #creating = open(newtop, 'w+')
        #creating.close()

        # count number of atoms in c10-Ch3 and c10-oh chains, and number of solvent atoms
        f = open(grofile)
        totalSAM = 0
        totalXOH = 0
        totalSOL = 0
        for line in f:
            if "SAM" in line:
                totalSAM += 1
            elif "XOH" in line:
                totalXOH += 1
            elif "SOL" in line:
                totalSOL += 1
        f.close()

        # determine number of chains
        totalSAM = int(totalSAM/CH3len)
        totalXOH = int(totalXOH/OHlen)

        # determine number of solvent molecules
        totalSOL = int(totalSOL/3)

        # print out calculated numbers
        print "totalSAM=",totalSAM,"totalXOH=",totalXOH,"totalSOL=",totalSOL

        # create new .top file
        with open(newtop, 'w') as f1:

            # copy first lines from benchfile
            with open(benchfile, 'r') as g:
                l = 0
                k = 0
                m = 0
                for line in g:
                    if l < (firstline-1):
                        f1.write(line)
                    l = l + 1

            # write into new .top file
            with open(grofile, 'r') as h:
                
                # set counters to zero
                lastcountsam=0
                lastcountXOH=0
                
                # write one line for each carbon chain
                for line2 in h:
                    # write one line for each chain with CH3-head group
                    if "SAM" in line2:
                        k = k + 1
                        if k in range(1,(totalSAM*CH3len)+1,CH3len):
                            f1.write("SAM	1\n")
                            lastcountsam += 1
                    # write one line for each chain with OH-head group
                    elif "XOH" in line2:
                        m = m + 1
                        if m in range(1,(totalXOH*OHlen)+1,OHlen):
                            f1.write("XOH	1\n")
                            lastcountXOH += 1
                
            # write number of water molecules at the end of file
            f1.write("SOL	"+str(totalSOL)+"\n")

            # check number of chains and water molecules
            print "lastcount:",lastcountsam,lastcountXOH,totalSOL
            print "just created ", newtop

        #os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(startsamfile, samfile ))
        #This last line would make the .top file include ALSO T1_new.itp
        #os.system("sed -i -e 's/%s/%s/g' %s")% ("#include \"T1.itp\"","#include \"T1.itp\"\n#include \"T1_new.itp\"".itp,newtop, ))


# In[7]:

for i in pc:
    for j in molec: 
        separatedfolder='s'+str(i)+'_w'+str(j)
        os.chdir(samsfolder)
        os.chdir(separatedfolder)
        os.system("rm *.top-e")


# In[9]:

os.system("mkdir reshapingfiles")
os.system("cp *_c.gro reshapingfiles/")
os.system("rm *_c.gro")


# In[2]:

######## THIS CELL IS FOR TESTING WHICH LINES ARE COUNTED AND THE ATOM NUMBERS #########
samsfolder = "/Users/burbol/Desktop/scripts/SAM_CREATION/SAMs/NEW/drop_placement" #path to .gro files
i=21
j=216
CH3len= 65     #length of chain with CH3-head groups
CH3len2= 62
OHlen= 63      #length of chain with OH-head groups
OHlen2= 63

#totalSAM = int(totalSAM)
#totalXOH = int(totalXOH)
#totalSAM2 = int(totalSAM)
#totalXOH2 = int(totalXOH)
#totalSOL = int(totalSOL)

systfile='sam'+str(i)+'_water'+str(j)+'.gro' #name of .gro files
os.chdir(samsfolder)
f = open(systfile)
k = 0
l = 0
m = 0
for line in f:
    if "SAM" in line:
        k += 1
        if i!=33 and k in range(1,(totalSAM*CH3len2)+1,CH3len2):
            print line
        elif i==33 and k in range(1,(totalSAM*CH3len)+1,CH3len):
            print line
    elif "XOH" in line:
        l += 1
        if i!=33 and l in range(1,(totalXOH*OHlen2)+1,OHlen2):
            print line
        elif i==33 and l in range(1,(totalXOH*OHlen)+1,OHlen):
            print line
    elif "SOL" in line:
        print line
        m += 1  
    
f.close()

#k = (k)/CH3len
#l = l/OHlen
#k2 = (k)/CH3len2
#l2 = l/OHlen2
m = m/3
print "last molec count:",totalSAM,totalXOH,totalSOL
print "new count:", k,l,m


# In[ ]:



