import numpy as np
from scipy.optimize import curve_fit
from scipy import odr
import math
import pylab as pl


def frange(start, end, inc):
    """Function range with float increments.
    
    Imported from:
    http://code.activestate.com/recipes/66472-frange-a-range-function-with-float-increments/.
    """
    
    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L
            

def sigmoid_guess(y):
    """Find initial estimate for the first parameter of sigmoid fit.
    
    Args:
    y(array): Radial density profile at one z-coordinate.
    
    Returns:
    sig_guess(float): Initial parameter estimate.
    
    The output is the mean of the density values that are at least 
    two thirds of the maximum density. 
    """
    m = max(y)
    m2 = min(y)
    third = (m - m2)/3
    bottom = m - third
    tot = 0
    count = 0
    for i in range(0, len(y)):
        if y[i] >= bottom:
            tot = tot + y[i]
            count = count + 1
    sig_guess = tot / count
    return sig_guess
    
def sigmoid_func(r, ro, R, d):
    return (ro/2)*(1-np.tanh(2*(r-R)/d))


def sigmoidfit(input):
    """Make sigmoidal fit of density profiles at every z-coordinate.
    
    The input function (sigmoid_func) is fitted to the density profiles of all z-coordinates
    (to each z-coordinate or "slice" corresponds one radial density profile).
    
    Args:
    input(ndarray): input[0] stores array with z-coordinates . The 
                            remaining elements (arrays) are radial density profiles for
                            the different z-coordinates (array of arrays).

    Returns:
    ro_sigmoid(array): Parameter from sigmoidal fit.
    R_sigmoid(array): Parameter from sigmoidal fit (cylindrical radius).
    d_sigmoid(array): Parameter from sigmoidal fit.
    
    The output parameters are arrays because there is one fitted parameter for each 
    z-coordinate (one radial density profile of each horizontal "slice").
     
    "maxfev" is a parameter of scipy.optimize.curve_fit. It is the 
    allowed number of funtion calls when doing the 
    fit. Default (maxfev=800) is too low.
    """
    # Save z-coordinates in array "z"
    
    z = input[0] 
    
    
    # Save total number of "slices" in integer "slicestotal"
    # (one corresponding to each z-coordinate)
    
    slicestotal = len(input)
    
        
    #Create empty arrays to store output
    
    ro_sigmoid = np.zeros(slicestotal)
    R_sigmoid = np.zeros(slicestotal)
    d_sigmoid = np.zeros(slicestotal)

    
    # Loop through all z-coordinates ("slices")
    
    for i in range(0,slicestotal):
    
        # Save in array "slicedens" the radial density profile of 
        # the "ith-slice"
        slicedens = input[i]  
        
        # Save inital guess of the fitting parameters in the float "fit_guess"
        
        fit_guess = sigmoid_guess(slicedens)
        
        # Fit sigmoidal function to radial density profile.
        # Then save each parameter from the fit in a separate array (in the ith position)
        popt, pcov = curve_fit(sigmoid_func, z, slicedens,[fit_guess, 2, 1], maxfev=100000)
        ro_sigmoid[i], R_sigmoid[i], d_sigmoid[i] = popt
    return ro_sigmoid, R_sigmoid, d_sigmoid


def waterbulk(input, r0, R_cyl, d ):
    """Calculate bulk value of water drop from radial density profile matrix.
    
    Only the region with mean density > 800kg/m3 is used to calculate
    the bulk value. The mean density of each z-coordinate (slice) is
    the mean density at the center (radius = 0) calculated as the
    value of a sigmoidal function at radius = 0.
    
    Args: 
    input(ndarray): input[0] stores array with z-coordinates . The 
                  remaining elements are radial density profiles for
                  the different z-coordinates (array of arrays).
    r0(array): Parameter from sigmoidal fit.
    R_cyl(array): Parameter from sigmoidal fit (cylindrical radius).
    d(array): Parameter from sigmoidal fit.
    
    Returns:
    bulk(float): Bulk density.
    """
    waterdensity = 1000 # kg/m3
    mindensity = 0.8*waterdensity

    slicestotal = len(input)
    densmean = np.zeros(slicestotal) 
    i = 0
    totaldens = 0
    
    for slice in range(1,slicestotal):
        central_dens = sigmoid_func(0, r0[slice], R_cyl[slice], d[slice])
        densmean[slice]=central_dens
        
        if central_dens > mindensity:
            i = i + 1
            totaldens = totaldens + central_dens
            bulk = totaldens/i
    return bulk


