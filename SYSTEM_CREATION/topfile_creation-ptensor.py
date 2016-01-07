
import numpy as np
import os

#### copy bench top file to the working folder!!! ####


#i=21
#j=1000
#benchfile=str(i)+'pc_'+str(j)+'.top' #.top file with the right configuration to copy
benchfile='0pc_double.top' 
firstline=24 #first line to copy (use the real line number, it will recalculated)

samsfolder = "/Users/burbol/Downloads/small_sams2/WaterSamSeparated/RESULTS" #path to .gro files
#samsfolder = '/Users/burbol/Downloads/small_sams2/w'+str(i) #path to .gro files

#pc = [0,5, 11, 17,21,25, 33, 50,66]
pc = [25]

# VERSION 1 of the new sams 21% & 25% ==> #chain length of the rest:  CH3len2= 62, OHlen2= 63

CH3itp='CH3.itp'  #
newCH3itp='CH3_long.itp'
newCH3itp2='CH3version2.itp'
OHitp='OH.itp'
newOHitp='OHversion2.itp'

#chain length of sam 0%
CH3len= 62    #length of chain with CH3-head groups
#OHlen= 63      #length of chain with OH-head groups

#chain length of the rest  
CH3len2= 65
OHlen2= 63

# From here everything runs automatically...
os.chdir(samsfolder)
for i in pc:
    print i
    #systfile='NPT_PR2_water'+str(i)+'_double.gro 
    #newtop= str(i)+'pc_double.top' #name of new .top file
    systfile='sam'+str(i)+'_water_ptensor.gro' #name of .gro files        
    newtop= 'sam'+str(i)+'_water_ptensor.top' #name of new .top file

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
        #elif " O1" in line: #for sam11
            #totalOAM += 1
            #print line
    f.close()
    if i==0:
        totalSAM = int(totalSAM/CH3len)
        #totalOAM = int(totalOAM/OHlen)
    elif i!=0:
        totalSAM = int(totalSAM/CH3len2)
        totalOAM = int(totalOAM/OHlen2)
    totalSOL = int(totalSOL/3)
    print "totalSAM=",totalSAM,"totalOAM=",totalOAM,"totalSOL=",totalSOL

    with open(newtop, 'w') as f1:  ##### TEST!!!!
        with open(benchfile, 'r') as g:
            l = 0
            k = 0
            m = 0
            for line in g: 
                if l < firstline-1: 
                    if l == 3 and i!=0:
                        f1.write(line)
                        f1.write('#include "OH.itp"\n')
                    else:
                        f1.write(line)
                l = l + 1
        with open(systfile, 'r') as h:
            lastcountsam=0
            lastcountoam=0
            for line2 in h:
                if "SAM" in line2:
                    k = k + 1
                    if i!=0 and k in range(1,(totalSAM*CH3len2)+1,CH3len2):
                        f1.write("SAM	1\n")
                        lastcountsam+= 1
                    elif i==0 and k in range(1,(totalSAM*CH3len)+1,CH3len):
                        f1.write("SAM	1\n")
                        lastcountsam+= 1
                elif "OAM" in line2:
                    #print lastcountoam, ':', line2
                #elif "O1" in line2:   #for sam11
                    m = m + 1
                    if i!=0 and m in range(1,(totalOAM*OHlen2)+1,OHlen2):
                        f1.write("OAM	1\n")
                        lastcountoam+= 1
                    elif i==0 and m in range(1,(totalOAM*OHlen)+1,OHlen):
                        f1.write("OAM	1\n")
                        lastcountoam+= 1
                
            #f1.write("SAM	"+str(totalSAM)+"\n")
            #f1.write("OAM	"+str(totalOAM)+"\n")
        
        f1.write("SOL	"+str(totalSOL)+"\n")
        
        print "lastcount:",lastcountsam,lastcountoam,totalSOL
        print "just created ", newtop
    if i==0:
        os.system("sed -i -e 's/%s/%s/g' %s" %("CH3.itp",CH3itp,newtop ))
    elif i==21 or i==25 or i==50:
        os.system("sed -i -e 's/%s/%s/g' %s" %("CH3.itp",newCH3itp2,newtop ))
        os.system("sed -i -e 's/%s/%s/g' %s" %("OH.itp",newOHitp,newtop ))
    else:
        os.system("sed -i -e 's/%s/%s/g' %s" %("CH3.itp",newCH3itp,newtop ))
        #os.system("sed -i -e 's/%s/%s/g' %s" %("OH.itp",OHitp,newtop ))
            
    #os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(startsamfile, samfile ))
    #This last line would make the .top file include ALSO T1_new.itp
    #os.system("sed -i -e 's/%s/%s/g' %s")% ("#include \"T1.itp\"","#include \"T1.itp\"\n#include \"T1_new.itp\"".itp,newtop, ))

 os.system("rm *.top-e")

