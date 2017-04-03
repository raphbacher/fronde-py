# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:43:43 2016

@author: celine.meillier@unistra.fr, raphael.bacher@gipsa-lab.fr
"""
from scipy.stats import norm
import numpy as np


def fine_clipping(x, niter = 20, fact_value = 0.9,sym=True):
    """
    Robust estimation of median and variance of data
    Parameters
    ----------
    x : array_like
        Input array.
    niter : int
        Max number of iterations.
    fact_value: float (between 0 and 1)
        Factor of truncation (for improved robustness.)
    sym: bool
        If True compute sigma using interquartile Q3-Q1 else use median-Q1

    Returns
    -------
    medclip : scalar
        Robust median estimate
    sigclip2 : scalar
        Robust standard deviation estimate
    
    """
    x_sorted=np.sort(x)
    fact_IQR=norm.ppf(0.75)-norm.ppf(0.25)
    xclip = x_sorted
    
    #Initialize
    facttrunc = norm.ppf(fact_value)
    cdf_facttrunc=norm.cdf(facttrunc)
    correction = norm.ppf((0.75*( 2*cdf_facttrunc-1 ) + (1 - cdf_facttrunc) )) - norm.ppf(0.25*( 2*cdf_facttrunc-1 ) + (1 - cdf_facttrunc) )
    medclip = middle(xclip)
    qlclip = percent(xclip, 25)
    stdclip = 2.*(medclip - qlclip)/fact_IQR    
    oldmedclip=1.
    oldstdclip=1.
    i=0
    
    #Loop
    while ( (oldmedclip,oldstdclip) != (medclip,stdclip)) and (i < niter):
        lim=np.searchsorted(x_sorted,[medclip-facttrunc*stdclip,medclip+facttrunc*stdclip])
        xclip = x_sorted[lim[0]:lim[1]]
        oldoldmedclip=oldmedclip
        oldmedclip = medclip
        oldoldstdclip=oldstdclip
        oldstdclip=stdclip
        medclip = middle(xclip)
        qlclip = percent(xclip, 25)
        qlclip2 = percent(xclip, 75)
        if sym==True:
            stdclip = np.abs(qlclip2 - qlclip)/correction
        else:
            stdclip = 2*np.abs(medclip - qlclip)/correction
        
        if oldoldmedclip ==medclip:#gestion des cycles
            if stdclip>oldstdclip:
                break
            else:
                stdclip=oldstdclip
                medclip=oldmedclip
        i+=1

    #Refinement of sigma estimation using only uncontaminated lower values.
    xclip2 = x_sorted[np.where( ((x_sorted-medclip) <0) & ((x_sorted-medclip) > -3*stdclip)) ]
    correctionTrunc= np.sqrt( 1. +(-3.*2.* norm.pdf(3.)) / (2.*norm.cdf(3.) -1.) )
    stdclip2 = np.sqrt( np.mean( (xclip2-medclip)**2)) / correctionTrunc
    
    return medclip,stdclip2

def middle(L):
    """
    L: np.array 
    Get median assuming L is sorted
    """
    n = len(L)
    m = n - 1
    return (L[n/2] + L[m/2]) / 2.0

def percent(L,q):
    """
    L: np.array
    q: float betwwen 0-100
    """
    n0=q/100. * len(L)
    n = int(np.floor(n0))
    if n>=len(L):
        return L[-1]
    if n >= 1:
        if n==n0:
            return L[n-1]
        else:
            return (L[n-1]+L[n])/2.0
    else:
        return L[0]
