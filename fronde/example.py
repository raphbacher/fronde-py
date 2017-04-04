from fronde import fronde
import numpy as np
import scipy.io as sio

#load data example
Lmat = sio.loadmat('L.mat')
L = Lmat['L']

# get robust mean and variance
med,var = fronde(np.reshape(L, -1))

print med,var
