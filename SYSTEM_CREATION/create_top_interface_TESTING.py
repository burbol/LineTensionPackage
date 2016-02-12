# Testing configuration of upper interface of SAMs with different OH- headgroups percentages
# (polarities). The surface is configured as a grid of atoms (C and O)
 
 
 

import numpy as np
import math
import matplotlib.pyplot as plt
import sys
 
 
 

xcopies = 1
ycopies = 1

Nx = 10 # number of gridpoints in x-direction (carbons)
Ny = 10 # number of gridpoints in y-direction (carbons)

Nx = Nx*xcopies # number of gridpoints in x-direction (carbons)
Ny = Ny*ycopies # number of gridpoints in y-direction (carbons)

a0 = 5.0 #

xinterval = 2
yinterval = 2
 
 
 

########################### SET ALL PARTICLE TYPES TO 'C' ###############################

pType = np.zeros([Nx,Ny],dtype=str) # particle type

# set standard particle type as Carbon
for i in range(Nx):
  for j in range(Ny):
    pType[i,j] = 'C' 
 
 
 

########################### EXCHANGE CARBONS WITH OXYGENS #############################
 
 
 

########################### TYPE 1 OF LOOP #############################################
       
pc = 21
xinterval = 2
yinterval = 1
    
        
pc=  28
xinterval = 2
yinterval = 2


n = 0
for k in range(0,Nx,yinterval*2):
    for l in range(0,Ny,xinterval*2):
        pType[k,l] = 'O' 
        n = n+1
for k in range(yinterval,Nx,xinterval*2):
    for l in range(xinterval,Ny,xinterval*2):
        pType[k,l] = 'O' 
        n = n+1
 
 
 

########################### TYPE 2 OF LOOP #############################################
        
pc = 20
xinterval = 3
yinterval = 3
        
pc = 25
xinterval = 3
yinterval = 2


n = 0
for l in range(0,Ny,yinterval):
    for k in range(0,Nx,xinterval-1):
        pType[k,l] = 'O' 
        n = n+1           
           
 
 
 

########################### TYPE 3 OF LOOP (NEW) #######################################

pc = 25
xinterval = 3
yinterval = 2


n = 0
for l in range(0,Ny,yinterval):
    for k in range(0,Nx,xinterval):
        pType[k,l] = 'O' 
        n = n+1
 
 
 

########################### CREATE GRID USING BASIS VECTORS Vx, Vy, Wx, Wy ###########################
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
        xPos[i,j] = i*Vx + j*Wx +12.68
        yPos[i,j] = i*Vy + j*Wy 
for j in range(Ny):
    for i in range(Nx):  # Here we move the last particles of almost each line to get a more rectangular surface shape
        if xPos[i,j]>xPos[-1,1]:
           xPos[i,j] = xPos[i-Nx+1,j-2]
 
 
 

########################### TYPE 2 OF GRID #############################################

counter = 0
# set particle positions
for j in range(Ny):
    x_shift = j - counter
    for i in range(Nx):
        xPos[i,j] = i*Vx + j*Wx - x_shift*Vx
        yPos[i,j] = i*Vy + j*Wy
        n = n + 1
    if (j%2):
        counter = counter + 1
 
 
 

################################## PLOT GRID  ######################################
SizeOfDots = 8
fig, ax = plt.subplots()
for i in range(Nx):
  for j in range(Ny):
    if pType[i,j] == 'O':
      ax.plot([xPos[i,j]],[yPos[i,j]],marker='o',markersize=SizeOfDots,color='blue')
    else:
      ax.plot([xPos[i,j]],[yPos[i,j]],marker='o',markersize=SizeOfDots,color='green')
text = ', Grid '+ str(Nx)+'x'+str(Ny)    
plt.title("Percentage = " + str(int(pc*100))+text, fontsize= 14)
plt.grid()
plt.show()
#fig.savefig('output_' + str(Percentage) + '_positions.pdf',format='pdf')
 
 
 


 
 
 

