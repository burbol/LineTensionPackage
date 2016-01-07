# We define the functions needed to write the particle positions along the chains

################# Basis Vectors  ##################

#V = (Vx,Vy) first basis vector 
Vx = a0
Vy = 0

# W = (Wx,Wy) second basis vector 
Wx = a0*np.sin(np.pi/6)
Wy = a0*np.cos(np.pi/6)


################# Head Groups  ##################


####  SAMs Head Groups  TOP ####

xLengthCHTOP = -0.90
yLengthCHTOP = 0.00
zLengthCHTOP = +0.41

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

xLengthCH1a = -0.50
yLengthCH1a = +0.81
zLengthCH1a = +0.29

xLengthCH2a = -0.50
yLengthCH2a = -0.810
zLengthCH2a = +0.29

xLengthCCb = +0.15
yLengthCCb = 0.00
zLengthCCb = -1.53

xLengthCH1b = +0.50
yLengthCH1b = +0.81
zLengthCH1b = -0.29

xLengthCH2b = +0.50
yLengthCH2b = -0.810
zLengthCH2b = -0.29

####  Head Groups  BOTTOM  (a) ####

xLengthCHBOTTOM = 0.10
yLengthCHBOTTOM = 0.00
zLengthCHBOTTOM = -0.99


################# Functions  ##################


################# Write atoms  ##################


def writeC(xLength,yLength,zLength,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC):
    atomtype = 'C'
    atomnum=str(atomtype)+str(indexC)
    printline(totalpos, atomnum, chaintype, chainNum,xoldC,yoldC,zoldC) # C
    xnew = xoldC + xLength
    ynew = yoldC + yLength
    znew = zoldC + zLength
    totalpos = totalpos + 1
    indexC = indexC + 1
    return xnew,ynew,znew,totalpos,indexC
    
def writeH(xLength,yLength,zLength,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH):
    atomtype = 'H'
    atomnum=str(atomtype)+str(indexH)
    xnew = xoldC + xLength
    ynew = yoldC + yLength
    znew = zoldC + zLength
    printline(totalpos, atomnum, chaintype, chainNum, xnew,ynew,znew) # H 
    totalpos = totalpos + 1
    indexH = indexH + 1
    return totalpos,indexH
    
def writeO(xLength,yLength,zLength,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexO): 
    atomtype = 'O'
    atomnum=str(atomtype)+str(indexO)
    printline(totalpos, atomnum, chaintype, chainNum, xoldC,yoldC,zoldC)  # O
    xnew = xoldC + xLength
    ynew = yoldC + yLength
    znew = zoldC + zLength
    totalpos = totalpos + 1
    indexC = indexO + 1
    return xnew,ynew,znew,totalpos,indexO
    
    
################# Write molecules  ##################

def writeOH(chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexO,indexH):
    ####### OXYGEN ######
    xnew,ynew,znew,totalpos,indexO = writeO(xLengthCO,yLengthCO,zLengthCO,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexO)
    ####### H1 ######
    totalpos,indexH = writeH(xLengthOH,yLengthOH,zLengthOH,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    
    return xnew,ynew,znew,totalpos,indexO,indexH
    
    
def writeCHTOP(chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC,indexH):
    
    ####### CARBON ######
    xnew,ynew,znew,totalpos,indexC = writeC(xLengthCCb,yLengthCCb,zLengthCCb,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC)
    ####### H1 ######
    totalpos,indexH = writeH(xLengthCH1b,yLengthCH1a,zLengthCH1a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H2 ######
    totalpos,indexH = writeH(xLengthCH2b,yLengthCH2a,zLengthCH2a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H3 ######
    totalpos,indexH = writeH(xLengthCHTOP,yLengthCHTOP,zLengthCHTOP,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
            
    return xnew,ynew,znew,totalpos,indexC,indexH
    

def writeCHa(chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC,indexH):
    
    ####### CARBON ######
    xnew,ynew,znew,totalpos,indexC = writeC(xLengthCCb,yLengthCCb,zLengthCCb,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC)
    ####### H1 ######
    totalpos,indexH = writeH(xLengthCH1a,yLengthCH1a,zLengthCH1a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    #Second H atom (H2)
    totalpos,indexH = writeH(xLengthCH2a,yLengthCH2a,zLengthCH2a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
            
    return xnew,ynew,znew,totalpos,indexC,indexH
   
        
def writeCHb(chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC,indexH):
    
    ####### CARBON ######
    xnew,ynew,znew,totalpos,indexC = writeC(xLengthCCa,yLengthCCa,zLengthCCa,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC)
    ####### H1 ######
    totalpos,indexH = writeH(xLengthCH1b,yLengthCH1b,zLengthCH1b,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H2 ######
    totalpos,indexH = writeH(xLengthCH2b,yLengthCH2b,zLengthCH2b,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
            
    return xnew,ynew,znew,totalpos,indexC,indexH


def writeCHBOTTOM(chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC,indexH):
    
    ####### CARBON ######
    xnew,ynew,znew,totalpos,indexC = writeC(xLengthCCb,yLengthCCb,zLengthCCb,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexC)
    ####### H1 ######
    totalpos,indexH = writeH(xLengthCH1a,yLengthCH1a,zLengthCH1a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H2 ######
    totalpos,indexH = writeH(xLengthCH2a,yLengthCH2a,zLengthCH2a,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
    ####### H3 ######
    totalpos,indexH = writeH(xLengthCHBOTTOM,yLengthCHBOTTOM,zLengthCHBOTTOM,chaintype,chainNum,xoldC,yoldC,zoldC,totalpos,indexH)
                        
    return xnew,ynew,znew,totalpos,indexC,indexH

