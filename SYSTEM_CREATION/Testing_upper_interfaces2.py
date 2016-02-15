
# coding: utf-8

# In[1]:

# Testing configuration of upper interface of SAMs with different OH- headgroups percentages
# (polarities). The surface is configured as a grid of atoms (C and O)
import numpy as np
import math
import matplotlib.pyplot as plt
import sys
import os

get_ipython().magic(u'pylab inline')


# In[2]:

########################### SET PARAMETERS FOR THE SIZE ###############################
xcopies = 1
ycopies = 1

Nx = 10 # number of gridpoints in x-direction (carbons)
Ny = 10 # number of gridpoints in y-direction (carbons)

Nx = Nx*xcopies # number of gridpoints in x-direction (carbons)
Ny = Ny*ycopies # number of gridpoints in y-direction (carbons)

a0 = 5.0 #


# In[3]:


########################### FUNCTION SET ALL PARTICLE TYPES TO 'C' ###############################

def C_restart(Nx,Ny):
    pType = np.zeros([Nx,Ny],dtype=str) # particle type

    # set standard particle type as Carbon
    for i in range(Nx):
        for j in range(Ny):
            pType[i,j] = 'C'
    return pType


# In[15]:

########################### FUNCTION TO CREATE GRID ###########################
def creategrid(a0):
    # set particle x- and y- coordinates
    # !!!! later move to create_top_surface.ipynb !!!


    # First basis vector V = (Vx,Vy)
    Vx = a0
    Vy = 0
    # Second basis vector W = (Wx,Wy) 
    Wx = a0*np.sin(np.pi/6)
    Wy = a0*np.cos(np.pi/6)

    # create arrays that hold particle positions
    xPos = np.zeros([Nx,Ny],dtype=float) # x positions of particles
    yPos = np.zeros([Nx,Ny],dtype=float) # y positions of particles
    zlastPos = np.zeros([Nx,Ny],dtype=float) # zlastPos ONLY will serve to calculate the box height (z)
    
    ########################### TYPE 1 OF GRID #############################################

    for j in range(Ny):
        for i in range(Nx):
            xPos[i,j] = i*Vx + j*Wx
            yPos[i,j] = i*Vy + j*Wy 
            
    #for j in range(1,Ny):
        #for i in range(Nx):  # Here we move the last particles of almost each line to get a more rectangular surface shape
            #if xPos[i,j]>xPos[-1,1]:
                #xPos[i,j] = xPos[i-Nx+1,j-2]

    return xPos, yPos, zlastPos


# In[16]:

################################## FUNCTION TO PLOT HEAT MAP  ######################################
def plotheat(pType, pc):
    # HEATMAP
    #   create array with 0s where there is O
    #   and ones where there is C:
    Z = np.zeros([Nx,Ny],dtype=int)
    for i in range(Nx):
        for j in range(Ny):
            if pType[i,j] == 'C':
                Z[i,j] = 1
    
    # plot the heatmap
    fig, ax = plt.subplots()
    ax.imshow(Z, cmap=plt.cm.winter, interpolation='nearest')
    #fig.savefig('s_' + str(pc) + '_heatmap.pdf',format='pdf')
 


# In[22]:

################################## FUNCTION TO PLOT GRID  ######################################
def plotgrid(pType, a0, pc):
    
    xPos, yPos, zlastPos = creategrid(a0)
    
    SizeOfDots = 8
    fig, ax = plt.subplots()
    for i in range(Nx):
        for j in range(Ny):
            if pType[i,j] == 'O':
                ax.plot([xPos[i,j]],[yPos[i,j]],marker='o',markersize=SizeOfDots,color='blue')
            else:
                ax.plot([xPos[i,j]],[yPos[i,j]],marker='o',markersize=SizeOfDots,color='yellow')
    text = '%, Grid '+ str(Nx)+'x'+str(Ny)    
    plt.title("Percentage = " + str(int(pc*100))+text, fontsize= 14)
    plt.grid()
    plt.show()
    #fig.savefig('s_' + str(pc) + '_grid.pdf',format='pdf')
 


# In[7]:

def loop1(xinterval,yinterval, Nx, Ny):
    pType = C_restart(Nx,Ny)

    n_oxys = 0
    for k in range(0,Nx,yinterval*2):
        for l in range(0,Ny,xinterval*2):
            pType[k,l] = 'O' 
            n_oxys = n_oxys + 1
    for k in range(yinterval,Nx,xinterval*2):
        for l in range(xinterval,Ny,xinterval*2):
            pType[k,l] = 'O' 
            n_oxys = n_oxys + 1
    pc = float(n_oxys)/float(Nx*Ny)
    return pType, pc

def loop2(xinterval,yinterval, Nx, Ny):
    pType = C_restart(Nx,Ny)
    n_oxys = 0
    for l in range(0,Ny,yinterval):
        for k in range(0,Nx,xinterval-1):
            pType[k,l] = 'O' 
            n_oxys = n_oxys + 1
    pc = float(n_oxys)/float(Nx*Ny)
    return pType, pc

