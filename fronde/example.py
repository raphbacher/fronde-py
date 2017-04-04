from fronde import fronde
import numpy as np
import scipy.io as sio

#load data example
Lmat = sio.loadmat('L.mat’)
L = Lmat['L']

# get robust mean and variance
med,var = fronde(np.reshape(L, -1))

print med,var

# ----------------
    
# Create null samples
x=np.random.normal(loc=1,scale=0.5,size=1000)
    
# add outliers/alternative 
x[:100] = 10

# get robust mean and variance
med,var = fronde(x)

print(med,var)
