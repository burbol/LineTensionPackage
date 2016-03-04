#!/usr/bin/python
# This script assumes the Package pdbfile_v2.py is in the same folder
# Functions for writing particle coordinates along the SAM chains AND for producing the .pdb file

import numpy as np

################# Basis Vectors  ##################

# Lattice vector
a0 = 5.0

# First basis vector V = (Vx,Vy)
Vx = a0
Vy = 0

# Second basis vector W = (Wx,Wy)
Wx = a0*np.sin(np.pi/6)
Wy = a0*np.cos(np.pi/6)


################# Head Groups  ##################

####  OAM Head Groups  TOP ####

xLengthCO = 0.22
yLengthCO = 0.00
zLengthCO = -1.42

xLengthOH = +0.87
yLengthOH = 0.00
zLengthOH = +0.39

############## SAM & OAM CHAINS ##############
xLengthCCa = -1.40
yLengthCCa = 0.00
zLengthCCa = -0.64

xLengthCCb = +0.15
yLengthCCb = 0.00
zLengthCCb = -1.53


""" Not needed anymore

####  SAMs Head Groups  TOP ####

xLengthCHTOP = -0.90
yLengthCHTOP = 0.00
zLengthCHTOP = +0.41

####  Head Groups  BOTTOM  (a) ####

xLengthCHBOTTOM = 0.10
yLengthCHBOTTOM = 0.00
zLengthCHBOTTOM = -0.99


xLengthCH1a = -0.50
yLengthCH1a = +0.81
zLengthCH1a = +0.29

xLengthCH2a = -0.50
yLengthCH2a = -0.810
zLengthCH2a = +0.29

xLengthCH1b = +0.50
yLengthCH1b = +0.81
zLengthCH1b = -0.29

xLengthCH2b = +0.50
yLengthCH2b = -0.810
zLengthCH2b = -0.29
"""

########################### FUNCTION TO CREATE GRID ###########################
def creategrid(a0, Nx, Ny):
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

    ########################### TYPE 1 OF GRID #############################################

    for j in range(Ny):
        for i in range(Nx):
            xPos[i,j] = i*Vx + j*Wx
            yPos[i,j] = i*Vy + j*Wy

    #for j in range(1,Ny):
        #for i in range(Nx):  # Here we move the last particles of almost each line to get a more rectangular surface shape
            #if xPos[i,j]>xPos[-1,1]:
                #xPos[i,j] = xPos[i-Nx+1,j-2]

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
    ####### OXYGEN ######
    xnew,ynew,znew,totalpos,indexO = writeO(openfile,xLengthCO,yLengthCO,zLengthCO,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexO)
    ####### H1 ######
    totalpos,indexH = writeH(openfile,xLengthOH,yLengthOH,zLengthOH,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)

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

def writepdb(pType,xPos,yPos,zlast,pc,a0,Nx,Ny):
	#############################################  PDB FILE WRITTING    ###################################################
	# Set box size
	Wx = a0*np.sin(np.pi/6)
	Wy = a0*np.cos(np.pi/6)
	xPos, yPos = creategrid(a0, Nx, Ny)
	xbox = round(xPos.max() - xPos.min()+ Wx,3)
	ybox = round(yPos.max() - yPos.min()+ Wy,3)
	#zbox = round(zPos,3)-zlastPos.min() #zlastPos doesn't get a value until the end of this cell => run 2 times!
	#zlastPos = zlast*np.ones([Nx,Ny],dtype=float) # zlastPos ONLY will serve to calculate the box height (z)
	zbox = zlast + 2.0

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
			zoldC= zlast
			atomtype = pType[i,j]
			indexC = 1
			indexO = 1
			indexH = 1
			atomsbottom = 1 #number of atoms of molecule at the bottom
			atomschain = 1 #number of atoms of molecules inside the chain
			#OXYGEN CHAIN
			if atomtype == 'O':
				#chainlength = 63  # Old SAMs
				chainlength = 12
				atomshead = 2 #number of atoms of head group molecule at the top
				chaintype='OAM'
				xnew,ynew,znew,totalpos,indexO,indexH = pdb.writeOH(f,chaintype,chainNum,xoldC,yoldC,(zoldC-pdb.zLengthCO),totalpos,indexO,indexH)

			elif atomtype == 'C':    #CARBON CHAIN parameters
			#Third H atom (H3)
				#chainlength = 65 # Old SAMs
				chainlength = 11
				atomshead = 1 #number of atoms of head group molecule at the top
				chaintype = 'SAM'
				atomtype = 'CAL'
				xnew,ynew,znew,totalpos,indexC,indexH = pdb.writeCHTOP(f,atomtype,chaintype,chainNum,xoldC,yoldC,zoldC-pdb.zLengthCCb,totalpos,indexC,indexH)

			#here comes the "body" of the chain
   			chainloop = (chainlength-atomshead-atomsbottom-atomschain)/atomschain
			for d in range(chainloop/2):

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

				######### CHb #######
				xnew,ynew,znew,totalpos,indexC,indexH = pdb.writeCHb(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)

				######### CHa #######
				xnew,ynew,znew,totalpos,indexC,indexH = pdb.writeCHa(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)

			# At the end of each chain we also write one last CH2 + the (BOTTOM) Head Group
			######### CHb #######
			atomtype = 'CAD'
			xnew,ynew,znew,totalpos,indexC,indexH = pdb.writeCHb(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)

			######### CHBottom #######
			atomtype = 'CAC'
			xnew,ynew,znew,totalpos,indexC,indexH = pdb.writeCHBOTTOM(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)

	f.close()