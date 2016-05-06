
# coding: utf-8

# In[1]:

#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import os
import pylab as pl


# In[2]:

# Cell copied from ExtendSam.ipynb

pc=[21,25]
samsfolder = "/Users/burbol/MEGAsync/scripts/SAM_CREATION/ExtendSAMs"
# WE CHECK THE BOXSIZE OF THE NEW FILE TO ENTER THEM IN placedrop.ipynb
os.chdir(samsfolder)
for m in pc:
    newfile = '%sstart%d.gro'%('BIG',m, )   
    last_line = open(newfile, "r").readlines()[-1]
    Line_len = len(last_line)
    print newfile, ":", last_line


# In[4]:

######## CHECK FOLDER PATHS AND NAME OF gro FILE startsamfile--> look also for os.chdir!!!!!! #########
#folder with sams and water .gro files

#Put surfaces in ../samsfolder!! (now: drop_placement)
samsfolder = "/Users/burbol/MEGAsync/scripts/SAM_CREATION/SAMs/NEW/drop_placement/DropsGroTop" #path to .gro files

# folder where we will put the shifted sams: can be deleted if everything works fine
unwantedfolder = "/Users/burbol/MEGAsync/scripts/SAM_CREATION/SAMs/NEW/drop_placement/reshaping_files" #path unwanted files

# sam sizes in z-direction (not box size!!)
sam={}
#sam[21]=2.357  # small SAM
#sam[25]=2.357  # small SAM

sam[21]=2.310 # big SAM
sam[25]=2.368 # big SAM
sam[33]=2.312 
sam[50]=2.310

# water drop sizes in z-direction (they could also be read, look at script ExtendSam.ipynb)
water={}
water[216]=2.020
water[1000]=3.320
water[2000]=4.124
water[3000]=4.637
water[4000]=5.124
water[5000]=5.495
water[6500]=5.981 
water[7000]=6.126
water[8000]=6.395
water[9000]=6.665
water[10000]=6.895  

#sizes of simulation box of sams
xbox={}
ybox={}
zbox={}

#xbox[21]=10.0000 # small SAM
#ybox[21]=13.1913
#zbox[21]=12.0000

#xbox[25]=10.0000 # small SAM
#ybox[25]=13.1913
#zbox[25]=12.0000

#xbox[33]=13.500
#ybox[33]=13.856
#zbox[33]=12.000

xbox[21]=20.00000
ybox[21]=21.66500
zbox[21]=20.00000

xbox[25]=20.00000
ybox[25]=21.66500
zbox[25]=20.00000

xbox[33]=18.00000  
ybox[33]=17.33200 
zbox[33]=20.00000 

xbox[50]=20.00000
ybox[50]=21.66500
zbox[50]=20.00000

#pc = [33,50]
#molec = [216, 1000, 2000, 3000, 4000, 5000, 6500, 7000, 8000, 9000, 10000]
pc = [21,25]
#molec = [6500, 7000, 8000, 9000, 10000]
molec = [216, 1000, 2000, 3000, 4000, 5000]

# From here everything runs automatically...

os.system("mkdir %sdelete"% (str(unwantedfolder)+'/'))
os.chdir(samsfolder)

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def linecount(file_name):
    with open(file_name, 'r') as foo:
        x = len(foo.readlines())
        return x
    
for i in pc:   
    
    #sam file names
    #startsamfile='start'+str(i)+'.gro'
    startsamfile='%sstart%d.gro'%('BIG',i, )
    samfile='start'+str(i)+'_c.gro'
    
    #we copy the sams to the working folder
    os.system("cp ../%s ." %(startsamfile, ))
    #we move the sams down
    os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(startsamfile, samfile, ))
    os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -translate 0 0 %5.3f" %(samfile, samfile, sam[i]/(-2), ))
    
    for j in molec:        
        
        #water file names
        startwaterfile='NPT_water'+str(j)+'.gro'
        waterfile='NPT_water'+str(j)+'_c.gro'
        #new files names
        newsystfile='NPT_sam'+str(i)+'_water'+str(j)+'_c.gro'
        
        #we change the water box size to the same as the sams and we center every water system
        os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -box %5.3f %5.3f %5.3f" %(startwaterfile, waterfile, xbox[i], ybox[i], zbox[i], ))
        os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(waterfile, waterfile, ))
               
        #we move the drops up 
        os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -translate 0 0 %5.3f" %(waterfile, waterfile, 0.5+(water[j]/2), ))
        
