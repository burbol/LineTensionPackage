#!/usr/bin/python

import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from fractions import Fraction
import math
#from scipy.optimize import curve_fit
#import os
#from scipy.interpolate import interp1d
#from matplotlib.font_manager import FontProperties


# func is the function of a line, that will be used in the linear fits
def func(x, a, b):
    return a*x + b

#endpoint returns the integer "end": the last data point different then "nan"
def endpoint(theta):
	for end in range(20, len(theta)):
		 if math.isnan(theta[end]):
			    break
	return (end-1)

# The following functions will be used to calculate the block averages and the errorbars
# The function naive_variance will only be used inside the function blockAverage
def naive_variance(data):
    n = 0
    Sum = 0
    Sum_sqr = 0
 
    for x in data:
        n = n + 1
        Sum = Sum + x
        Sum_sqr = Sum_sqr + x*x
 
    variance = (Sum_sqr - (Sum*Sum)/n)/(n - 1)
    return variance

def blockAverage(datastream, Nblocks):
    
    # FIRST WE CREATE AN ARRAY TO STORE THE MEAN VALUES OF THE DATA BLOCKS (blockMean)
    blockMean = np.zeros(Nblocks)  
        
    # Nobs is the number of points (observations) in our data
    Nobs = len(datastream) 
    # BlockSize is the size of each block of data
    BlockSize = int(Nobs//Nblocks) 
    
    if Nblocks==1:
        errorbar = naive_variance(datastream)
        return errorbar

    else:
       # WE CALCULATE IN A LOOP THE MEAN VALUES OF EACH DATA BLOCK (blockMean)
        for i in range(0,Nblocks-1):
            ibeg = i*BlockSize
            iend = (i+1)*BlockSize
            blockMean[i] = np.mean(datastream[ibeg:iend])
            
        # WE TREAT THE LAST BLOCK SEPARATELY, BECAUSE WE HAVE TO TAKE INTO ACCOUNT THE POSSIBLE REMAINING POINTS 
        # WHEN THE NUMBER OF DATA POINTS ISN'T A MULTIPLE OF THE NUMBER OF BLOCKS
        ibeg = (Nblocks-1)*BlockSize
        iend = Nobs
        blockMean[Nblocks-1] = np.mean(datastream[ibeg:iend])
     
        errorbar = (np.std(blockMean))/math.sqrt(Nblocks -1) #np.std(blockMean) is the standard deviation of blockMean
        simulavr = np.mean(blockMean)
        return simulavr, errorbar

#best_start SEARCHS FOR THE STARTING POINT (start) OF BIGGEST TIME INTERVAL where the error interval is smaller then the variation of the data (controlled 
# with a line fit of the data
def best_start(theta,t,omitstart,fixend):

	lastnumber = endpoint(theta)
	endblocks = lastnumber - fixend

	error = np.zeros(endblocks-omitstart) #error will be the total error (of all the points taken each time we choose a different set of data to make the blocks)
	average = np.zeros(endblocks-omitstart) # average is the same, but for the average
	
	slope = np.zeros(endblocks-omitstart)
	intercept = np.zeros(endblocks-omitstart)
	shift = np.zeros(endblocks-omitstart)
	goodblocks = []

	error = error.tolist()
	j=0
	# Loop for finding the "best" interval to do the block averaging
	for i in range (omitstart, endblocks):
		average[j],error[j] = blockAverage((theta[i:lastnumber]),3)
		slope[j], intercept[j], delete1, delete2, delete3 = stats.linregress(t[i:lastnumber],theta[i:lastnumber])
		shift[j] = abs(func(t[i], slope[j], intercept[j]) - func(t[lastnumber], slope[j], intercept[j]))
		if shift[j] <= (2*error[j]):
			goodblocks.append(i)
		j = j+1	 
	if goodblocks==[]: 		# Not equilibrated yet
		return None
	else:
		print "num of good intervals=", len(goodblocks)
		start = min(goodblocks)
		return start
		
		
#create_pi_labels (script from internet) creates ticks ans labels for plot in radians
def create_pi_labels(a, b, step):

    # next line and .limit_denominator solve issues with floating point precision
    max_denominator = int(1/step)


    values = np.arange(a, b+step/10, step)
    fracs = [Fraction(x).limit_denominator(max_denominator) for x in values]
    ticks = values*np.pi

    labels = []

    for frac in fracs:
        if frac.numerator==0:
            labels.append(r"$0$")
        elif frac.numerator<0:
            if frac.denominator==1 and abs(frac.numerator)==1:
                labels.append(r"$-\pi$")
            elif frac.denominator==1:
                labels.append(r"$-{}\pi$".format(abs(frac.numerator)))
            else:
                labels.append(r"$-\frac{{{}}}{{{}}} \pi$".format(abs(frac.numerator), frac.denominator))
        else:
            if frac.denominator==1 and frac.numerator==1:
                labels.append(r"$\pi$")
            elif frac.denominator==1:
                labels.append(r"${}\pi$".format(frac.numerator))
            else:
                labels.append(r"$\frac{{{}}}{{{}}} \pi$".format(frac.numerator, frac.denominator))

    return ticks, labels
    
    
# Plot the equilibrated interval and return results
def equil_results(Waters, angles, pc, Nrows, Ncolumns, blocksNum, beg, t, minblocksize, mylabel, pltname):
          
    fig, ax = plt.subplots(Ncolumns, Nrows,figsize=(5,3.5),dpi=400)
    fig.subplots_adjust(bottom=0.0,top=4.5, left=0., right=2.5, hspace = 0.5)

    matplotlib.rcParams['legend.handlelength'] = 0
    
    theta = [] # microscopic contact angle of equilibrated system
    errortheta = [] # error in the microscopic contact angle of equilibrated system
    equil_theta = [] #equilibrated systems
    #start_theta[b] = [] #first t (time) of the simulation with finite contact angle -> uncomment if needed
    #end_theta[b] = [] # last t (time) of the simulation -> uncomment if needed
        
    i = 0
    for c in Waters:
    
        print "for SAM ",pc,"% and ", c, " molecules:"
    
        #n=Waters.index(c)  -> uncomment if needed

        theta2 = np.array(angles[(pc, c)])
    
        end=endpoint(theta2)
        start=best_start(theta2,t,beg,minblocksize)    

        titletext = r'$\Phi=\ $'+str(pc)+'\%, $n_{W}=\ $'+str(c)

        if start != None:
            slope, intercept, delete1, delete2, delete3 = stats.linregress(t[start:end],theta2[start:end])
            thetamean, errrorbar = blockAverage((theta2[start:end]),blocksNum)
            (errortheta).append(errrorbar)
            (theta).append(thetamean)
            (equil_theta).append(c)
            #(start_theta[pc]).append(start)
            #(end_theta[pc]).append(end)    
        
        else:
            print " Not equilibrated!"
            start = end-40
            slope, intercept, delete1, delete2, delete3 = stats.linregress(t[start:end],theta2[start:end])
            thetamean, errrorbar = blockAverage((theta2[start:end]),blocksNum)
            titletext = titletext +': Not equilibrated'

            
    
        ax = plt.subplot(Nrows, Ncolumns, i+1)
        ax.plot(t[start:end], theta2[start:end],'-',color='orange',linewidth=1.5)  
        ax.plot(t[start:end], func(t[start:end], 0, thetamean+errrorbar),'k-',linewidth=1.5)
        ax.plot(t[start:end], func(t[start:end], 0, thetamean-errrorbar),'k-',linewidth=1.5)
        line1, = ax.plot(t[start:end], func(t[start:end], slope, intercept),'b', label=titletext,linewidth=1.5)
    
    
        #We set the ticks size
        for item in (ax.get_xticklabels() + ax.get_yticklabels()):item.set_fontsize(15)
    
        # Labels with symbols
        ax.set_xlabel(r'$\mathbf{t [ns]}$',fontsize=20)
    
        # Labels with names
        ax.set_ylabel(mylabel,fontsize=23)
    
        #titles for each subplot:
        ax.set_title(titletext,fontsize=20,fontweight='bold')
        ax.set_xlim([t[start],t[end-1]])    

        # Create a legend for the first line.
        #first_legend = plt.legend(loc=1,borderaxespad=0.,borderpad=0.2,fontsize=14)
        # Add the legend manually to the current Axes.
        #ax = plt.gca().add_artist(first_legend)
        
        i = i + 1
    
    plt.show()
    fig.savefig('equil_' + pltname + '_t_s' + str(pc) + '.jpg', bbox_inches='tight',dpi=400)
    
    #return theta, errortheta, equil_theta, start_theta, end_theta -> uncomment if needed
    return theta, errortheta, equil_theta
    
    
# Plot whole simulation and return results
# Uncomment lines for MiddlePoint/GDS  when results are provided
#def whole_results(Waters, angles_w, angles_m, angles_s, pc, Nrows, Ncolumns, blocksNum, beg, t, minblocksize, mylabel, pltname):
def whole_results(Waters, angles_w, angles_s, pc, Nrows, Ncolumns, blocksNum, beg, t, minblocksize, mylabel, pltname):

    # Interface at MiddlePoint/GDS
    #errortheta_m=[]
    #theta_m=[]
    #equil_theta_m=[]
    #start_theta_m=[] -> uncomment if needed
    #end_theta_m=[] -> uncomment if needed

    # Interface at SAM peak
    errortheta_s=[]
    theta_s=[]
    equil_theta_s=[]
    #start_theta_s=[] -> uncomment if needed
    #end_theta_s=[] -> uncomment if needed
    

    fig, ax = plt.subplots(Ncolumns, Nrows,figsize=(5,3.5),dpi=400)
    fig.subplots_adjust(bottom=0.0,top=4.5, left=0., right=2.5, hspace = 0.5)

    matplotlib.rcParams['legend.handlelength'] = 1



    p=0
    i = 0
    for c in Waters:

        print "for SAM ",pc,"% and ", c, " molecules:"
        # n = Waters.index(c) -> uncomment if needed
    
        ax = plt.subplot(Nrows, Ncolumns, i+1)

        theta2_w = np.array(angles_w[(pc, c)])
        #theta2_m = np.array(angles_m[(pc, c)])
        theta2_s = np.array(angles_s[(pc, c)])
    
        end=endpoint(theta2_w) 
        start=best_start(theta2_w,t,beg,minblocksize)
        
        titletext = r'$\Phi=\ $'+str(pc)+'\%, $n_{W}=\ $'+str(c)
        
        # Save results
        
        if start != None:
        
            # Empty arrays to store averages (for plots)
            avrg_w = np.ones(end - start)
            #avrg_m = np.ones(end - start)
            avrg_s = np.ones(end - start)
        
            # Arrays with time variables (for plots)
            t_avrg_w = t[start:end]
            #t_avrg_m = t[start:end]
            t_avrg_s = t[start:end]
        
            # Interface at first water peak (calculated only for plot)
            thetamean, errrorbar =blockAverage((theta2_w[start:end]),blocksNum) 
            avrg_w = thetamean*avrg_w
        
            # Interface at MiddlePoint/GDS
            #thetamean, errrorbar =blockAverage((theta2_m[start:end]),blocksNum)        
            #avrg_m = thetamean*avrg_m
                
            #(errortheta_m).append(errrorbar)
            #(theta_m).append(thetamean)
            #(equil_theta_m).append(c)
            #(start_theta_m).append(start)  -> uncomment if needed
            #(end_theta_m).append(end)  -> uncomment if needed

            # Interface at SAM peak
            thetamean, errrorbar =blockAverage((theta2_s[start:end]),blocksNum)        
            avrg_s = thetamean*avrg_s
               
            (errortheta_s).append(errrorbar)
            (theta_s).append(thetamean)
            (equil_theta_s).append(c)
            #(start_theta_s).append(start)  -> uncomment if needed
            #(end_theta_s).append(end)  -> uncomment if needed
        
            ax.plot(t_avrg_w, avrg_w,'-',color='orange',linewidth=4)
            #ax.plot(t_avrg_m, avrg_m,'-',color='black', linewidth=4)
            ax.plot(t_avrg_s, avrg_s,'g-',linewidth=4)
        
    
            p=p+1
        
        else:
            print " Not equilibrated!"
            start=end-20
            titletext = titletext + ': Not equilibrated'
    
        ax.plot(t, theta2_w,'^',label="Water Peak",color='orange',markersize=7.0)
        #ax.plot(t, theta2_m,'h', color='gray',label="GDS",markersize=6.0)
        ax.plot(t,theta2_s,'s',label="SAM Peak",color='lightgreen',markersize=5.0)
        ax.set_xlim([t[0],t[end-1]])
    
        #We set the ticks size
        for item in (ax.get_xticklabels() + ax.get_yticklabels()):item.set_fontsize(15)
    
        # Labels with symbols
        ax.set_xlabel(r'$\mathbf{t [ns]}$',fontsize=20)
    
        # Labels with names
        ax.set_ylabel(mylabel,fontsize=23)
    
        #titles for each subplot:
        ax.set_title(titletext,fontsize=20,fontweight='bold')
    
        # Create a legend for the first line.
        #first_legend = plt.legend(loc=0,borderaxespad=0.,borderpad=0.2)
        first_legend = plt.legend(loc=0,borderaxespad=0.,borderpad=0.3,fontsize=16,numpoints=1, markerscale=1,handlelength=0.4,handletextpad=0.3)
        # Add the legend manually to the current Axes.
        ax = plt.gca().add_artist(first_legend)
    
        i = i+1

    plt.show()
    fig.savefig(pltname +'_t_s'+str(pc)+'.jpg', bbox_inches='tight',dpi=400)
    
    #return #theta_m,errortheta_m,equil_theta_m, theta_s,errortheta_s,equil_theta_s, start_theta_m, end_theta_m, start_theta_s, end_theta_s -> uncomment if needed
    #return #theta_m,errortheta_m,equil_theta_m, theta_s,errortheta_s,equil_theta_s 
    return theta_s,errortheta_s,equil_theta_s
    
    