def checkslice(r0, R_cyl, d, bulk):
    """Check if density at drop center is bigger than 90% of bulk value.

    Use parameters from sigmoid fit to check if the mean density
    at the drop center (R_cyl=0) is greater then 90% of the bulk value.

    Args:
    r0(float): Parameter from sigmoidal fit.
    R_cyl(float): Parameter from sigmoidal fit (cylindrical radius).
    d(float): Parameter from sigmoidal fit.
    bulk(float): Bulk density.

    Returns: Boolean.
    """
    k = sigmoid_func(0, r0, R_cyl, d)
    bulklimit = 0.9*bulk
    if k > bulklimit:
        return True
    else: 
        return False
    
    
def circle_radius(xc, yc, x, y):
    """ Calculate distance of (x,y) to (xc, yc). """
    
    return np.sqrt((x-xc)**2 + (y-yc)**2)


def implicit_circle(circle_params, x):
    """ Implicit function of circle with center at (x,0).
    
    Args:
    circle_params(array): Three parameters of the circle:
                        ---circle_params[0],circle_params[1] are the 
                            circle center coordinates.
                        ---circle_params[2] is the circle radius.
    x(array): Function variables (x,y) = (x[0], x[1]).
    """
    return (x[0]-circle_params[0])**2 + (x[1])**2 - circle_params[2]**2
    
    
def from_slice_circle(slicemax, slicemin, zcoord, cyl_radius):
    """Circle fit to cylindrical radius of consecutive slices.

    Args:
    slicemin(int): First slice.
    slicemax(int): Last slice.
    zcoord(list): z-coordinates of all slices.
    cyl_radius(array): Cylindrical radii of all slices.
    
    Returns: 
    xc(float): Coordinate of circle center (xc,yc).
    yc(float) = 0.0: Coordinate of circle center (xc,yc) set to zero
                    (corresponds to the cylindrical radius).
    R(float): Circle radius.
    x(array): Coordinate of points used for the fit (z-coordinates).
    y(array): Coordinate of points used for the fit (cylindrical radii).
 
    Circle fit imported from:
    "http://wiki.scipy.org/Cookbook/Least_Squares_Circle"
    Method used for fit: "Orthogonal distance regression"
    """
    dims = slicemax - slicemin + 1
    
    if dims<=1 or (dims is None):
        return float('nan'), 0.0, float('nan'), [float('nan')], [float('nan')]
        
    else:
        i=0
        x = np.zeros(dims)
        y = np.zeros(dims)
        for a in range(slicemin,  slicemax + 1):
            i = a - slicemin
            x[i] = zcoord[a-1] 
            y[i] = cyl_radius[a]

        # coordinates of the barycenter: x_m and y_m = 0
        x_mean = np.mean(x)
     
        # initial guess for parameters
        R_mean = circle_radius(x_mean, 0, x, y).mean()
        start_guess = [ x_mean, 0, R_mean]
     
        # circle fit from implicit function :
        data_for_fit= odr.Data(np.row_stack([x, y]), y=1)
        model_for_fit  = odr.Model(implicit_circle, implicit=True)
        
        #Instantiate ODR with data, model and initial parameter estimate
        input_odr    = odr.ODR(data_for_fit, model_for_fit, start_guess)
        
        #Run the fit
        output_odr    = input_odr.run()
        
        #Investigate output 
        xc, yc, R = output_odr.beta
        
        # Residues may also be used 
        
        #Ri = circle_radius(xc, yc, x, y)
        #residu = sum((Ri - R)**2) # error of circle fit 
        #residu2 = sum((Ri**2-R**2)**2) #quadratic error

        return xc, 0.0, R, x, y

    
def distance(x, y, xc, yc,R):
    """Calculate shortest distance between a point and a circle. 

    Args:
    x(float): Coordinate of point (x,y).
    y(float): Coordinate of point (x,y).
    xc(float): Coordinate of circle center (xc,yc).
    yc(float): Coordinate of circle center (xc,yc).
    R(float): Circle radius.

    Returns:
    d(float): Shortest distance point-circle.
    """
    a = np.asarray([x,y])
    b = np.asarray([xc,yc])
    d = np.linalg.norm(a - b)- R
    d = math.fabs(d)
    return d 
    
    
