#!/usr/bin/python

'''
This Python script computes the contact angle between water 
droplets and SAMs simulated with GROMACS. The radius of the 
circular surface at the base of the droplets is also determined. 
The script is designed to loop through multiple input density 
profiles.

Input:
Files with format ".xvg" produced with "g_rad_density"

Output: 
        -- Two files with format ".txt" (contact angle and base 
        radius in two columns. One of them has a third column
        with the name of the input file. Each line corresponds
        to one input file).
        -- One file with format ".pdf" (with circle fit plots. Each 
        page corresponds to one input file).
        
        Dependencies: C_AnglesModule.py, gromacs wrapper, scipy
        
(g_rad_density is a modification of the GROMACS program g_densmap
created in the research group AG Netz at the FU Berlin. The
difference is that g_rad_density uses the same coordinates as 
the simulation files while g_densmaps sets the center at the com).

It uses the self-developed module C_AnglesModule.py
Also the module GromacsWrapper from:
Oliver Beckstein, http://github.com/orbeckst/GromacsWrapper
'''

import C_AnglesModule
import numpy as np
import os
import math
from matplotlib.backends.backend_pdf import PdfPages
import gromacs
gromacs.config.setup()
from gromacs.formats import XVG


# Define folder names: "parentfolder" is the parent folder of the
# density profiles folders, "peaksfolder" stores the .txt files with
# the interface positions, and "outputfolder" the output files

#parentfolder = "/net/data/eixeres/Version_v2/radial_densmaps/" #densmaps on server
parentfolder = "/Volumes/UNI/radial_densmaps_Version_v2/" #densmaps locally
peaksfolder = parentfolder #interface positions
outputfolder = parentfolder


# SYSTEMS TO ANALYZE

# Percentage of -OH coverage (polarity) of the SAMs 

#SAMs=[0]
SAMs=[11, 22, 33, 37, 44]
#Number of water molecules in the droplets

#Waters=[1000]
Waters=[1000, 2000, 3000, 4000, 5000, 6500, 7000, 8000, 9000, 10000]

# Length of longest interval analyzed. In the shorter simulations
# 'NaN' will be returned for each time step that does not exist

start_time = 0
end_time = 200
timestep = 0.5


# Simulation box length in the z-direction:

boxlength={0: 12.0, 11: 12.0, 22: 12.0, 33: 12.0, 37: 12.0, 44: 12.0}


# Select position of solid-liquid interface (z = 0).
# a) for Water Peak
# b) for GDS
# c) for SAM Peak
# d) for Middle Point
# e) for highest carbon in SAM

option= 'e'
if option == 'a':
    interface='WaterPeak'
elif option == 'b':
    interface='GDS'
elif option == 'c':
    interface='SAMPeaks'
elif option == 'd':
    interface='MiddlePoint'
elif option == 'e':
    interface='SAM_last_C_atom'
    

# File with interface positions:

file_pos_interface = peaksfolder + interface + '.txt'


# Systems that appear in file with interface positions:

SAMpeaks=[0, 11, 22, 33, 37, 44]
Waterpeaks=[1000, 2000, 3000, 4000, 5000, 6500, 7000, 8000, 9000, 10000]

            
# Store interface positions in array "interface_data"

interface_data= np.loadtxt(file_pos_interface, skiprows=1)


# Store interface position of each system in dictionary for easier
# access. The keys are the OH percentage (polarity) and number of
# molecules of the system. For example: interface_pos[(11, 1000)]

i = 0
interface_pos={}
for pc in SAMpeaks:
    for molecs in Waterpeaks:
        z = pc, molecs
        interface_pos[z] = interface_data[i]
        i = i + 1


os.chdir(parentfolder)


# Loop through files corresponding to SAMs with different 
# OH-coverage percentage 

for pc in SAMs:

    # Define names of output files: 
    
