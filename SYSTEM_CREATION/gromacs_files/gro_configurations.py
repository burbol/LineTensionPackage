# Configuration of upper interface of SAMs with different OH- headgroups percentages
# (polarities). The surface is configured as a grid 

########################### SET ALL PARTICLE TYPES TO 'C' ###############################

pType = np.zeros([Nx,Ny],dtype=str) # particle type

# set standard particle type as Carbon
for i in range(Nx):
  for j in range(Ny):
    pType[i,j] = 'C' 
    
########################### CHOOSE NUMBER OF PARTICLES ###################################
   
carbons = 100
Nx=10
Ny=10

########################### EXCHANGE CARBONS WITH OXYGENS ##############################

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