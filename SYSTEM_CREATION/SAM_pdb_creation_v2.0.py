# WARNING!!!! THIS CELL HAS TO RUN 2 TIMES TO GET THE CORRECT VALUES (see comment of zbox)
#!/usr/bin/python

#!/usr/bin/env python

import sys
import pdbfile_v2.0 as pdb

%cd /Users/burbol2/Desktop/
#############################################  PDB FILE WRITTING    ###################################################
# Set box size
xbox = round(xPos.max()-xPos.min()+(a0*0.5),3)
ybox = round(yPos.max()-yPos.min()+Wy,3)
zbox = round(zPos,3)-zlastPos.min() #zlastPos doesn't get a value until the end of this cell => run 2 times!

title = 'sam ' + str(int(pc*100)) + '% OH-coverage'
f = open('start' + str(int(pc*100)) + '.pdb','w')
# save the particle types and positions
f.write('TITLE     ' + title + '\n')
f.write('REMARK    THIS IS A SIMULATION BOX' + '\n')
f.write("CRYST1  %3.3f  %3.3f  %3.3f  90.00  90.00  90.00 P 1           1"%(xbox,ybox,zbox) + '\n')
f.write('MODEL        1' + '\n')


# We start all the counters
chainlength = 12 # CHECK!!!!
totalpos=1
chainNum = 0
#indexH = 1
#indexC = 1
#indexO = 1


# First we write the top Head Group
for i in range(Nx):
  for j in range(Ny):   
        chainNum = chainNum +1
        xoldC= round(xPos[i,j],3)
        yoldC= round(yPos[i,j],3)
        zoldC= zPos
        atomtype = pType[i,j]
        indexC = 1
        indexO = 1        
        indexH = 1
        if atomtype == 'O':    #OXYGEN CHAIN
            #chainlength = 63
            chainlength = 12
            chaintype='OAM'
            xnew,ynew,znew,totalpos,indexO,indexH = pdb.writeOH(f,chaintype,chainNum,xoldC,yoldC,(zoldC-pdb.zLengthCO),totalpos,indexO,indexH)
            
        elif atomtype == 'C':    #CARBON CHAIN parameters
        #Third H atom (H3)
            #chainlength = 65
            chainlength = 11
            chaintype = 'SAM'
            atomtype = 'CAL'
            xnew,ynew,znew,totalpos,indexC,indexH = pdb.writeCHTOP(f,atomtype,chaintype,chainNum,xoldC,yoldC,zoldC-pdb.zLengthCCb,totalpos,indexC,indexH)
            
        #here comes the "body" of the chain
        for d in range(4):
            
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

        # At the end of each chain we also write a last CH2 + the Head Group (BOTTOM)
        ######### CHb #######
        atomtype = 'CAD'
        xnew,ynew,znew,totalpos,indexC,indexH = pdb.writeCHb(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)
        
        ######### CHBottom #######
        atomtype = 'CAC'
        xnew,ynew,znew,totalpos,indexC,indexH = pdb.writeCHBOTTOM(f,atomtype,chaintype,chainNum,xnew,ynew,znew,totalpos,indexC,indexH)
        
f.close()