#     # Name for single file with all systems with same SAM percentage
#     txtoutput2 = outputfolder + 'Contact_Angles2_' + interface +'_s'+str(pc)+'.txt'
#     txtoutput = outputfolder + 'Contact_Angles_' + interface +'_s'+str(pc)+'.txt
#     plotsOutput = outputfolder + interface + 'Circle_plots_s'+str(pc)+'.txt'
    
    # Name for single system files
    txtoutput2 = outputfolder + 'Contact_Angles2_' + interface +'_s'+str(pc)+'.txt'
    txtoutput = outputfolder + 'Contact_Angles_' + interface +'_s'+str(pc)+'.txt'
    plotsOutput = outputfolder + interface + 'Circle_plots_s'+str(pc)+'.pdf'


    # Create (open) output files: 
    # "myfile" and "myfile2" are .txt files where the contact angle
    # and radius at every time step will be printed in two columns
    # (in each line).
    # "myfile" has an additional column with the name of the 
    # corresponding density file (one file for every time step) and
    # before each bloc of results the name of the system is printed.
    # "myfile2" separates the blocs of results with one empty line.
    # "plotsOutput" is a .pdf file with one plot per page. The plots 
    # show both the data points used in the fit and the resulting
    # fitted circle for each time step.
    
    
    with PdfPages(plotsOutput) as pp, open(txtoutput, 'w') as myfile, open(txtoutput2, 'w') as myfile2:
    #with open(txtoutput, 'w') as myfile, open(txtoutput2, 'w') as myfile2:
        #pp = PdfPages(plotsOutput)
        
        # Print titles for the 3 columns of data
        
        print >> myfile, '{0}  {1}  {2}'.format(
        'File', 'Contact Angle', 'Base Radius')
        print >> myfile2, '{0}  {1}'.format(
        'Contact Angle', 'Base Radius')
        
        
        # Loop through files corresponding to water droplets with
        # different number molecules
        for molecs in Waters:
        
            # Define name of folder where density profiles are stored
            # (using SAM's polarity and number of water molecules. For
            # example s25_w2000)
            densmaps_folder = parentfolder + 's'+str(pc) + '_w' + str(molecs)
                
            os.chdir(densmaps_folder)
            
            
            # Separate new bloc of results with empty line (in 
            # "myfile") or system name (in "myfile2")
            print >> myfile, '             '
            print >> myfile2, '{0}  {1} {2}'.format('#File:', pc, molecs)
            
            
            # If simulation folder doesn't exist print "NaN" for all 
            # time steps and jump to the next simulation 
            if not os.path.isdir(densmaps_folder):
                            
                for start in C_AnglesModule.frange(
                start_time, end_time, timestep):
                
                    print >> myfile, '{0}  {1}  {2}'.format(
                    filename,'NaN', 'NaN')
                    print >> myfile2, '{0}  {1}'.format('NaN', 'NaN')
                    
                continue
                print "ERROR 2: folder not found for s",pc," w",molecs
            
            # Start loop over all time steps
            
            for start in C_AnglesModule.frange(
            start_time, end_time, timestep):
                
                # Set input file name
                
                end = start + timestep
                filename = 'g_rad_dmap_%dpc_w%d_%sns_%sns.xvg'%(
                pc, molecs, str(start), str(end), )
                
            
                # If density file doesn't exist for this time step print 
                # "NaN" and jump to the next time step
                
                if not os.path.isfile(filename): 
                   print >> myfile, '{0}  {1}   {2}'.format(
                   filename, 'NaN', 'NaN')
                   print >> myfile2, '{0}   {1}'.format('NaN', 'NaN')
                   continue
                                  
                # Read density files and store in ndarray "myinput" (multidimensional 
                # array or matrix). The first element of "myinput" (first 
                # column of matrix) is stored in array "x" and corresponds
                # to the z-coordinates of the radial density profiles.
                # (x[i] is the z-coordinate of density profile myinput[i])
                
                xvg = XVG()   
                xvg.read(filename)
                myinput = xvg.array
                x = myinput[0] 
                
                # Store interface position in float "shift"
                shift = interface_pos[(pc, molecs)]
                
                # Store total number of slices in integer "slicestotal"
                slicestotal = len(myinput) - 1
                
                # Store height of slices in float "sliceheight"
                sliceheight = boxlength[pc]/ slicestotal
                        
                
                # Shift coordinate system in the z-direction to set
                # origin at interface position. Store new coordinates
                # in array "zcoord"
                
                zcoord = np.zeros(len(myinput)-1)
                       
                for i in range(1,len(myinput)): 
                    zcoord[i-1] = (sliceheight *(i-1))-shift
                print "first coordinates of zcoord", zcoord[0], zcoord[1], zcoord[2], zcoord[-1]
        
        
                # Store slice number i with zcoord[i] = 0.0 in integer
                # "zeroslice". (Needed to discard first 8 nm above 
                # the surface from fit)
                
                zeroslice = 0
                cnt = 0
                for slicepos in zcoord:
                    if slicepos >= 0.0: 
                       zeroslice = cnt
                       break
                    cnt = cnt + 1
                
                # Store parameters of sigmoidal fit in arrays "r0", "R", "d"
                
                r0, R, d = C_AnglesModule.sigmoidfit(myinput)
                
                
                # Store bulk density in float "bulk"
                
                bulk = C_AnglesModule.waterbulk(myinput, r0, R, d )
                
                
                # Store first estimate of last "good slice" for
                # circle fit in integer "slicemax"
                
                slicemax = 0
                for slice in range(slicestotal,0,-1):
                    
                    if C_AnglesModule.checkslice(
                    r0[slice], R[slice], d[slice], bulk):
                        
                        slicemax = slice
                        break
                    else:
                        continue
                print "first estimate of slicemax = ", slicemax
                print "zcoord[slicemax]= ", zcoord[slicemax]
                        
                        
                # Store first estimate of first "good slice" for
                # circle fit in integer "slicemin"
                
                slicemin = 0
                middleslice = int(0.75*slicestotal)
                
                for slice in range(0,middleslice):
                    
                    if C_AnglesModule.checkslice(
                    r0[slice], R[slice], d[slice], bulk):
                        slicemin = slice
                        break
                    else: 
                        continue
                print "first estimate of slicemin = ", slicemin
                print "zcoord[slicemin]= ", zcoord[slicemin]
                        
  
                # Shift "slicemin" if too close to surface.
                # 0.8nm above "zeroslice" (if needed).
                
