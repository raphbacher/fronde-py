from fronde import fine_clipping
import numpy as np
    
# create null samples
x=np.random.normal(loc=1,scale=0.5,size=1000)
    
# add outliers/alternative 
x[:100] = 10

# get robust mean and variance
med,var = fine_clipping(x)

print med,var