def loop3(xinterval,yinterval, Nx, Ny):
    pType = C_restart(Nx,Ny)
    n_oxys =0
    for l in range(0,Ny,yinterval):
        for k in range(0,Nx,xinterval):
            pType[k,l] = 'O' 
            n_oxys = n_oxys +1
    pc = float(n_oxys)/float(Nx*Ny)
    return pType, pc


# In[25]:


########################### EXCHANGE CARBONS WITH OXYGENS #############################


# In[23]:

#path = "/Users/eixeres/Desktop/loop1/"
path = "/Users/burbol2/Desktop/PlotsLoops/loop1/"
for xinterval in range(1,5):
    for yinterval in range(1,5):            
        pType, pc = loop1(xinterval,yinterval, Nx, Ny)
        plotgrid(pType, a0, pc)
        plotheat(pType, pc)


# In[25]:

#path = "/Users/eixeres/Desktop/loop2/"
path = "/Users/burbol2/Desktop/PlotsLoops/loop2/"
for xinterval in range(2,5):
    for yinterval in range(2,5):            
        pType, pc = loop2(xinterval,yinterval, Nx, Ny)
        plotgrid(pType, a0, pc)
        plotheat(pType, pc)


# In[24]:

#path = "/Users/eixeres/Desktop/loop3/"
path = "/Users/burbol2/Desktop/PlotsLoops/loop3/"
for xinterval in range(1,5):
    for yinterval in range(1,5):            
        pType, pc = loop3(xinterval,yinterval, Nx, Ny)
        plotgrid(pType, a0, pc)
        plotheat(pType, pc)


# In[29]:

########################### TYPE 1 OF LOOP #############################################

pc = 8 # Good!
xinterval = 3
yinterval = 3

pc = 14 #(not evenly distributed)
xinterval = 3
yinterval = 1

pc = 10 #(not evenly distributed)
xinterval = 3
yinterval = 2

pc = 21 # Old SAM distribution
xinterval = 2
yinterval = 1

pc = 35 #(not evenly distributed)
xinterval = 1
yinterval = 2

pc=  13 #Good!
xinterval = 2
yinterval = 2

pc = 50 # not evenly distributed!
xinterval = 1
yinterval = 1

pType = C_restart(Nx,Ny)
n_oxys = 0
for k in range(0,Nx,yinterval*2):
    for l in range(0,Ny,xinterval*2):
        pType[k,l] = 'O' 
        n_oxys = n_oxys + 1
for k in range(yinterval,Nx,xinterval*2):
    for l in range(xinterval,Ny,xinterval*2):
        pType[k,l] = 'O' 
        n_oxys = n_oxys + 1

plotgrid(pType, a0)


# In[9]:

plotheat(pType)


# In[14]:

########################### TYPE 2 OF LOOP #############################################
        
pc = 20 #Good!
xinterval = 3
yinterval = 3

pc = 25 #Good!
xinterval = 3
yinterval = 2

pc = 15 #atoms distributed in lines
xinterval = 3
yinterval = 4

pc = 12 #(not evenly distributed)
xinterval = 4
yinterval = 4

pc = 50 #not evenly distributed!
xinterval = 2
yinterval = 2

pc = 100
xinterval = 2
yinterval = 1

pc = 50 #not evenly distributed!
xinterval = 3
yinterval = 1

pc = 50 #not evenly distributed!
xinterval = 2
yinterval = 3

pType = C_restart(Nx,Ny)
n_oxys = 0
for l in range(0,Ny,yinterval):
    for k in range(0,Nx,xinterval-1):
        pType[k,l] = 'O' 
        n_oxys = n_oxys + 1

plotheat(pType)
 


# In[17]:

plotgrid(pType, a0)


# In[53]:

########################### TYPE 3 OF LOOP (NEW) #######################################

pc = 20 #Good!
xinterval = 2
yinterval = 3

pc = 25 # Good!
xinterval = 2
yinterval = 2

pc = 40 # not evenly distributed!
xinterval = 3
yinterval = 1

pc = 30 # not evenly distributed!
xinterval = 4
yinterval = 1

pc = 20 # not evenly distributed!
xinterval = 3
yinterval = 2

pc = 16 # not evenly distributed!
xinterval = 3
yinterval = 3

pc = 15 # not evenly distributed!
xinterval = 4
yinterval = 2


# exchange Carbons with oxygens
pType = C_restart(Nx,Ny)
n_oxys =0
for l in range(0,Ny,yinterval):
    for k in range(0,Nx,xinterval):
        pType[k,l] = 'O' 
        n_oxys = n_oxys +1

plotheat(pType)


# In[54]:

plotgrid(pType, a0)


# In[ ]:



