
import numpy as np
import os

#### copy bench top file t```o the working folder!!! ####
#### AFTER RUNNING placedrop.ipynb rename the created sam files. (One line was added for this!) ####
#### F.ex: from NPT_sam22_water2000.gro to sam22_water2000.gro ####
i=50
j=10000
#samsfolder = "/Users/burbol/MEGAsync/scripts/SAM_CREATION/SAMs/NEW/drop_placement/DropsGroTop" #path to .gro files
samsfolder = "/Volumes/Backup/YosemiteFiles/MEGAsync/scripts/SAM_CREATION/SAMs/NEW/drop_placement/NewVersion3/" #path to .gro files

benchfile=str(i)+'pc_'+str(j)+'.top' #.top file with the right configuration to copy
firstline=25 #first line to copy (use the real line number, it will recalculated) ---> uncomment and check

#pc = [33, 50]
#molec = [216, 1000, 2000, 3000, 4000, 5000, 6500, 7000, 8000, 9000, 10000]
pc = [21,25]
molec = [1000, 2000, 3000, 4000, 5000, 6500, 7000, 8000, 9000, 10000]
#molec = [1000,2000, 3000, 4000, 5000]

# VERSION 1 of the new sams 21% & 25% ==> #chain length of the rest:  CH3len2= 62, OHlen2= 63

newCH3itp='CH3version2.itp'
newOHitp='OHversion2.itp'
oldCH3itp="CH3new.itp"
oldOHitp="OHnew.itp" 

#chain length of sam 33%
CH3len= 65     #length of chain with CH3-head groups
OHlen= 63      #length of chain with OH-head groups

#chain length of the rest  
CH3len2= 65
OHlen2= 63

# From here everything runs automatically...

os.chdir(samsfolder)
for i in pc:
    for j in molec: 
        
        separatedfolder='s'+str(i)+'_w'+str(j)
        os.chdir(samsfolder)
        os.chdir(separatedfolder)
        systfile='sam'+str(i)+'_water'+str(j)+'.gro' #name of .gro files       
        newtop= str(i)+'pc_'+str(j)+'.top' #name of new .top file

        # we create the new file by openning and closing it
        #creating = open(newtop, 'w+')
        #creating.close()
        
        f = open(systfile)
        totalSAM = 0
        totalOAM = 0
        totalSOL = 0
        for line in f:
            if "SAM" in line:
                totalSAM += 1
            elif "OAM" in line:
                totalOAM += 1
            elif "SOL" in line:
                totalSOL += 1
            #print i, j
        f.close()
        if i==33:
            totalSAM = int(totalSAM/CH3len)
            totalOAM = int(totalOAM/OHlen)
        elif i!=33:
            totalSAM = int(totalSAM/CH3len2)
            totalOAM = int(totalOAM/OHlen2)
        totalSOL = int(totalSOL/3)
        #print "totalSAM=",totalSAM,"totalOAM=",totalOAM,"totalSOL=",totalSOL

        with open(newtop, 'w') as f1:  ##### TEST!!!!
            with open('../'+benchfile, 'r') as g:
                l = 0
                k = 0
                m = 0
                for line in g:                    
                    if l < (firstline-1): 
                        f1.write(line) 
                    l = l + 1
            with open(systfile, 'r') as h:
                lastcountsam=0
                lastcountoam=0
                for line2 in h:
                    if "SAM" in line2:
                        k = k + 1
                        if i!=33 and k in range(1,(totalSAM*CH3len2)+1,CH3len2):
                            f1.write("SAM	1\n")
                            lastcountsam+= 1
                        elif i==33 and k in range(1,(totalSAM*CH3len)+1,CH3len):
                            f1.write("SAM	1\n")
                            lastcountsam+= 1
                    elif "OAM" in line2:
                        m = m + 1
                        if i!=33 and m in range(1,(totalOAM*OHlen2)+1,OHlen2):
                            f1.write("OAM	1\n")
                            lastcountoam+= 1
                        elif i==33 and m in range(1,(totalOAM*OHlen)+1,OHlen):
                            f1.write("OAM	1\n")
                            lastcountoam+= 1
                    
                #f1.write("SAM	"+str(totalSAM)+"\n")
                #f1.write("OAM	"+str(totalOAM)+"\n")
            
            f1.write("SOL	"+str(totalSOL)+"\n")
            
            print "lastcount:",lastcountsam,lastcountoam,totalSOL
            print "just created ", newtop
        if i!=33:
            os.system("sed -i -e 's/%s/%s/g' %s" %(oldCH3itp,newCH3itp,newtop ))
            os.system("sed -i -e 's/%s/%s/g' %s" %(oldOHitp,newOHitp,newtop ))
                
        #os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(startsamfile, samfile ))
        #This last line would make the .top file include ALSO T1_new.itp
        #os.system("sed -i -e 's/%s/%s/g' %s")% ("#include \"T1.itp\"","#include \"T1.itp\"\n#include \"T1_new.itp\"".itp,newtop, ))

os.system("rm *.top-e")

os.system("mkdir reshapingfiles")
os.system("cp *_c.gro reshapingfiles/")
os.system("rm *_c.gro")

######## THIS CELL IS FOR TESTING WHICH LINES ARE COUNTED AND THE ATOM NUMBERS #########
samsfolder = "/Users/burbol/MEGAsync/scripts/SAM_CREATION/SAMs/NEW/drop_placement/DropsGroTop" #path to .gro files
i=21
j=6500
CH3len= 65     #length of chain with CH3-head groups
CH3len2= 62
OHlen= 63      #length of chain with OH-head groups
OHlen2= 63

#totalSAM = int(totalSAM)
#totalOAM = int(totalOAM)
#totalSAM2 = int(totalSAM)
#totalOAM2 = int(totalOAM)
#totalSOL = int(totalSOL)

systfile='sam'+str(i)+'_water'+str(j)+'.gro' #name of .gro files
os.chdir(samsfolder)
f = open(systfile)
k = 0
l = 0
m = 0
linenumber=0
#for line in f:
#    if "SAM" in line:
#        k += 1
#        if i!=33 and k in range(1,(totalSAM*CH3len2)+1,CH3len2):
#            #print line
#            print linenumber
#        elif i==33 and k in range(1,(totalSAM*CH3len)+1,CH3len):
#            #print line
#            print linenumber
#    elif "OAM" in line:
#        l += 1
#        if i!=33 and l in range(1,(totalOAM*OHlen2)+1,OHlen2):
#            #print line
#            print linenumber           
#        elif i==33 and l in range(1,(totalOAM*OHlen)+1,OHlen):
#            #print line
#            print linenumber
#    elif "SOL" in line:
#        #print line
#        print linenumber
#        m += 1  
#    linenumber=linenumber+1
#f.close()

with open(benchfile, 'r') as g:
    for line in g:
        if "Compound" in line:
            print linenumber
        linenumber=linenumber+1
g.close()


#k = (k)/CH3len
#l = l/OHlen
#k2 = (k)/CH3len2
#l2 = l/OHlen2
m = m/3
print "last molec count:",totalSAM,totalOAM,totalSOL
print "new count:", k,l,m

 