#                 discard = 0.8 # use nm!
#                 slices_out =  int(discard/sliceheight)
#                 slicemin2 = zeroslice + 13
#                 
#                 if slicemin < slicemin2:
#                     slicemin = slicemin2

        
                #Leave slices below zero out (if needed).
                
                if slicemin < zeroslice :
                    slicemin = zeroslice 
                
                               
                if ((slicemin==None) and (slicemax==None)) or (slicemin >= slicemax - 1):
                    print >> myfile, '{0}  {1}  {2}'.format(
                    filename,'NaN', 'NaN')
                    print >> myfile2, '{0}  {1}'.format('NaN', 'NaN')
                    print "ERROR: no good slices found for s",pc," w",molecs," at ",start," ns"
                    continue
                
                # Boundaries for fit:
                
                slicemin, slicemax = C_AnglesModule.find_best_slices(
                slicemax, slicemin, zcoord, R)                   
        
                #Leave slices below zero out.
                
                if zeroslice > slicemin:
                    slicemin = zeroslice 
                
                
                # Make the circle fit again.
                xc, yc, Rc, z_circle, R_circle  = \
                    C_AnglesModule.from_slice_circle(
                    slicemax, slicemin,zcoord, R)
                print "xc=",xc,", Rc =", Rc
                    
                    
#                 if math.isNaN(xc) or math.isNaN(Rc) or ((slicemin==None) and (slicemax==None)) or (slicemin >= slicemax - 1):
#                     print >> myfile, '{0}  {1}  {2}'.format(
#                     filename,'NaN', 'NaN')
#                     print >> myfile2, '{0}  {1}'.format('NaN', 'NaN')
#                     print "ERROR 3: good slices lost. CHECK!"
#                     continue
    
                # Final results: 

                theta = C_AnglesModule.angle(Rc, xc)  #contact angle
                base_r = C_AnglesModule.radius(Rc, xc)  #base radius
                
                
                # Print results on screen.
                print "File analyzed ", filename
                print "Slices used: zero=",  zeroslice, \
                ", min=",  slicemin, ", max=",  slicemax
                print "\n Results: theta=", theta, "base_r=", base_r
        
        
                # Store results in output files.
                
                print >> myfile, '{0}  {1}  {2}'.format(
                filename, theta, base_r)
                print >> myfile2, '{0}  {1}'.format(theta, base_r)
        
        
                # Plot circle with fitted points.
                
                circle_fit_plot =  C_AnglesModule.plot_circ_points(
                z_circle, R_circle, xc, yc, Rc, filename)
                
                
                #Store one plot per page.
                
                pp.savefig(circle_fit_plot)
                
                
    #pp.close()