def find_best_slices(slicemax, slicemin, zcoord, cyl_radius):
    """Find "best" slices for circle fit.

    Fit circle to cylindrical radius of each droplet slice between "slicemin"
    and "slicemax". Find maximum number of "good slices": where
    distance of "slicemin" to circle is smaller than epsilon, 
    and "slicemax" to circle smaller than epsilon2.
    
    Args:
    slicemax: Initial guess for slicemax (with d < epsilon).
    slicemin: Initial guess for slicemin (with d < epsilon).
    zcoord(list): z-coordinates of each slice.
    cyl_radius(array): Cylindrical radius of each slice. 
    
    Returns:
    slicemin(int):  Lower "good" slices".
    slicemax(int): Higher "good" slices".
    """
    epsilon = 0.03 # For slicemin
    epsilon2 = 0.031 # For slicemax
    
    if from_slice_circle(slicemax, slicemin, zcoord, cyl_radius)==None:
        return None,None

    # Find slicemin
    
    # fit circle 
    xc, yc, R_2, z_circle, R_circle =  from_slice_circle(slicemax, slicemin, zcoord, cyl_radius)
    
    # distance from point to circle
    d = distance(z_circle[0], R_circle[0], xc, yc, R_2)
    
    #If d < epsilon: start new loop with slicemin - 1   
    
    if d <= epsilon:
        while d <= epsilon:
            old_slicemin = slicemin
            slicemin = old_slicemin - 1
            old_d = d
            xc, yc, R_2,z_circle, R_circle =  from_slice_circle(slicemax, slicemin, zcoord, cyl_radius)
            d = distance(z_circle[0], R_circle[0], xc, yc, R_2)
            
    #If d > epsilon: return slicemin - 1
    
    elif d > epsilon:
        while d > epsilon:
            old_slicemin = slicemin
            slicemin = old_slicemin + 1
            old_d = d
            xc, yc, R_2,  z_circle, R_circle =  from_slice_circle(slicemax, slicemin, zcoord, cyl_radius)
            d = distance(z_circle[0], R_circle[0], xc, yc, R_2)

    if d > epsilon:
        slicemin = old_slicemin
        d = old_d

    # Find slicemax

    xc, yc, R_2, z_circle, R_circle =  from_slice_circle(slicemax, slicemin, zcoord, cyl_radius)
    d = distance(z_circle[-1], R_circle[-1], xc, yc, R_2)
    
    #If d < epsilon: start new loop with slicemax + 1
    
    if d <= epsilon2:
        while d <= epsilon2:      
            oldslicemax = slicemax
            slicemax = oldslicemax + 1
            old_d = d
            xc, yc, R_2, z_circle, R_circle =  from_slice_circle(slicemax, slicemin, zcoord, cyl_radius)
            d = distance(z_circle[-1], R_circle[-1], xc, yc, R_2)
            
    #If d > epsilon: return slicemax + 1
    
    elif d > epsilon2:
        while d > epsilon2:
            oldslicemax = slicemax
            slicemax = oldslicemax - 1
            old_d = d
            xc, yc, R_2, z_circle, R_circle =  from_slice_circle(slicemax, slicemin, zcoord, cyl_radius)
            d = distance(z_circle[-1], R_circle[-1], xc, yc, R_2)
            
    if d > epsilon2:
        slicemax = oldslicemax
        d = old_d

    return slicemin, slicemax
    
    
def angle(R, Zc):
    """Calculate the contact angle of a sphere cap.

    Args:
    R(float): Radius of complete sphere.
    Zc(float): Coordinate of sphere center (Zc,0).
    
    Returns:
    theta(float): Contact angle in degrees.
    """
    phi = Zc / np.sqrt(R**2 - Zc**2)
    theta = math.degrees(np.arctan(phi)) + 90
    return theta
    

def radius(R, Zc):
    """Calculate the base radius of sphere cap.
    
    Args:
    R(float): Radius of complete sphere.
    Zc(float): Coordinate of sphere center (Zc,0).
    
    Returns:
    r_base(float): Base radius.
    """
    r_base = np.sqrt(R**2 - Zc**2)
    return r_base


def plot_circ_points(x, y, xc, yc, Rc,filename):
    """Plot circle fit together with points used for fit.

    Args:
    x(array): Coordinate of points used for fit (x,y).
    y(array): Coordinate of points used for fit (x,y).
    xc(float): Coordinate of circle center (xc,yc).
    yc(float): Coordinate of circle center (xc,yc).
    Rc(float): Radius of circle.

    Returns:
    fig: figure object
    """
    fig = pl.figure()
    theta_fit = np.linspace(-np.pi, np.pi, 180)
    x_circle = xc + Rc*np.cos(theta_fit)
    y_circle = yc + Rc*np.sin(theta_fit)
    pl.plot(y_circle, x_circle, 'b-', y, x, 'k.')
    fig.suptitle(filename)
    pl.xlim(0,2*Rc+ 1.0)
    pl.ylim(0,2*Rc+ 1.0)
    pl.xlabel('R [nm]')
    pl.ylabel('z [nm]')
    pl.grid(True)
    
    return fig    
