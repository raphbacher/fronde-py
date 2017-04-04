# fronde-py
A Fixed-point algorithm for Robust Null Distribution Estimation.

This simple and fast method allows to estimate in a robust way the median and the standard
deviation under the null hypothesis from data samples that can be contaminated by a source signal.
It is a σ-clipping algorithm based on a fixed-point approach.

To install

    python setup.py install

To get robust variance and mean estimators of null distribution of a data vector x

    from fronde import fronde
    import numpy as np
    
    # create null samples
    x=np.random.normal(loc=1,scale=0.5,size=1000)
    
    # add outliers/alternative 
    x[:100] = 10
    
    # get robust mean and variance
    med,var = fronde(x)

You can also try pregenerated data with example.py

    python example.py
