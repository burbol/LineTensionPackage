#!/usr/bin/python
# This script assumes the Package pdbfile_v2.py is in the same folder
# Functions for writing particle coordinates along the SAM chains AND for producing the .pdb file

import numpy as np

################# Basis Vectors  ##################

# Lattice vector
a0 = 5.0

#First basis vector V = (Vx,Vy)
Vx = a0
Vy = 0

#Second basis vector W = (Wx,Wy)
#Wx = a0*np.sin(np.pi/6)
#Wy = a0*np.cos(np.pi/6)

Wx = a0*np.sin(2*np.pi/3)
Wy = a0*np.cos(2*np.pi/3)


################# Num of atoms in each chain ##################

chainlengthCH3 = 11
chainlengthOH = 12

#chainlengthCH3 = 65 # Old SAMs
#chainlengthOH = 63  # Old SAMs

atomsheadCH3 = 1 #number of atoms of head group molecule at the top
atomsheadOH = 2 #number of atoms of head group molecule at the top

atomsbottom = 1 #number of atoms of molecule at the bottom
atomschain = 1 #number of atoms of each molecule inside the chain

################# Names of different chains ##################

chaintypeOH='XOH'
chaintypeCH3 = 'SAM'

################# Names of different atoms/molecules ##################
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
	return atomtype

################# Bond length: Head Groups  ##################

""" New bond lengths """
####  OH Head Groups  TOP ####

xLengthOH = -0.54
yLengthOH = -0.42
zLengthOH = 0.73

xLengthCO = -0.88
yLengthCO = 0.57
zLengthCO = -0.98

############## OH & CH3 CHAINS ##############
xLengthCCa = 0.89
yLengthCCa = 0.63
zLengthCCa = -1.09

xLengthCCb = -0.86
yLengthCCb = 0.64
zLengthCCb = -1.1

""" Old bond lengths 
####  OH Head Groups  TOP ####

xLengthOH = +0.87
yLengthOH = 0.00
zLengthOH = +0.39

xLengthCO = 0.22
yLengthCO = 0.00
zLengthCO = -1.42

############## OH & CH3 CHAINS ##############
xLengthCCa = -1.40
yLengthCCa = 0.00
zLengthCCa = -0.64

xLengthCCb = +0.15
yLengthCCb = 0.00
zLengthCCb = -1.53
"""

########################### FUNCTION SET ALL PARTICLE TYPES TO 'C' ###############################

def C_restart(Nx,Ny):
    pType = np.zeros([Nx,Ny],dtype=str) # particle type

    # set standard particle type as Carbon
    for i in range(Nx):
        for j in range(Ny):
            pType[i,j] = 'C'
    return pType

########################### FUNCTION TO CREATE GRID ###########################
def creategrid(Nx, Ny):

    # First basis vector V = (Vx,Vy)
    Vx = a0
    Vy = 0
    # Second basis vector W = (Wx,Wy)
    Wx = a0*np.sin(np.pi/6)
    Wy = a0*np.cos(np.pi/6)

    # Create arrays that hold particle positions
    xPos = np.zeros([Nx,Ny],dtype=float) # x positions of particles
    yPos = np.zeros([Nx,Ny],dtype=float) # y positions of particles
    
    for j in range(Ny):
        for i in range(Nx):
            xPos[i,j] = i*Vx + j*Wx
            yPos[i,j] = i*Vy + j*Wy
            # Move last particles of (almost) each line to get rectangular grid shape
            if xPos[i,j]>((Nx-1)*Vx + Wx):
                xPos[i,j] = xPos[i,j] - (Nx*Vx)

    return xPos, yPos

################# .pdb file Functions  ##################

def printline(openfile,totalpos, atomnum, chaintype, chainNum, x, y, z):
    occupancy=1.00
    temp=0.00
    # save the particle types and positions
    openfile.write( "%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s"%("ATOM ", totalpos, atomnum, '',chaintype,'',chainNum,'', x, y, z, occupancy, temp,'','' + '\n'))

################# New Functions  ##################