# THIS CELLS WRITES ONLY THE TOTAL NUMBERS OF ATOMS IN THE TOP FILES
#### copy bench top file to the working folder!!! ####

#i=21
#j=1000
#benchfile=str(i)+'pc_'+str(j)+'.top' #.top file with the right configuration to copy
benchfile='0pc_double.top' 
firstline=24 #first line to copy (use the real line number, it will recalculated)

samsfolder = "/Users/burbol/Downloads/small_sams2" #path to .gro files

#pc = [5, 17, 33, 66]
pc = [66]

CH3itp='CH3.itp'
newCH3itp='CH3_long.itp'
newCH3itp2='CH3version2.itp'
OHitp='OH.itp'
newOHitp='OHversion2.itp'

#chain length of sam 0%
CH3len= 62    #length of chain with CH3-head groups
OHlen= 65      #length of chain with OH-head groups #for sam66

#chain length of the rest  
CH3len2= 65
OHlen2= 63

# From here everything runs automatically...

os.chdir(samsfolder)
for i in pc:
    #systfile='NPT_PR2_water'+str(i)+'_double.gro 
    #newtop= str(i)+'pc_double.top' #name of new .top file
    systfile='sam'+str(i)+'_water_ptensor.gro' #name of .gro files        
    newtop= str(i)+'pc_ptensor.top' #name of new .top file
    
    # we create the new file by openning and closing it
    #creating = open(newtop, 'w+')
    #creating.close()
    
    f = open(systfile)
    totalSAM = 0
    totalOAM = 0
    totalSOL = 0
    for line in f:
        if "OAM" in line:
            totalOAM += 1
        elif "SAM" in line:
            totalSAM += 1
        elif "SOL" in line:
            totalSOL += 1
        #if " O1" in line: #for sam11
            #totalOAM += 1
            #print line
    f.close()
    
    #print "totalSAM=",(totalSAM/float(CH3len2)),"totalOAM=",totalOAM,"totalSOL=",totalSOL
    #print "totalSAM=",(totalSAM/float(CH3len)),"totalOAM=",(totalOAM/float(OHlen))
    if i==0:
        totalSAM = int(totalSAM/CH3len)
        totalOAM = int(totalOAM/OHlen)
    elif i!=0:
        totalSAM = int(totalSAM/CH3len2)
        totalOAM = int(totalOAM/OHlen2)
    totalSOL = int(totalSOL/3)    
    print "totalSAM=",totalSAM,"totalOAM=",totalOAM,"totalSAM+totalOAM=",totalSAM+totalOAM,"totalSOL=",totalSOL

    with open(newtop, 'w') as f1:  ##### TEST!!!!
        with open(benchfile, 'r') as g:
            l = 0
            k = 0
            m = 0
            for line in g: 
                if l < firstline-1:
                    if l == 3:
                        f1.write(line)
                        f1.write('#include "OH.itp"\n')
                    #if l == 6:
                        #f1.write("Linea 6")
                    else:
                        f1.write(line)                    
                #else:
                    #f1.write("SAM	"+str(totalSAM+totalOAM)+"\n")
                    #f1.write("OAM	"+str(totalOAM+"\n")
                l = l + 1
        
        f1.write("SAM        "+str(totalSAM+totalOAM)+"\n")
        #f1.write("SAM        "+str(totalSAM)+"\n")
        #f1.write("OAM        "+str(totalOAM)+"\n")
        f1.write("SOL        "+str(totalSOL)+"\n")
        
        print "just created ", newtop
        print "lastcount:",lastcountsam,lastcountoam,totalSOL
        print "just created ", newtop
    if i==0:
        os.system("sed -i -e 's/%s/%s/g' %s" %("CH3.itp",CH3itp,newtop ))
    elif i==21 or i==25 or i==50:
        os.system("sed -i -e 's/%s/%s/g' %s" %("CH3.itp",newCH3itp2,newtop ))
        os.system("sed -i -e 's/%s/%s/g' %s" %("OH.itp",newOHitp,newtop ))
    else:
        os.system("sed -i -e 's/%s/%s/g' %s" %("CH3.itp",newCH3itp,newtop ))
        #os.system("sed -i -e 's/%s/%s/g' %s" %("OH.itp",OHitp,newtop ))
            
    #os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(startsamfile, samfile ))
    #This last line would make the .top file include ALSO T1_new.itp
    #os.system("sed -i -e 's/%s/%s/g' %s")% ("#include \"T1.itp\"","#include \"T1.itp\"\n#include \"T1_new.itp\"".itp,newtop, ))

