import numpy as np

# Evaluate function based on Chebyshev expansion coefficients
#
# ----------------------------------------------------------------------
#
# Input:
#       x, coef
#       parity  -- 0 for even, 1 for odd
#  partialcoef  -- true: only include even/odd coefficiennts
# Output:
#       ret     -- function at x

def ChebyCoef2Func(x, coeff, parity, partialcoeff):
    ret = np.zeros((len(x), 1))
    y = np.arccos(x)
    len_coeff = len(coeff)
    if partialcoeff:
        if parity == 0:
            for k in range(len_coeff):
                ret += coeff[k] * np.cos(2*k*y)
        else:
            for k in range(len_coeff):
                ret += coeff[k] * np.cos((2 * (k+1) - 1) * y)
    else:
        if parity == 0:
            for k in range(0, len_coeff, 2):
                ret += coeff[k] * cos(k * y)
        else:
            for k in range(1, len_coeff, 2):
                ret += coeff[k] * cos(k * y)
    return ret