""" OH head group """
def writeO(openfile,xLength,yLength,zLength,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexO):
    atomtype = 'OAA'
    #atomnum=str(atomtype)+str(indexO)
    atomnum=str(atomtype)
    printline(openfile,totalpos, atomnum, chaintype, chainNum, xoldC,yoldC,zoldC)  # O
    xnew = xoldC + xLength
    ynew = yoldC + yLength
    znew = zoldC + zLength
    totalpos = totalpos + 1
    #indexC = indexO + 1 # Not used because there is only one O in the chain (modify script and delete!)
    return xnew,ynew,znew,totalpos,indexO

def writeH(openfile,xLength,yLength,zLength,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH):
    atomtype = 'HAA'
    #atomnum=str(atomtype)+str(indexH)
    atomnum=str(atomtype)
    xnew = xoldC + xLength
    ynew = yoldC + yLength
    znew = zoldC + zLength
    printline(openfile,totalpos, atomnum, chaintype, chainNum, xnew,ynew,znew) # H
    totalpos = totalpos + 1
    indexH = indexH + 1
    return totalpos,indexH

def writeOH(openfile,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexO,indexH):
    ####### H1 ######
    totalpos,indexH = writeH(openfile,xLengthOH,yLengthOH,zLengthOH,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### OXYGEN ######
    xnew,ynew,znew,totalpos,indexO = writeO(openfile,xLengthCO,yLengthCO,zLengthCO,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexO)

    return xnew,ynew,znew,totalpos,indexO,indexH

""" For CH2 and CH3"""
# Argument "atomtype" needed because each atom has a different name
def writeC(atomtype,openfile,xLength,yLength,zLength,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC):
    #atomtype = 'CHA'
    #atomnum=str(atomtype)+str(indexC)
    atomnum=str(atomtype)
    printline(openfile,totalpos, atomnum, chaintype, chainNum,xoldC,yoldC,zoldC) # C
    xnew = xoldC + xLength
    ynew = yoldC + yLength
    znew = zoldC + zLength
    totalpos = totalpos + 1
    indexC = indexC + 1
    return xnew,ynew,znew,totalpos,indexC


def writeCHa(openfile,atomtype,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC,indexH):

    ####### CARBON ######
    xnew,ynew,znew,totalpos,indexC = writeC(atomtype,openfile,xLengthCCb,yLengthCCb,zLengthCCb,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC)
    """ Not needed anymore
    ####### H1 ######
    totalpos,indexH = writeH(xLengthCH1a,yLengthCH1a,zLengthCH1a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    #Second H atom (H2)
    totalpos,indexH = writeH(xLengthCH2a,yLengthCH2a,zLengthCH2a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    """
    return xnew,ynew,znew,totalpos,indexC,indexH


def writeCHb(openfile,atomtype,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC,indexH):

    ####### CARBON ######
    xnew,ynew,znew,totalpos,indexC = writeC(atomtype,openfile,xLengthCCa,yLengthCCa,zLengthCCa,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC)
    """ Not needed anymore
    ####### H1 ######
    totalpos,indexH = writeH(xLengthCH1b,yLengthCH1b,zLengthCH1b,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H2 ######
    totalpos,indexH = writeH(xLengthCH2b,yLengthCH2b,zLengthCH2b,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    """
    return xnew,ynew,znew,totalpos,indexC,indexH

def writeCHTOP(openfile,atomtype,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC,indexH):

    ####### CARBON ######
    xnew,ynew,znew,totalpos,indexC = writeC(atomtype,openfile,xLengthCCb,yLengthCCb,zLengthCCb,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC)
    """ Not needed anymore
    ####### H1 ######
    totalpos,indexH = writeH(xLengthCH1b,yLengthCH1a,zLengthCH1a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H2 ######
    totalpos,indexH = writeH(xLengthCH2b,yLengthCH2a,zLengthCH2a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H3 ######
    totalpos,indexH = writeH(xLengthCHTOP,yLengthCHTOP,zLengthCHTOP,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    """
    return xnew,ynew,znew,totalpos,indexC,indexH

def writeCHBOTTOM(openfile,atomtype,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC,indexH):

    ####### CARBON ######
    xnew,ynew,znew,totalpos,indexC = writeC(atomtype,openfile,xLengthCCb,yLengthCCb,zLengthCCb,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC)
    """ Not needed anymore
    ####### H1 ######
    totalpos,indexH = writeH(xLengthCH1a,yLengthCH1a,zLengthCH1a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H2 ######
    totalpos,indexH = writeH(xLengthCH2a,yLengthCH2a,zLengthCH2a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H3 ######
    totalpos,indexH = writeH(xLengthCHBOTTOM,yLengthCHBOTTOM,zLengthCHBOTTOM,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    """
    return xnew,ynew,znew,totalpos,indexC,indexH

#############################################  PDB FILE WRITTING    ###################################################
def writepdb(pType,xPos,yPos,pc,Nx,Ny):
	
	Wx = a0*np.sin(np.pi/6)
	Wy = a0*np.cos(np.pi/6)
	xPos, yPos = creategrid(Nx, Ny)
	
	# Set box size 
	"""(In order for the protein to avoid seeing its image across the periodic boundary, 
	it must be at least twice the cut-off distance from the next nearest image of itself.)"""
	xbox = round(xPos.max() - xPos.min()+ Wx,3)
	ybox = round(yPos.max() - yPos.min()+ Wy,3)
	#zbox = round(zPos,3)-zlastPos.min() #zlastPos doesn't get a value until the end of this cell => run 2 times!
	#zlastPos = zlast*np.ones([Nx,Ny],dtype=float) # zlastPos ONLY will serve to calculate the box height (z)
	#zbox = zlast

	zbox = abs(zLengthCO) + (float(chainlengthOH)/2.)*(abs(zLengthCCa) + abs(zLengthCCb)) + abs(zLengthCCb) # Now zlast isn't used anymore!

	title = 'sam ' + str(int(pc*100)) + '% OH-coverage'
	f = open('start' + str(int(pc*100)) + '.pdb','w')
	# save the particle types and positions
	f.write('TITLE     ' + title + '\n')
	f.write('REMARK    THIS IS A SIMULATION BOX' + '\n')
	f.write("CRYST1  %3.3f  %3.3f  %3.3f  90.00  90.00  90.00 P 1           1"%(xbox,ybox,zbox) + '\n')
	f.write('MODEL        1' + '\n')


	# We start all the counters
	totalpos=1
	chainNum = 0

	# First we write the top Head Group
	for i in range(Nx):
	  for j in range(Ny):
			chainNum = chainNum +1
			xoldC= round(xPos[i,j],3)
			yoldC= round(yPos[i,j],3)
			zoldC= zbox
			atomtype = pType[i,j]
			indexC = 1
			indexO = 1
			indexH = 1

			#OXYGEN CHAIN
			if atomtype == 'O':
				#chaintype='OAM'  # Old SAMs
				chainlength = chainlengthOH
				atomshead = atomsheadOH
				chaintype = chaintypeOH
				xnew,ynew,znew,totalpos,indexO,indexH = writeOH(f,chaintype,chainNum,xoldC,yoldC,(zoldC-zLengthCO),totalpos,indexO,indexH)

			#CARBON CHAIN
			elif atomtype == 'C':
			#Third H atom (H3)
				chainlength = chainlengthCH3
				atomshead = atomsheadCH3
				chaintype = chaintypeCH3
				atomtype = namecarbons(indexC)
				xnew,ynew,znew,totalpos,indexC,indexH = writeCHTOP(f,atomtype,chaintype,chainNum,xoldC,yoldC,zoldC-zLengthCCb,totalpos,indexC,indexH)

			#here comes the "body" of the chain
   			chainloop = (chainlength-atomshead-atomsbottom-atomschain)/atomschain
			for d in range(chainloop/2):

				######### CHb #######
				atomtype = namecarbons(indexC)
				xnew,ynew,znew,totalpos,indexC,indexH = writeCHb(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)

				######### CHa #######
				atomtype = namecarbons(indexC)
				xnew,ynew,znew,totalpos,indexC,indexH = writeCHa(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)

			# At the end of each chain we also write one last CH2 + the (BOTTOM) Head Group
			######### CHb #######
			atomtype = namecarbons(indexC)
			xnew,ynew,znew,totalpos,indexC,indexH = writeCHb(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)

			######### CHBottom #######
			atomtype = namecarbons(indexC)
			xnew,ynew,znew,totalpos,indexC,indexH = writeCHBOTTOM(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)

	f.close()