os.system("rm *.top-e")

## --> THIS CELL is only for water drops WITHOUT sams!!!
# THIS CELL WRITES ONLY THE TOTAL NUMBERS OF ATOMS IN THE TOP FILES
 ##### The names of the water ".gro files" must be changed also in placedrop-ptensor.ipynb from water5.gro to water5_ptensor.gro
#### first copy bench top file to the working folder!!! ####

benchfile='water.top' 
firstline=21 #first line NOT to copy (use the real line number, it will recalculated)

samsfolder = "/Users/burbol/Downloads/small_sams2" #path to .gro files

pc = [0,5,11, 17, 21,25,33,50, 66]
#pc = [66]

# From here everything runs automatically...

os.chdir(samsfolder)
for i in pc:
    systfile='water'+str(i)+'_ptensor.gro' #name of .gro files
    systfileold='water'+str(i)+'pc_ptensor.gro' #name of .gro files  ##### THIS 2 LINES WERE ADDED ONLY TO CHANGE THE NAMES OF THE WATER DROPLETS!!
                                                           ##### The names must be changed also in placedrop-ptensor.ipynb 
    os.system("mv %s %s" %(systfileold,systfile, )) #### comment them one the names have changed
    newtop= 'water'+str(i)+'_ptensor.top' #name of new .top file
    
    # we create the new file by openning and closing it
    #creating = open(newtop, 'w+')
    #creating.close()
    
    f = open(systfile)
    totalSOL = 0
    for line in f:
        if "SOL" in line:
            totalSOL += 1
    f.close()

    totalSOL = int(totalSOL/3) 
    
    with open(newtop, 'w') as f1:  ##### TEST!!!!
        with open(benchfile, 'r') as g:
            l = 0
            for line in g: 
                if l < firstline-1:
                    f1.write(line)
                    #print(line)
                    l = l + 1
            f1.write("SOL        "+str(totalSOL)+"\n")
            print("SOL        "+str(totalSOL)+"\n")
        
        print "just created ", newtop

os.system("rm *.top-e")

# This cells probably needs some re-writing
os.system("mkdir reshapingfiles")
os.system("cp *_c.gro reshapingfiles/")
os.system("rm *_c.gro")
os.system("rm *.top-e")
#print "lastcount:",lastcountsam,lastcountoam,totalSOL

# THIS CELL DELETS THE FILES THAT HAD A WRONG NAME
for i in pc:
    wrongtopname='water'+str(i)+'pc_ptensor.top' #name of new .top file
    os.system("rm %s" %(wrongtopname, )) #### comment them one the names have changed


