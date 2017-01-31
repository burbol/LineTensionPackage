#!/usr/bin/python

#source /usr/local/gromacs/bin/GMXRC

import gromacs
gromacs.config.setup()
import matplotlib 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import os
import math
import pylab as pl 
import gromacs.formats
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#copy first peakdetect.py to the work folder!!
#os.chdir('/eixeres/Dropbox/scripts/Python') 
import peakdetect
pk = peakdetect.peakdetect

# The function "peakdetect" is included in the module "peakdetect.py", 
# which can be found at https://gist.github.com/sixtenbe/1178136.
# This is a a copy of its original description:
# peakdetect(y_axis, x_axis = None, lookahead = 300, delta=0):
"""
    Converted from/based on a MATLAB script at: 
    http://billauer.co.il/peakdet.html
    
    function for detecting local maximas and minmias in a signal.
    Discovers peaks by searching for values which are surrounded by lower
    or larger values for maximas and minimas respectively
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- (optional) A x-axis whose values correspond to the y_axis list
        and is used in the return to specify the postion of the peaks. If
        omitted an index of the y_axis is used. (default: None)
    lookahead -- (optional) distance to look ahead from a peak candidate to
        determine if it is the actual peak (default: 200) 
        '(sample / period) / f' where '4 >= f >= 1.25' might be a good value
    delta -- (optional) this specifies a minimum difference between a peak and
        the following points, before a peak may be considered a peak. Useful
        to hinder the function from picking up false peaks towards to end of
        the signal. To work well delta should be set to delta >= RMSnoise * 5.
        (default: 0)
            delta function causes a 20% decrease in speed, when omitted
            Correctly used it can double the speed of the function
    
    return -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a tupple
        of: (position, peak_value) 
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do: 
        x, y = zip(*tab)
"""

#os.chdir('/Users/burbol/Downloads/global_density_maps')
work_folder = '/net/data/eixeres/NewVersion4/FINISHED/'
os.chdir(work_folder)
xvg = gromacs.formats.XVG()


# Name of the file where the Contact Angles will be saved
myfile1 = open('WaterPeak1.txt', 'w')
print >> myfile1, '{0}  {1}'.format('File', 'Water Peaks')
myfile = open('WaterPeak.txt', 'w')
print >> myfile, '{0}'.format('Water Peaks Position')

#pp = PdfPages('/Users/burbol/Downloads/global_density_maps/densplots.pdf')
pp = PdfPages('densplots.pdf')

ticki=np.zeros(24)
for lm in range(0,24): 
    xm = lm*0.5   
    ticki[lm] = xm 

def plot_dens(x, y, filename, point):                   

    majorLocator   = MultipleLocator(1)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator   = MultipleLocator(0.2)
  
#    fig = pl.figure()   
    fig, ax = plt.subplots()                        
    pl.plot(x, y, 'b-', x, y, 'k.')
    fig.suptitle(filename)
    # pl.plot(z, R, 'k.')
    #fig.set_xlim(0,4.0)
    #fig.set_ylim(0,3)                
    # fig = plt.gcf()
    plt.xticks(ticki)
#    plt.xticks(range(0,d_max_y,50))
    pl.xlim(0,12)
    pl.ylim(0,max(y))
    pl.xlabel('z [nm]')
    pl.ylabel('Density [kg/nm3]')
#    pl.grid(b=True, which='both', axis='both', color='r', linestyle='-', linewidth=0.5)
    # fig.set_size_inches(18.5,10.5)
    pl.annotate('first peak', xy=(point[0], point[1]),  xycoords='data', xytext=(-50, 30), textcoords='offset points', arrowprops=dict(arrowstyle="->"))

    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)

    #for the minor ticks, use no labels; default NullFormatter
    ax.xaxis.set_minor_locator(minorLocator)

    ax.xaxis.grid(True, which='minor')
    ax.yaxis.grid(True, which='major')

    return fig
    

# Loop through all the density files in the main directory

#for testing
#for b in [5]:
#    for c in [2000]:
for b in [5, 21, 25, 41]:
    for c in [2000, 3000, 4000, 5000, 6500, 7000, 8000, 9000]:
        #os.chdir('/Users/burbol/Downloads/global_density_maps')
        new_folder = work_folder + '/s'+  str(b) + '_w' + str(c)
        
        #print "nan' if folder doesn't exists (because the simulation hasn't been copied to the backup folder
        # and it is still on scratch probably not finished yet) 
        if not os.path.isdir(new_folder):
			print >> myfile, '{0}  {1}'.format(filename, 'nan')
			print >> myfile, '{0}'.format('nan') 
			print b, c, "not ok"
			continue 
			
        os.chdir(new_folder)
        print b, c, "ok"
        
        print >> myfile1, '             '
#        print >> myfile, '             '
        filename = 'g_density_NVT_sam%d_water%d.xvg'%(b,c, ) 
        xvg.read(filename)
        input = xvg.array
        x = input[0]
        y = input[1]
        [MAXTAB, MINTAB] = pk(y, x, 1, 8)
        point = MAXTAB[0]

# The results are printed to the opened file.
        print >> myfile1, '{0}  {1}'.format(filename, MAXTAB[0])
        print >> myfile, '{0}'.format(point[0]) 

        plot1 =  plot_dens(x, y, filename, point)
        pp.savefig(plot1)


pp.close()
myfile.close()