##### WE START THE MERGING PROCESS OF water drops + sams #################

        # we create the new file by openning and closing it
        creating = open(newsystfile, 'w+')
        creating.close()
        
        #linecount
        linewater=linecount(waterfile)
        linesam=linecount(samfile)
        
        lastline = open(samfile, "r").readlines()[-1]
        with open(newsystfile, 'a') as f1:
            with open(samfile, 'r') as g:
                l = 0
                for line in g:
                    if l < linesam-1: 
                        f1.write(line)
                    l = l+1   
            with open(waterfile, 'r') as h:
                l = 0
                for line in h:                        
                    if l > 1 and l < linewater-1:
                        f1.write(line)
                    l = l + 1
            f1.write(lastline)

             
        #replace atom number
        atomssam = linesam-3
        atomswater = linewater-3
            
        replace_line(newsystfile, 1, str(atomssam+atomswater) + "\n")
        replace_line(newsystfile, 0, "sam "+str(i)+"% OH-coverage + water "+str(j)+ "\n")
        
        endfile='NPT_sam'+str(i)+'_water'+str(j)+'.gro'
        os.system("/usr/local/gromacs/bin/editconf -f %s -o %s" %(newsystfile, endfile, ))
        os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -translate %8.5f %8.5f %8.5f" %(endfile, endfile, 0, 0,-5, ))

# We delete/move not needed files
os.system("mkdir %sdelete"% (str(unwantedfolder)+'/'))
for i in pc:
    samfile='start'+str(i)+'_c.gro'
    os.system("mv %s  %s"%(samfile,unwantedfolder+'/delete/'+samfile, ))
    for j in molec: 
        waterfile='NPT_water'+str(j)+'_c.gro'
        os.system("mv %s  %s"% (waterfile,unwantedfolder+'/delete/'+waterfile, ))
        newsystfile='NPT_sam'+str(i)+'_water'+str(j)+'_c.gro'
        os.system("mv %s  %s"% (newsystfile,unwantedfolder+'/delete/'+newsystfile, ))
        os.system("rm \#*")


# In[6]:

print("mv %s > %s"%(samfile,unwantedfolder+'/'))


# In[9]:

os.system("mkdir %s"% (str(unwantedfolder)+'/'))
# We delete/move not needed files
os.system("mkdir %sdelete"% (str(unwantedfolder)+'/'))
for i in pc:
    samfile='start'+str(i)+'_c.gro'
    os.system("mv %s  %s"%(samfile,unwantedfolder+'/delete/'+samfile, ))
    for j in molec: 
        waterfile='NPT_water'+str(j)+'_c.gro'
        os.system("mv %s  %s"% (waterfile,unwantedfolder+'/delete/'+waterfile, ))
        newsystfile='NPT_sam'+str(i)+'_water'+str(j)+'_c.gro'
        os.system("mv %s  %s"% (newsystfile,unwantedfolder+'/delete/'+newsystfile, ))
        os.system("rm \#*")


# In[22]:

######### R E A D    T H I S!!!!!!! ##########
##Run topfile_creation.ipynb. There the files are moved. If not run this cell

#Renaming and moving endfiles

startfolder = "/Users/burbol/MEGAsync/scripts/SAM_CREATION/SAMs/NEW/drop_placement/DropsGroTop/"
endfolder="/Users/burbol/MEGAsync/scripts/SAM_CREATION/SAMs/NEW/drop_placement/NewVersion3/NewVersionBIG_Backup/"
for i in pc:
    for j in molec:
        startname='NPT_sam'+str(i)+'_water'+str(j)+'.gro'
        endname='sam'+str(i)+'_water'+str(j)+'.gro'
        os.system("mv %s  %s"% (startfolder+startname,endfolder+endname, ))
        #print("mv %s  %s"% (startfolder+startname,endfolder+endname, ))
        #print('\n')


# In[ ]:



