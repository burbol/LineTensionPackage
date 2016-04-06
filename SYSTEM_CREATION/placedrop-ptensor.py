
# coding: utf-8

# In[1]:

#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import os
import pylab as pl


# In[7]:

######## CHECK FOLDER PATHS AND NAME OF gro FILE startsamfile--> look also for os.chdir!!!!!! #########
#folder with sams and water .gro files
samsfolder = "/Users/burbol/Downloads/small_sams2/WaterSamSeparated/RESULTS" #path to .gro files
# folder where we will put the shifted sams: can be deleted if everything works fine
unwantedfolder = "/Users/burbol/Downloads/small_sams2/delete" #path unwanted files

#pc = [5, 11, 17, 21, 25, 33, 50, 66]
pc = [25]

# sam sizes in z-direction
sam={}
sam[0]=2.216
sam[5]=2.312
sam[11]=2.312
sam[17]=2.312
sam[21]=2.310
sam[25]=2.312
sam[33]=2.312 
sam[50]=2.310
sam[66]=2.357

# water (box) drop size in z-direction (they could also be read, look at script ExtendSam.ipynb)
water={}
water[0]=4.035 
water[5]=4.044
water[11]=4.037
water[17]=4.042
water[21]=4.035
water[25]=4.344  #4.203
water[33]=4.030
water[50]=4.028
water[66]=4.039

#sizes of simulation box of sams
xbox={}
ybox={}
zbox={}

xbox[0]=5.000
ybox[0]=3.464
zbox[0]=sam[0]+water[0]+0.4

xbox[5]=5.000
ybox[5]=3.464
zbox[5]=sam[5]+water[5]+0.4

xbox[11]=4.500
ybox[11]=2.598
zbox[11]=sam[11]+water[11]+0.4

xbox[17]=4.500
ybox[17]=3.464
zbox[17]=sam[17]+water[17]+0.4

xbox[21]=5.000
ybox[21]=4.397
zbox[21]=sam[21]+water[21]+0.4

xbox[25]=4.500
ybox[25]=3.464
zbox[25]=sam[25]+water[25]+0.4

xbox[33]=4.500 
ybox[33]=3.464 
zbox[33]=sam[33]+water[33]+0.4 

xbox[50]=5.000
ybox[50]=4.397
zbox[50]=sam[50]+water[50]+0.4

xbox[66]=4.500
ybox[66]=3.464
zbox[66]=sam[66]+water[66]+0.4

# From here everything runs automatically...

os.system("mkdir %s"% (str(unwantedfolder)))
os.chdir(str(samsfolder))

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
    startsamfile='start'+str(i)+'.gro'
    samfile='start'+str(i)+'_c.gro'  
    
    #water file names 
    startwaterfile='NPT_water'+str(i)+'_ptensor.gro'
    waterfile='NPT_water'+str(i)+'_ptensor_c.gro'
    
    #new files names
    newsystfile='sam'+str(i)+'_water_ptensor_c.gro'
    endfile='sam'+str(i)+'_water_ptensor.gro'
    
    #we copy the sams to the working folder
    #os.system("cp ../%s ." %(startsamfile, ))
    #we move the sams down
    watercenter=(sam[i]+0.5*water[i])+0.4
    #watercenter=(sam[i]+0.5*water[i])
    samcenter=0.5*sam[i]
    #zsam=-0.5*sam[i]
    os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -box %5.3f %5.3f %5.3f -center %5.3f %5.3f %5.3f" %(startsamfile, samfile, xbox[i], ybox[i],zbox[i], 0.5*xbox[i],0.5*ybox[i],samcenter, ))
    #os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -translate 0 0 %5.3f" %(samfile, samfile, zsam, ))    
        
    #we change the water box size to the same as the sams and we center every water system
    os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -box %5.3f %5.3f %5.3f -center %5.3f %5.3f %5.3f" %(startwaterfile, waterfile, xbox[i], ybox[i], zbox[i],0.5*xbox[i],0.5*ybox[i],watercenter, ))
    #os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(waterfile, waterfile, ))
               
    #we move the drops up 
    #os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -translate 0 0 %5.3f" %(waterfile, waterfile, zwater, ))
        
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
    replace_line(newsystfile, 0, "small sam "+str(i)+"% OH-coverage + water slab "+str(i)+ "\n")
    
    os.system("/usr/local/gromacs/bin/editconf -f %s -o %s" %(newsystfile, endfile, ))
    #os.system("/usr/local/gromacs/bin/editconf -f %s -o %s -translate %5.3f %5.3f %5.3f" %(endfile, endfile,0, 0, -sam[i], ))
    print "finished",endfile


# In[79]:

######## CHECK FOLDER PATHS AND NAME OF gro FILE startsamfile--> look also for os.chdir!!!!!! #########
#folder with sams and water .gro files
samsfolder = "/Users/burbol/Downloads/small_sams2" #path to .gro files
# folder where we will put the shifted sams: can be deleted if everything works fine
unwantedfolder = "/Users/burbol/Downloads/small_sams2/delete" #path unwanted files

# sam sizes in z-direction
sam={}
sam[0]=2.216
sam[5]=2.312
sam[11]=2.312
sam[17]=2.312
sam[21]=2.310
sam[25]=2.312
sam[33]=2.312 
sam[50]=2.310
sam[66]=2.357

# water drop sizes in z-direction (they could also be read, look at script ExtendSam.ipynb)
water={}
water[0]=4.284
water[5]=4.188
water[11]=4.188
water[17]=4.188
water[21]=4.19
water[25]=4.188
water[33]=4.188
water[50]=4.19
water[66]=4.188

#sizes of simulation box of sams
xbox={}
ybox={}
zbox={}

xbox[0]=5.000
ybox[0]=3.464
zbox[0]=9.000

xbox[5]=5.000
ybox[5]=3.464
zbox[5]=9.000

xbox[11]=4.500
ybox[11]=2.598
zbox[11]=9.000

xbox[17]=4.500
ybox[17]=3.464
zbox[17]=9.000

xbox[21]=5.000
ybox[21]=4.397
zbox[21]=9.000

xbox[25]=4.500
ybox[25]=3.464
zbox[25]=9.000

xbox[33]=4.500 
ybox[33]=3.464 
zbox[33]=9.000 

xbox[50]=5.000
ybox[50]=4.397
zbox[50]=9.000

xbox[66]=4.500
ybox[66]=3.464
zbox[66]=9.000

#pc = [0, 5, 11, 17, 21, 25, 33,50, 66]
pc = [11]

# From here everything runs automatically...

print("mkdir %s"% (unwantedfolder))
print 'chdir(str(samsfolder))'

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
    startsamfile='start'+str(i)+'.gro'
    samfile='start'+str(i)+'_c.gro'  
    
    #water file names
    startwaterfile='water'+str(i)+'.gro'
    waterfile='water'+str(i)+'_c.gro'
    
    #new files names
    newsystfile='sam'+str(i)+'_water_ptensor_c.gro'
    endfile='sam'+str(i)+'_water_ptensor.gro'
    
    #we copy the sams to the working folder
    print("cp ../%s ." %(startsamfile, ))
    #we move the sams down
    zwater=0.5+(water[i]/2.0)
    zsam=sam[i]/(-2.0)
    print("/usr/local/gromacs/bin/editconf -f %s -o %s -box %5.3f %5.3f %5.3f" %(startsamfile, startsamfile, xbox[i], ybox[i], zbox[i], ))
    print("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(startsamfile, samfile, ))
    print("/usr/local/gromacs/bin/editconf -f %s -o %s -translate 0 0 %5.3f" %(samfile, samfile, zsam, ))    
        
    #we change the water box size to the same as the sams and we center every water system
    print("/usr/local/gromacs/bin/editconf -f %s -o %s -box %5.3f %5.3f %5.3f" %(startwaterfile, waterfile, xbox[i], ybox[i], zbox[i], ))
    print("/usr/local/gromacs/bin/editconf -f %s -o %s -c" %(waterfile, waterfile, ))
               
    #we move the drops up 
    print("/usr/local/gromacs/bin/editconf -f %s -o %s -translate 0 0 %5.3f" %(waterfile, waterfile, zwater, ))
        
##### WE START THE MERGING PROCESS OF water drops + sams #################

    # we create the new file by openning and closing it
    creating = open(newsystfile, 'w+')
    creating.close()
    
    #linecount
    linewater=linecount(waterfile)
    linesam=linecount(samfile)
    
    lastline = open(samfile, "r+").readlines()[-1]
    with open(newsystfile, 'a') as f1:
        with open(samfile, 'r+') as g:
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
    replace_line(newsystfile, 0, "small sam "+str(i)+"% OH-coverage + water slab "+str(i)+ "\n")
    
    print("/usr/local/gromacs/bin/editconf -f %s -o %s" %(newsystfile, endfile, ))
    print("/usr/local/gromacs/bin/editconf -f %s -o %s -translate %5.3f %5.3f %5.3f" %(endfile, endfile,0, 0, -sam[i], ))


# In[5]:

print("mv %s > %s"%(samfile,unwantedfolder+'/'))


# In[4]:

# WATER ONLY
# We delete/move not needed files
#os.system("mkdir %sdelete"% (str(unwantedfolder)+'/'))
pc = [0, 5, 11, 17, 21, 25, 33,50, 66]
os.chdir(str(samsfolder))
for i in pc:
    samfile='start'+str(i)+'_c.gro'
    os.system("mv %s  %s"%(samfile,unwantedfolder+'/'+samfile, ))
    waterfile='water'+str(i)+'_c.gro'
    os.system("mv %s  %s"% (waterfile,unwantedfolder+'/'+waterfile, ))
    newsystfile='sam'+str(i)+'_water_ptensor_c.gro'
    os.system("mv %s  %s"% (newsystfile,unwantedfolder+'/'+newsystfile, ))
    os.system("rm \#*")
# We delete/move not needed files
    print("mv %s  %s"%(samfile,unwantedfolder+'/'+samfile, ))
    print("mv %s  %s"%(waterfile,unwantedfolder+'/'+waterfile, ))
    print("mv %s  %s"%(newsystfile,unwantedfolder+'/'+newsystfile, ))
    print("rm \#*")
    print "finished",endfile


# In[ ]:



